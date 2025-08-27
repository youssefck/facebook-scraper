#!/usr/bin/env python3
"""
Debug Facebook Search - Check what's happening
"""

import sys
sys.path.insert(0, '/workspace')

# Your cookies
COOKIES = {
    'datr': 'T5AiZ8l6hbmh1Qh3OTE-_vSf',
    'sb': 'T5AiZ5UyDKV9wbgl_mBw6y2R', 
    'ps_l': '1',
    'ps_n': '1',
    'dpr': '1.5',
    'c_user': '100003651255170',
    'xs': '23%3Akb3jl3EgjW-ZgQ%3A2%3A1756137972%3A-1%3A-1',
    'fr': '1cGoymFMkpiDiRWmt.AWeCaO07KIrhu3-_A6UMmA0ayiK7iA62oRnN00-QKovpGuJy8Uc.Boqfzc..AAA.0.0.BorIn2.AWdH_UghHdnTh16TQ4il46lpePE',
    'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1756138038008%2C%22v%22%3A1%7D',
    'wd': '1920x326',
}

def test_basic_import():
    print("🧪 Testing basic imports...")
    try:
        from facebook_scraper import get_posts_by_search
        print("✅ facebook_scraper imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_simple_search():
    print("\n🧪 Testing simple search without authentication...")
    try:
        from facebook_scraper import get_posts_by_search
        
        # Try a very simple search with minimal options
        print("🔍 Searching for 'test' keyword...")
        
        post_count = 0
        for post in get_posts_by_search("test", pages=1):
            post_count += 1
            print(f"Found post {post_count}: {post.get('text', '')[:50]}...")
            if post_count >= 2:  # Just get a couple of posts
                break
        
        print(f"✅ Simple search worked - found {post_count} posts")
        return True
        
    except Exception as e:
        print(f"❌ Simple search failed: {e}")
        return False

def test_cookies_search():
    print("\n🧪 Testing search with your cookies...")
    try:
        from facebook_scraper import get_posts_by_search
        
        print("🔍 Searching for 'inwi.ma' with authentication...")
        
        post_count = 0
        try:
            for post in get_posts_by_search("inwi.ma", cookies=COOKIES, pages=1):
                post_count += 1
                print(f"✅ Found post {post_count}:")
                print(f"   Author: {post.get('username', 'Unknown')}")
                print(f"   Text: {post.get('text', '')[:100]}...")
                print(f"   URL: {post.get('post_url', 'N/A')}")
                print(f"   Likes: {post.get('likes', 0)}")
                
                if post_count >= 3:  # Get first 3 posts
                    break
        
        except Exception as search_error:
            print(f"❌ Search with cookies failed: {search_error}")
            
            # Try alternative approach
            print("\n🔄 Trying alternative search approach...")
            try:
                # Try searching for a more common term
                for post in get_posts_by_search("morocco", cookies=COOKIES, pages=1):
                    post_count += 1
                    print(f"✅ Alternative search found post {post_count}")
                    if post_count >= 1:
                        break
            except Exception as alt_error:
                print(f"❌ Alternative search also failed: {alt_error}")
        
        if post_count > 0:
            print(f"✅ Authenticated search worked - found {post_count} posts")
            return True
        else:
            print("❌ No posts found with authenticated search")
            return False
            
    except Exception as e:
        print(f"❌ Authenticated search setup failed: {e}")
        return False

def main():
    print("🚀 Facebook Scraper Debug Test")
    print("=" * 50)
    
    success_count = 0
    
    # Test 1: Basic imports
    if test_basic_import():
        success_count += 1
    
    # Test 2: Simple search
    if test_simple_search():
        success_count += 1
    
    # Test 3: Authenticated search
    if test_cookies_search():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {success_count}/3 tests passed")
    
    if success_count == 3:
        print("✅ All tests passed! The scraper should work.")
    elif success_count >= 1:
        print("⚠️  Partial success - some features working.")
    else:
        print("❌ All tests failed - there are issues with the setup.")

if __name__ == "__main__":
    main()