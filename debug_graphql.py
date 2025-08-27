#!/usr/bin/env python3
"""
Debug Facebook GraphQL Response
Let's see exactly what Facebook returns and how to parse it properly
"""

import requests
import json
import sys
from datetime import datetime

def debug_facebook_response(keyword: str = "inwi.ma"):
    """
    Debug what Facebook GraphQL API actually returns
    """
    
    cookies = {
        'datr': 'u4MOaBz8cANjLPfdxB-kyrow',
        'sb': 'u4MOaKiWNS00Ub_bVCu0Kc2f',
        'ps_l': '1',
        'ps_n': '1',
        'c_user': '100007570923188',
        'b_user': '61559962276051',
        'locale': 'en_US',
        'pas': '100007570923188%3A0tD7VC74XY',
        'fbl_st': '101628247%3BT%3A29267760',
        'wl_cbv': 'v2%3Bclient_version%3A2902%3Btimestamp%3A1756065637',
        'dpr': '1',
        'wd': '1920x919',
        'ar_debug': '1',
        'fr': '1yicHj3sck1c8Y88b.AWdt42sk1ovov4veHzQyixVUS8o9dqyBnabJiOABBR2kPrE5oJA.BorixF..AAA.0.0.BorixF.AWdDJriyAIAAmh6FjqiLVh-n-Zs',
        'xs': '39%3AHedndidVURnKpw%3A2%3A1746745261%3A-1%3A-1%3AhpgzruHmnkIPDA%3AAcXHkHSM908HEl3N5boOsl8UqwsKXWqiCBAXhf5hvfds',
        'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1756245102703%2C%22v%22%3A1%7D',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ar;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'referer': f'https://www.facebook.com/search/posts?q={keyword}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'SearchCometResultsPaginatedResultsQuery',
        'x-fb-lsd': 'vLhMaN7xuRiuDe_Nydjw6X',
    }

    # Simplified data for debugging
    data = {
        'av': '100007570923188',
        '__user': '100007570923188',
        '__a': '1',
        '__req': '1',
        '__hs': '20326.HYP:comet_pkg.2.1...0',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1026338653',
        '__comet_req': '15',
        'fb_dtsg': 'NAfsC--IVdRQAbezpRZYxfOtlFELNplwlYHtscNqWlFd6oFCgX57w0g:39:1746745261',
        'jazoest': '25628',
        'lsd': 'vLhMaN7xuRiuDe_Nydjw6X',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'SearchCometResultsPaginatedResultsQuery',
        'server_timestamps': 'true',
        'doc_id': '24190416707327186',
        'variables': json.dumps({
            "allow_streaming": False,
            "args": {
                "callsite": "COMET_GLOBAL_SEARCH",
                "config": {"exact_match": False},
                "context": {"bsid": "test", "tsid": None},
                "experience": {"type": "POSTS_TAB"},
                "filters": ["{\"name\":\"recent_posts\",\"args\":\"\"}"],
                "text": keyword
            },
            "count": 5,
            "feedLocation": "SEARCH",
            "renderLocation": "search_results_page",
            "scale": 1
        })
    }

    print(f"🔍 Debugging Facebook GraphQL response for: '{keyword}'")
    print("=" * 60)

    try:
        response = requests.post(
            'https://www.facebook.com/api/graphql/',
            cookies=cookies,
            headers=headers,
            data=data,
            timeout=30
        )

        print(f"📊 Response Status: {response.status_code}")
        print(f"📏 Response Length: {len(response.text)} characters")
        print(f"📋 Response Headers: {dict(response.headers)}")

        # Save raw response for analysis
        with open('facebook_raw_response.txt', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("💾 Raw response saved to: facebook_raw_response.txt")

        # Try to identify the JSON structure
        print("\n🔍 ANALYZING RESPONSE STRUCTURE:")
        print("=" * 60)

        text = response.text
        
        # Check if response starts with "for (;;);"
        if text.startswith('for (;;);'):
            print("✅ Found 'for (;;);' prefix - this is normal Facebook response format")
            json_text = text[9:]  # Remove the prefix
        else:
            json_text = text

        # Look for multiple JSON objects
        json_objects = []
        remaining_text = json_text
        
        while remaining_text.strip():
            try:
                # Try to parse a JSON object
                obj, idx = json.JSONDecoder().raw_decode(remaining_text)
                json_objects.append(obj)
                remaining_text = remaining_text[idx:].strip()
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing stopped at: {e}")
                break

        print(f"📊 Found {len(json_objects)} JSON objects in response")

        # Analyze each JSON object
        for i, obj in enumerate(json_objects):
            print(f"\n🔸 JSON Object {i+1}:")
            print(f"   Type: {type(obj)}")
            
            if isinstance(obj, dict):
                print(f"   Keys: {list(obj.keys())}")
                
                # Look for data structure
                if 'data' in obj:
                    print(f"   Has 'data' key: {type(obj['data'])}")
                    if isinstance(obj['data'], dict):
                        print(f"   Data keys: {list(obj['data'].keys())}")
                        
                        # Look for serpResponse
                        if 'serpResponse' in obj['data']:
                            serp = obj['data']['serpResponse']
                            print(f"   serpResponse type: {type(serp)}")
                            if isinstance(serp, dict):
                                print(f"   serpResponse keys: {list(serp.keys())}")
                                
                                # Look for results
                                if 'results' in serp:
                                    results = serp['results']
                                    print(f"   results type: {type(results)}")
                                    if isinstance(results, dict):
                                        print(f"   results keys: {list(results.keys())}")
                                        
                                        # Look for edges
                                        if 'edges' in results:
                                            edges = results['edges']
                                            print(f"   edges count: {len(edges) if isinstance(edges, list) else 'not a list'}")
                                            
                                            if isinstance(edges, list) and edges:
                                                print(f"   First edge keys: {list(edges[0].keys()) if isinstance(edges[0], dict) else 'not a dict'}")

        # Try to extract posts if found
        print(f"\n🎯 ATTEMPTING TO EXTRACT POSTS:")
        print("=" * 60)

        posts_found = 0
        for obj in json_objects:
            if isinstance(obj, dict) and 'data' in obj:
                posts_found += extract_posts_from_object(obj, keyword)

        print(f"📊 Total posts extracted: {posts_found}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def extract_posts_from_object(obj, keyword):
    """Try to extract posts from a JSON object"""
    posts_found = 0
    
    try:
        # Navigate to posts
        data = obj.get('data', {})
        serp_response = data.get('serpResponse', {})
        results = serp_response.get('results', {})
        edges = results.get('edges', [])
        
        print(f"🔍 Found {len(edges)} edges to process")
        
        for i, edge in enumerate(edges):
            if isinstance(edge, dict) and 'node' in edge:
                node = edge['node']
                print(f"\n📝 Processing edge {i+1}:")
                print(f"   Node type: {type(node)}")
                
                if isinstance(node, dict):
                    print(f"   Node keys: {list(node.keys())}")
                    
                    # Look for text content
                    text_content = find_text_in_node(node)
                    author_info = find_author_in_node(node) 
                    post_id = node.get('post_id', node.get('id', 'unknown'))
                    
                    if text_content or author_info:
                        posts_found += 1
                        print(f"   ✅ Post {posts_found}:")
                        print(f"      Text: {text_content[:100] if text_content else 'No text'}...")
                        print(f"      Author: {author_info}")
                        print(f"      Post ID: {post_id}")
        
    except Exception as e:
        print(f"❌ Error extracting posts: {e}")
    
    return posts_found

def find_text_in_node(node, path=""):
    """Recursively find text content in a node"""
    if isinstance(node, dict):
        # Check common text fields
        text_fields = ['text', 'message', 'content', 'body']
        for field in text_fields:
            if field in node and isinstance(node[field], str) and node[field].strip():
                return node[field]
        
        # Recursively search in nested objects
        for key, value in node.items():
            result = find_text_in_node(value, f"{path}.{key}")
            if result:
                return result
    
    elif isinstance(node, list):
        for i, item in enumerate(node):
            result = find_text_in_node(item, f"{path}[{i}]")
            if result:
                return result
    
    return None

def find_author_in_node(node, path=""):
    """Recursively find author information in a node"""
    if isinstance(node, dict):
        # Check common author fields
        author_fields = ['name', 'author', 'username', 'actor']
        for field in author_fields:
            if field in node and isinstance(node[field], str) and node[field].strip():
                return node[field]
        
        # Look for nested author info
        if 'actors' in node and isinstance(node['actors'], list) and node['actors']:
            first_actor = node['actors'][0]
            if isinstance(first_actor, dict) and 'name' in first_actor:
                return first_actor['name']
        
        # Recursively search in nested objects (but limit depth)
        if len(path.split('.')) < 5:  # Limit recursion depth
            for key, value in node.items():
                if key in ['actor', 'user', 'author', 'profile']:
                    result = find_author_in_node(value, f"{path}.{key}")
                    if result:
                        return result
    
    return None

if __name__ == "__main__":
    debug_facebook_response("inwi.ma")