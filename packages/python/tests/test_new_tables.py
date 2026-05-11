#!/usr/bin/env python
"""Test script for new tables: saved_posts, liked_posts, liked_comments"""

import json
import zipfile
import io
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock
import pytest

# Mock the js module before importing port modules
sys.modules['js'] = MagicMock()

# Add the port package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from port.script import extract_data, extract_saved_posts, extract_liked_posts, extract_liked_comments
from port.api.commands import FlushLogs


def _run(zip_path):
    results = None
    for item in extract_data(zip_path, "en"):
        if item is not FlushLogs:
            results = item
    return results


def create_test_zip_with_saved_posts():
    """Create a test zip with saved posts and collections data"""
    base_date = datetime.now()

    # saved_collections.json - posts saved to collections
    saved_collections_data = {
        "saved_saved_collections": [
            # Collection header
            {
                "title": "Collection",
                "string_map_data": {
                    "Name": {"value": "Travel"},
                    "Creation Time": {"timestamp": int((base_date - timedelta(days=100)).timestamp())},
                    "Update Time": {"timestamp": int((base_date - timedelta(days=10)).timestamp())}
                }
            },
            # Post in collection
            {
                "string_map_data": {
                    "Name": {
                        "href": "https://www.instagram.com/p/ABC123/",
                        "value": "travel_blogger"
                    },
                    "Added Time": {"timestamp": int((base_date - timedelta(days=5)).timestamp())}
                }
            },
            # Another collection header
            {
                "title": "Collection",
                "string_map_data": {
                    "Name": {"value": "Food"},
                    "Creation Time": {"timestamp": int((base_date - timedelta(days=50)).timestamp())},
                    "Update Time": {"timestamp": int((base_date - timedelta(days=2)).timestamp())}
                }
            },
            # Post in Food collection
            {
                "string_map_data": {
                    "Name": {
                        "href": "https://www.instagram.com/p/DEF456/",
                        "value": "food_lover"
                    },
                    "Added Time": {"timestamp": int((base_date - timedelta(days=3)).timestamp())}
                }
            },
        ]
    }

    # saved_posts.json - posts saved without collection
    saved_posts_data = {
        "saved_saved_media": [
            {
                "title": "random_user",
                "string_map_data": {
                    "Saved on": {
                        "href": "https://www.instagram.com/p/GHI789/",
                        "timestamp": int((base_date - timedelta(days=7)).timestamp())
                    }
                }
            },
            {
                "title": "another_user",
                "string_map_data": {
                    "Saved on": {
                        "href": "https://www.instagram.com/p/JKL012/",
                        "timestamp": int((base_date - timedelta(days=14)).timestamp())
                    }
                }
            },
        ]
    }

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("instagram/saved/saved_collections.json", json.dumps(saved_collections_data))
        zf.writestr("instagram/saved/saved_posts.json", json.dumps(saved_posts_data))
        # Add minimal required files
        zf.writestr("instagram/content/posts_1.json", json.dumps([]))
        zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

    zip_buffer.seek(0)
    return zip_buffer


def create_test_zip_with_liked_posts():
    """Create a test zip with liked posts data"""
    base_date = datetime.now()

    liked_posts_data = {
        "likes_media_likes": [
            {
                "title": "author1",
                "string_list_data": [
                    {
                        "href": "https://www.instagram.com/p/POST001/",
                        "value": "\u00f0\u009f\u0091\u008d",
                        "timestamp": int((base_date - timedelta(days=1)).timestamp())
                    }
                ]
            },
            {
                "title": "author2",
                "string_list_data": [
                    {
                        "href": "https://www.instagram.com/p/POST002/",
                        "value": "\u00f0\u009f\u0091\u008d",
                        "timestamp": int((base_date - timedelta(days=2)).timestamp())
                    }
                ]
            },
            {
                "title": "author3",
                "string_list_data": [
                    {
                        "href": "https://www.instagram.com/p/POST003/",
                        "value": "\u00f0\u009f\u0091\u008d",
                        "timestamp": int((base_date - timedelta(days=3)).timestamp())
                    }
                ]
            },
        ]
    }

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("instagram/likes/liked_posts.json", json.dumps(liked_posts_data))
        # Add minimal required files
        zf.writestr("instagram/content/posts_1.json", json.dumps([]))
        zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

    zip_buffer.seek(0)
    return zip_buffer


def create_test_zip_with_liked_comments():
    """Create a test zip with liked comments data"""
    base_date = datetime.now()

    liked_comments_data = {
        "likes_comment_likes": [
            {
                "title": "commenter1",
                "string_list_data": [
                    {
                        "href": "https://www.instagram.com/reel/REEL001/",
                        "value": "\u00f0\u009f\u0091\u008d",
                        "timestamp": int((base_date - timedelta(days=1)).timestamp())
                    }
                ]
            },
            {
                "title": "commenter2",
                "string_list_data": [
                    {
                        "href": "https://www.instagram.com/p/POST001/",
                        "value": "\u00f0\u009f\u0091\u008d",
                        "timestamp": int((base_date - timedelta(days=5)).timestamp())
                    }
                ]
            },
        ]
    }

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("instagram/likes/liked_comments.json", json.dumps(liked_comments_data))
        # Add minimal required files
        zf.writestr("instagram/content/posts_1.json", json.dumps([]))
        zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

    zip_buffer.seek(0)
    return zip_buffer


def create_test_zip_with_all_new_tables():
    """Create a test zip with all new tables"""
    base_date = datetime.now()

    saved_collections_data = {
        "saved_saved_collections": [
            {
                "title": "Collection",
                "string_map_data": {
                    "Name": {"value": "MyCollection"},
                    "Creation Time": {"timestamp": int((base_date - timedelta(days=100)).timestamp())},
                    "Update Time": {"timestamp": int((base_date - timedelta(days=10)).timestamp())}
                }
            },
            {
                "string_map_data": {
                    "Name": {
                        "href": "https://www.instagram.com/p/COLL001/",
                        "value": "collected_author"
                    },
                    "Added Time": {"timestamp": int((base_date - timedelta(days=5)).timestamp())}
                }
            },
        ]
    }

    saved_posts_data = {
        "saved_saved_media": [
            {
                "title": "saved_author",
                "string_map_data": {
                    "Saved on": {
                        "href": "https://www.instagram.com/p/SAVE001/",
                        "timestamp": int((base_date - timedelta(days=7)).timestamp())
                    }
                }
            },
        ]
    }

    liked_posts_data = {
        "likes_media_likes": [
            {
                "title": "liked_post_author",
                "string_list_data": [
                    {
                        "href": "https://www.instagram.com/p/LIKE001/",
                        "value": "\u00f0\u009f\u0091\u008d",
                        "timestamp": int((base_date - timedelta(days=2)).timestamp())
                    }
                ]
            },
        ]
    }

    liked_comments_data = {
        "likes_comment_likes": [
            {
                "title": "liked_comment_author",
                "string_list_data": [
                    {
                        "href": "https://www.instagram.com/p/COMM001/",
                        "value": "\u00f0\u009f\u0091\u008d",
                        "timestamp": int((base_date - timedelta(days=3)).timestamp())
                    }
                ]
            },
        ]
    }

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("instagram/saved/saved_collections.json", json.dumps(saved_collections_data))
        zf.writestr("instagram/saved/saved_posts.json", json.dumps(saved_posts_data))
        zf.writestr("instagram/likes/liked_posts.json", json.dumps(liked_posts_data))
        zf.writestr("instagram/likes/liked_comments.json", json.dumps(liked_comments_data))
        # Add minimal required files
        zf.writestr("instagram/content/posts_1.json", json.dumps([]))
        zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

    zip_buffer.seek(0)
    return zip_buffer


class TestSavedPostsTable:
    """Tests for Saved Posts table extraction"""

    def test_saved_posts_table_exists(self):
        """Test that saved posts table is generated"""
        test_zip = create_test_zip_with_saved_posts()
        results = _run(test_zip)

        saved_posts_table = next((r for r in results if r.id == "instagram_saved_posts"), None)
        assert saved_posts_table is not None, "Saved posts table should exist"

    def test_saved_posts_has_correct_columns(self):
        """Test that saved posts table has the correct columns"""
        test_zip = create_test_zip_with_saved_posts()
        results = _run(test_zip)

        saved_posts_table = next((r for r in results if r.id == "instagram_saved_posts"), None)
        assert saved_posts_table is not None

        df = saved_posts_table.data_frame
        expected_columns = ["Date and time", "Author", "URL", "Collection"]
        assert list(df.columns) == expected_columns, f"Expected columns {expected_columns}, got {list(df.columns)}"

    def test_saved_posts_count(self):
        """Test that saved posts table has correct number of rows"""
        test_zip = create_test_zip_with_saved_posts()
        results = _run(test_zip)

        saved_posts_table = next((r for r in results if r.id == "instagram_saved_posts"), None)
        assert saved_posts_table is not None

        df = saved_posts_table.data_frame
        # 2 posts from collections + 2 posts without collection = 4 total
        assert len(df) == 4, f"Expected 4 saved posts, got {len(df)}"

    def test_saved_posts_collection_assignment(self):
        """Test that posts in collections have correct collection name"""
        test_zip = create_test_zip_with_saved_posts()
        results = _run(test_zip)

        saved_posts_table = next((r for r in results if r.id == "instagram_saved_posts"), None)
        df = saved_posts_table.data_frame

        # Check that collection posts have collection names
        travel_posts = df[df["Collection"] == "Travel"]
        assert len(travel_posts) == 1, "Expected 1 post in Travel collection"

        food_posts = df[df["Collection"] == "Food"]
        assert len(food_posts) == 1, "Expected 1 post in Food collection"

        # Check that non-collection posts have "-" as collection
        no_collection_posts = df[df["Collection"] == "-"]
        assert len(no_collection_posts) == 2, "Expected 2 posts without collection"

    def test_saved_posts_authors(self):
        """Test that authors are correctly extracted"""
        test_zip = create_test_zip_with_saved_posts()
        results = _run(test_zip)

        saved_posts_table = next((r for r in results if r.id == "instagram_saved_posts"), None)
        df = saved_posts_table.data_frame

        authors = set(df["Author"].tolist())
        expected_authors = {"travel_blogger", "food_lover", "random_user", "another_user"}
        assert authors == expected_authors, f"Expected authors {expected_authors}, got {authors}"


class TestLikedPostsTable:
    """Tests for Liked Posts table extraction"""

    def test_liked_posts_table_exists(self):
        """Test that liked posts table is generated"""
        test_zip = create_test_zip_with_liked_posts()
        results = _run(test_zip)

        liked_posts_table = next((r for r in results if r.id == "instagram_liked_posts"), None)
        assert liked_posts_table is not None, "Liked posts table should exist"

    def test_liked_posts_has_correct_columns(self):
        """Test that liked posts table has the correct columns"""
        test_zip = create_test_zip_with_liked_posts()
        results = _run(test_zip)

        liked_posts_table = next((r for r in results if r.id == "instagram_liked_posts"), None)
        assert liked_posts_table is not None

        df = liked_posts_table.data_frame
        expected_columns = ["Date and time", "Author", "URL"]
        assert list(df.columns) == expected_columns, f"Expected columns {expected_columns}, got {list(df.columns)}"

    def test_liked_posts_count(self):
        """Test that liked posts table has correct number of rows"""
        test_zip = create_test_zip_with_liked_posts()
        results = _run(test_zip)

        liked_posts_table = next((r for r in results if r.id == "instagram_liked_posts"), None)
        assert liked_posts_table is not None

        df = liked_posts_table.data_frame
        assert len(df) == 3, f"Expected 3 liked posts, got {len(df)}"

    def test_liked_posts_authors(self):
        """Test that authors are correctly extracted"""
        test_zip = create_test_zip_with_liked_posts()
        results = _run(test_zip)

        liked_posts_table = next((r for r in results if r.id == "instagram_liked_posts"), None)
        df = liked_posts_table.data_frame

        authors = set(df["Author"].tolist())
        expected_authors = {"author1", "author2", "author3"}
        assert authors == expected_authors, f"Expected authors {expected_authors}, got {authors}"

    def test_liked_posts_urls(self):
        """Test that URLs are correctly extracted"""
        test_zip = create_test_zip_with_liked_posts()
        results = _run(test_zip)

        liked_posts_table = next((r for r in results if r.id == "instagram_liked_posts"), None)
        df = liked_posts_table.data_frame

        urls = set(df["URL"].tolist())
        assert "https://www.instagram.com/p/POST001/" in urls
        assert "https://www.instagram.com/p/POST002/" in urls
        assert "https://www.instagram.com/p/POST003/" in urls


class TestLikedCommentsTable:
    """Tests for Liked Comments table extraction"""

    def test_liked_comments_table_exists(self):
        """Test that liked comments table is generated"""
        test_zip = create_test_zip_with_liked_comments()
        results = _run(test_zip)

        liked_comments_table = next((r for r in results if r.id == "instagram_liked_comments"), None)
        assert liked_comments_table is not None, "Liked comments table should exist"

    def test_liked_comments_has_correct_columns(self):
        """Test that liked comments table has the correct columns"""
        test_zip = create_test_zip_with_liked_comments()
        results = _run(test_zip)

        liked_comments_table = next((r for r in results if r.id == "instagram_liked_comments"), None)
        assert liked_comments_table is not None

        df = liked_comments_table.data_frame
        expected_columns = ["Date and time", "Author", "URL"]
        assert list(df.columns) == expected_columns, f"Expected columns {expected_columns}, got {list(df.columns)}"

    def test_liked_comments_count(self):
        """Test that liked comments table has correct number of rows"""
        test_zip = create_test_zip_with_liked_comments()
        results = _run(test_zip)

        liked_comments_table = next((r for r in results if r.id == "instagram_liked_comments"), None)
        assert liked_comments_table is not None

        df = liked_comments_table.data_frame
        assert len(df) == 2, f"Expected 2 liked comments, got {len(df)}"

    def test_liked_comments_authors(self):
        """Test that authors are correctly extracted"""
        test_zip = create_test_zip_with_liked_comments()
        results = _run(test_zip)

        liked_comments_table = next((r for r in results if r.id == "instagram_liked_comments"), None)
        df = liked_comments_table.data_frame

        authors = set(df["Author"].tolist())
        expected_authors = {"commenter1", "commenter2"}
        assert authors == expected_authors, f"Expected authors {expected_authors}, got {authors}"


class TestAllNewTables:
    """Test all new tables together"""

    def test_all_new_tables_present(self):
        """Test that all three new tables are generated"""
        test_zip = create_test_zip_with_all_new_tables()
        results = _run(test_zip)

        result_ids = [r.id for r in results]

        assert "instagram_saved_posts" in result_ids, "Saved posts table should exist"
        assert "instagram_liked_posts" in result_ids, "Liked posts table should exist"
        assert "instagram_liked_comments" in result_ids, "Liked comments table should exist"

    def test_new_tables_have_titles(self):
        """Test that new tables have proper titles"""
        test_zip = create_test_zip_with_all_new_tables()
        results = _run(test_zip)

        saved_posts = next((r for r in results if r.id == "instagram_saved_posts"), None)
        liked_posts = next((r for r in results if r.id == "instagram_liked_posts"), None)
        liked_comments = next((r for r in results if r.id == "instagram_liked_comments"), None)

        # Titles are Translatable objects with translations dict
        assert saved_posts.title is not None
        assert liked_posts.title is not None
        assert liked_comments.title is not None


class TestEmptyData:
    """Test behavior with empty or missing data"""

    def test_empty_saved_posts(self):
        """Test that empty saved posts data doesn't crash"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/saved/saved_posts.json", json.dumps({"saved_saved_media": []}))
            zf.writestr("instagram/saved/saved_collections.json", json.dumps({"saved_saved_collections": []}))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)
        results = _run(zip_buffer)

        saved_posts = next((r for r in results if r.id == "instagram_saved_posts"), None)
        assert saved_posts is not None
        assert len(saved_posts.data_frame) == 0

    def test_empty_liked_posts(self):
        """Test that empty liked posts data doesn't crash"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/likes/liked_posts.json", json.dumps({"likes_media_likes": []}))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)
        results = _run(zip_buffer)

        liked_posts = next((r for r in results if r.id == "instagram_liked_posts"), None)
        assert liked_posts is not None
        assert len(liked_posts.data_frame) == 0

    def test_empty_liked_comments(self):
        """Test that empty liked comments data doesn't crash"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/likes/liked_comments.json", json.dumps({"likes_comment_likes": []}))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)
        results = _run(zip_buffer)

        liked_comments = next((r for r in results if r.id == "instagram_liked_comments"), None)
        assert liked_comments is not None
        assert len(liked_comments.data_frame) == 0

    def test_missing_files(self):
        """Test that missing files don't crash extraction"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # Only create minimal required files, no saved/liked data
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)
        results = _run(zip_buffer)

        # Tables should still be created but empty
        saved_posts = next((r for r in results if r.id == "instagram_saved_posts"), None)
        liked_posts = next((r for r in results if r.id == "instagram_liked_posts"), None)
        liked_comments = next((r for r in results if r.id == "instagram_liked_comments"), None)

        assert saved_posts is not None
        assert liked_posts is not None
        assert liked_comments is not None


class TestSortingAndLimiting:
    """Test that data is sorted before limiting to MAX_TABLE_ROWS"""

    def test_saved_posts_sorted_newest_first(self):
        """Test that saved posts are sorted by date (newest first) before limiting"""
        base_date = datetime.now()

        # Create posts with specific timestamps - oldest first in input
        saved_posts_data = {
            "saved_saved_media": [
                {
                    "title": "oldest_post",
                    "string_map_data": {
                        "Saved on": {
                            "href": "https://www.instagram.com/p/OLD/",
                            "timestamp": int((base_date - timedelta(days=30)).timestamp())
                        }
                    }
                },
                {
                    "title": "middle_post",
                    "string_map_data": {
                        "Saved on": {
                            "href": "https://www.instagram.com/p/MID/",
                            "timestamp": int((base_date - timedelta(days=15)).timestamp())
                        }
                    }
                },
                {
                    "title": "newest_post",
                    "string_map_data": {
                        "Saved on": {
                            "href": "https://www.instagram.com/p/NEW/",
                            "timestamp": int((base_date - timedelta(days=1)).timestamp())
                        }
                    }
                },
            ]
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/saved/saved_posts.json", json.dumps(saved_posts_data))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)
        results = _run(zip_buffer)

        saved_posts = next((r for r in results if r.id == "instagram_saved_posts"), None)
        df = saved_posts.data_frame

        # Should be sorted newest first
        assert df.iloc[0]["Author"] == "newest_post", f"Expected newest_post first, got {df.iloc[0]['Author']}"
        assert df.iloc[1]["Author"] == "middle_post", f"Expected middle_post second, got {df.iloc[1]['Author']}"
        assert df.iloc[2]["Author"] == "oldest_post", f"Expected oldest_post last, got {df.iloc[2]['Author']}"

    def test_liked_posts_sorted_newest_first(self):
        """Test that liked posts are sorted by date (newest first)"""
        base_date = datetime.now()

        liked_posts_data = {
            "likes_media_likes": [
                {
                    "title": "oldest",
                    "string_list_data": [{"href": "https://instagram.com/p/1/", "timestamp": int((base_date - timedelta(days=100)).timestamp())}]
                },
                {
                    "title": "newest",
                    "string_list_data": [{"href": "https://instagram.com/p/2/", "timestamp": int((base_date - timedelta(days=1)).timestamp())}]
                },
                {
                    "title": "middle",
                    "string_list_data": [{"href": "https://instagram.com/p/3/", "timestamp": int((base_date - timedelta(days=50)).timestamp())}]
                },
            ]
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/likes/liked_posts.json", json.dumps(liked_posts_data))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)
        results = _run(zip_buffer)

        liked_posts = next((r for r in results if r.id == "instagram_liked_posts"), None)
        df = liked_posts.data_frame

        # Should be sorted newest first
        assert df.iloc[0]["Author"] == "newest", f"Expected newest first, got {df.iloc[0]['Author']}"
        assert df.iloc[1]["Author"] == "middle", f"Expected middle second, got {df.iloc[1]['Author']}"
        assert df.iloc[2]["Author"] == "oldest", f"Expected oldest last, got {df.iloc[2]['Author']}"

    def test_liked_comments_sorted_newest_first(self):
        """Test that liked comments are sorted by date (newest first)"""
        base_date = datetime.now()

        liked_comments_data = {
            "likes_comment_likes": [
                {
                    "title": "oldest",
                    "string_list_data": [{"href": "https://instagram.com/p/1/", "timestamp": int((base_date - timedelta(days=100)).timestamp())}]
                },
                {
                    "title": "newest",
                    "string_list_data": [{"href": "https://instagram.com/p/2/", "timestamp": int((base_date - timedelta(days=1)).timestamp())}]
                },
            ]
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/likes/liked_comments.json", json.dumps(liked_comments_data))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)
        results = _run(zip_buffer)

        liked_comments = next((r for r in results if r.id == "instagram_liked_comments"), None)
        df = liked_comments.data_frame

        # Should be sorted newest first
        assert df.iloc[0]["Author"] == "newest", f"Expected newest first, got {df.iloc[0]['Author']}"
        assert df.iloc[1]["Author"] == "oldest", f"Expected oldest last, got {df.iloc[1]['Author']}"


class TestMalformedData:
    """Test handling of malformed data that could cause crashes in new tables"""

    def test_malformed_timestamp_string_in_saved_posts(self):
        """Test that string timestamps don't crash saved posts extraction"""
        # Test saved_posts specifically - it uses safe_parse_datetime
        saved_posts_data = {
            "saved_saved_media": [
                {
                    "title": "valid_post",
                    "string_map_data": {
                        "Saved on": {
                            "href": "https://instagram.com/p/1/",
                            "timestamp": int(datetime.now().timestamp())
                        }
                    }
                },
                {
                    "title": "invalid_post",
                    "string_map_data": {
                        "Saved on": {
                            "href": "https://instagram.com/p/2/",
                            "timestamp": "not_a_timestamp"
                        }
                    }
                },
            ]
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/saved/saved_posts.json", json.dumps(saved_posts_data))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)

        with zipfile.ZipFile(zip_buffer) as zf:
            result = extract_saved_posts(zf)

        # Should have only the valid post, invalid one skipped
        assert result is not None
        assert len(result.data_frame) == 1
        assert result.data_frame.iloc[0]["Author"] == "valid_post"

    def test_negative_timestamp_in_liked_posts(self):
        """Test that negative timestamps don't crash liked posts extraction"""
        liked_posts_data = {
            "likes_media_likes": [
                {
                    "title": "valid_post",
                    "string_list_data": [{"href": "https://instagram.com/p/1/", "timestamp": int(datetime.now().timestamp())}]
                },
                {
                    "title": "negative_timestamp",
                    "string_list_data": [{"href": "https://instagram.com/p/2/", "timestamp": -9999999999}]
                },
            ]
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/likes/liked_posts.json", json.dumps(liked_posts_data))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)

        with zipfile.ZipFile(zip_buffer) as zf:
            result = extract_liked_posts(zf)

        # Should have only the valid post, invalid one skipped
        assert result is not None
        assert len(result.data_frame) == 1
        assert result.data_frame.iloc[0]["Author"] == "valid_post"

    def test_none_timestamp_in_liked_comments(self):
        """Test that None timestamps don't crash liked comments extraction"""
        liked_comments_data = {
            "likes_comment_likes": [
                {
                    "title": "valid_comment",
                    "string_list_data": [{"href": "https://instagram.com/p/1/", "timestamp": int(datetime.now().timestamp())}]
                },
                {
                    "title": "no_timestamp",
                    "string_list_data": [{"href": "https://instagram.com/p/2/"}]  # Missing timestamp
                },
            ]
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("instagram/likes/liked_comments.json", json.dumps(liked_comments_data))
            zf.writestr("instagram/content/posts_1.json", json.dumps([]))
            zf.writestr("instagram/content/stories.json", json.dumps({"ig_stories": []}))

        zip_buffer.seek(0)

        with zipfile.ZipFile(zip_buffer) as zf:
            result = extract_liked_comments(zf)

        # Should have only the valid comment, missing timestamp one skipped
        assert result is not None
        assert len(result.data_frame) == 1
        assert result.data_frame.iloc[0]["Author"] == "valid_comment"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
