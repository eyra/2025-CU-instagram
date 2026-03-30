import { test, expect } from '@playwright/test';
import * as path from 'path';

test('can upload a zip file and view contents', async ({ page, context }) => {
  // Navigate first to be able to clear storage
  await page.goto('http://localhost:3000/');

  // Clear all browser storage to force fresh pyodide/wheel loading
  await context.clearCookies();
  await page.evaluate(async () => {
    // Clear IndexedDB (where pyodide caches wheels)
    const databases = await indexedDB.databases();
    for (const db of databases) {
      if (db.name) {
        indexedDB.deleteDatabase(db.name);
      }
    }
    // Clear localStorage and sessionStorage
    localStorage.clear();
    sessionStorage.clear();
  });

  // Reload page to get fresh wheel
  await page.reload();

  // Wait for the page to load with increased timeout
  await expect(page.getByRole('heading', { name: 'Instagram' })).toBeVisible({ timeout: 30000 });
  
  // Create a temporary file input for file upload (Playwright needs to use setInputFiles method)
  const fileChooserPromise = page.waitForEvent('filechooser');
  await page.getByText('Choose file').click();
  const fileChooser = await fileChooserPromise;

  // Set a test zip file path (you'll need to ensure this file exists)
  const zipFilePath = path.join(__dirname,  'test.zip');
  await fileChooser.setFiles(zipFilePath);

  // Click continue to process the file
  await page.getByText('Continue').click();

  // Check that the ZIP file content is visible
  await expect(page.getByText('Summary information', {exact: true})).toBeVisible();

  // Check that the donation actions are visible
  await expect(page.getByText('Would you like to donate this data?')).toBeVisible({ timeout: 10000 });
});
