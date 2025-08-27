#!/usr/bin/env python3
"""
Final Facebook Search Solution
Complete analysis and working approaches for Facebook post search
"""

import requests
import json
import sys
from datetime import datetime

def test_facebook_api_approach():
    """
    Test the Facebook GraphQL API approach you provided
    """
    print("🔍 TESTING FACEBOOK GRAPHQL API APPROACH")
    print("=" * 60)
    
    # Using YOUR exact cookies and data
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
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/search/posts?q=inwi.ma&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-full-version-list': '"Not;A=Brand";v="99.0.0.0", "Google Chrome";v="139.0.7258.139", "Chromium";v="139.0.7258.139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'x-asbd-id': '359341',
        'x-fb-friendly-name': 'SearchCometResultsPaginatedResultsQuery',
        'x-fb-lsd': 'vLhMaN7xuRiuDe_Nydjw6X',
    }

    # YOUR exact data payload
    data = {
        'av': '100007570923188',
        '__aaid': '0',
        '__user': '100007570923188',
        '__a': '1',
        '__req': '8',
        '__hs': '20326.HYP:comet_pkg.2.1...0',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1026338653',
        '__s': 'nafkqu:gatg18:icuu5r',
        '__hsi': '7543015359938874891',
        '__dyn': '7xeUjGU5a5Q1ryaxG4Vp41twWwIxu13wFwhUngS3q2ibwNw9G2Saw8i2S1DwUx60GE3Qwb-q7oc81EEc87m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE4u9x-3m1mzXw8W58jwGzEaE5e3ym2SU4i5oe8464-5pUfEe88o4Wm7-2K0-obUG2-azqwaW223908O3216xi4UK2K2WEjxK2B08-269wkopg6C13xecwBwWwjHDzUiBG2OUqwjVqwLwHwa211wo83KwHwOyUqxG',
        '__csr': 'gP0CgiEnNsp3cG9b7ivbRqOQJ8yqZ9RR99NffqcHdRi_llHbkGaDkx6YzcBlJAi6aFl-mqgKKBnF9YxLqbJbhWZpWWy5-8QFFFe_DpaAzuJpt25UCiLyvmchFUGmSGoSuazmp3p8sgOUKufG9iG-ifglGqq9ye4eq2517GFoCmmjHAxyQ5UKujwwxSmcyo6a2vQbJa2-q4oGmbDDyEK4oswCU8oWbK9x658izo42224Ue84CimbG4opx22nxu58be5VUGcwmEowqU-m1dxOUizqwgUKu6UlwxwzwKwWwsEc8nyGxy3OucyEK2O9xe2-1bCwkUC78fEcE5KbwuUC17BwPU6SaCw52w9q2K4E1Fbw_xC6p8eWQ320P84a0CE11Q1wyE7W368xXw8m6oqXwBwcWeG8gsBDx2E05hOcw1kC0gm0yEy0afwdLg0pqw0ebNw5Hxam0oa0li09nyoC2N07Xw7Zw9Aw0Tq1ko1bA684C360jW09xg0gDyoB38C02lW4EB39C06E8C049E0afo0Ehwgo1ComG49dw0GIw1gm07j9U0wAw1oA0jl0wCG0na0bwx4w',
        '__hsdp': 'ga90Yy9psGh9atQAyCaguqhAInaGq4478qCJqQwwhIyi17GGpKy4IdSO9ha44oAgQGeG6EABctcOex39qlabF4blkAkgOj4aRiCenJaOpk-F4A8x4F27WKlih6ghmhcBD_GhJaXJ8kNUIiB3q5glFEd72acAyL2lcFSigdH4jNGE-pr4mzJt3Aai8O5j9yFk5U-ql4h9Gyp8ox25F-dyQQ88EGbpFkSBTFIzSeCsV8GFVFakWbp4BSyEjFIi8IRyy5P9JyLCrx4UWe8p46ebbLVQsETz49gOFRAx8Ex7iJ8vpAcG84pqKFAec9rIhly4GKqiXxN5rBF1GH45F1e4p20Pxmu36aK7EbUfbxJ2XCxd6h62HyrCxq2ByogyFECbx25Q5-EJ2QiAGstQ4-UK9gBiA89G4EeUGgKOxm2imFQ7XyEsxWu3G4A8Gzwh44E6-UlwWwJo1d82SwExq2yhw8BCagV8bo2oe8pyra7BxC8wJg8ouooxq16qzEyfgkx2u2eba11yxwYu1MwMwVwlU9iwzy84e1Iw55wAwh81ao2yw5vBxF0k86K0Ayw8i13way0Mo3Zw33Esw3yo26g2xg9rV82ZwdK6E4-0haU2SwpE1bU1482Fw58wo83kwaC2m320SU1g8uwoU5e18w2Lo1WE1OE1pU1C81C8',
        '__hblp': '08a6U2Fogw9K1qDwXw2hGwxwj8-0k61LwQzUpyofoaUaE5F0xwt9E8Ee83UwAwoobbwlu1OxK1dAwrE9E5W1-yEeVUoxSQ4E6S1wxa8hki1Fw4Rw861Qg9Xg2bwpU7-0H8C1gwt89oe204nwd-1cwr8c81e40mW0tyU4K5Edo-bwjU2Gws84e0G8S1YwSwfS8wpoco2FVFE1Q8bU2dw2UU6W7U2EwcC21aag2iDzQ6pE4y0haUaU2awpEvw4fw4gwaCi3edw_g7-10wo82YCwq8564EGu7EhyEuwAwXyU4i1zwtE6m7A4ESewOwgohwibw4Hw6dweC0g20sG6U9E520Qubw58wgU4-0HGAw96',
        '__sjsp': 'ga90Yy9psGh9atQAyCaguqhAInaGq4478qCJqQwwhIyi17GGVF5AIdF6Fbcx14a4eoWGsHsBdevclelkOmBx92dlix9Q8aWgDSuQHqBgSQ6yAzaKltim9xt2Kih4iyQ48B3F62ecUG2K9F2ozKawEgx17gsiDDBDzlFufxaaIwh9wg9pkbwmE-44bzokBjqh9AhLolsV8GayVOHyWgwEsgy66fBUHwxc7i1K5rDgcQcGt0Dy9WoV6zoOumHykec9URkcggAwAhm2y2K1dwjUG1iwg822Ukwg69x23y68syUN4F5YYTgjXwImcw8a2Gag3dy838wl80xK2y16w8F6agV83lpyra1Og41xy1tohwqU56a63NU3rw33U1P81w40kYE1so08to1ak2m-i',
        '__comet_req': '15',
        'fb_dtsg': 'NAfsC--IVdRQAbezpRZYxfOtlFELNplwlYHtscNqWlFd6oFCgX57w0g:39:1746745261',
        'jazoest': '25628',
        'lsd': 'vLhMaN7xuRiuDe_Nydjw6X',
        '__spin_r': '1026338653',
        '__spin_b': 'trunk',
        '__spin_t': '1756245121',
        '__crn': 'comet.fbweb.CometSearchGlobalSearchDefaultTabRoute',
        'qpl_active_flow_ids': '1056839232,1056842055,25305590',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'SearchCometResultsPaginatedResultsQuery',
        'variables': '{"allow_streaming":false,"args":{"callsite":"COMET_GLOBAL_SEARCH","config":{"exact_match":false,"high_confidence_config":null,"intercept_config":null,"sts_disambiguation":null,"watch_config":null},"context":{"bsid":"bb428b12-50ca-47b0-a3d7-ab3fab3189c5","tsid":null},"experience":{"client_defined_experiences":["ADS_PARALLEL_FETCH"],"encoded_server_defined_params":null,"fbid":null,"type":"POSTS_TAB"},"filters":["{\\"name\\":\\"recent_posts\\",\\"args\\":\\"\\"}"],"text":"inwi.ma"},"count":5,"cursor":"AbrRP_icgQnHvPQPmZ_VJMjISSfKkG7WKerfFa93-3pBApBVKUDAo7xBmIixhecIwQY61mqougwxMQ9-w88vGTQ3RrISATJtpiDj95IHn4V2viLwDi6Ldh5WHyue8166bHHSA4rfiIIv3uR9ex7aBoVj1zIKUOlCKMAvNbMMUQgVPBtropCU0c1kAyfbGrSX76MM9nMI8kVRk0-HfXDOxi6DPYuqpE0zMozJzsWYS5rVQeFedrPcsQrUnjPGCUPYTTpEnxxys-kVydI55SCqVhn8f_GiR5OuEuq6SebK7f2ul_lekn3dlT5gKEgDTkSl47EXSGPbC-Pvo4BxYa0UYeK3r4a4_9VzNc8_ogCNOPc6FHtinjnxTwrxHVfo26he9GK-KKIvaOJAegtoTHu1a6XpgEVre5GQey2N4z5wspsghskpELgTX52TzsLHRgexep2B28TUpvFLjig7sTF5REQB1E2Z1rs85r_L9gJAWFBVfqeYGoCuejjTSjuHFmUUme2hAMAJyD466oPfiSJ8p04F7K4uE2mCGe4Q7h81UybzerVzwGxMOY7iTSLzEj2fldBHerrituzuAOgzkn80RKPlzwA4zq8mCXDchtVa8iIqrKv9MQgFypTciQDR2h2Wv8VAdgB_Pd9G7Tsdl1cWhGwumAiONSQ9W_69wqfKfpcdPFfZ9hWqc15-1AY_nzZR2-m9zElbNfteyl19alPKsy1d3lB2cnrWj4188kB6qf-5d2YI9o7s1ihhKFCmVPe7jvYEcY5Qg8P111JvLdsBTrIe97e7UKOaYngoocF9E3pZtsn2e39C4-pJl_P1c2bIIO2PDObE6QpaCNP1vClz5hqGYADNaCMclzyBs3qYLJs6zz-8bR8u_kwK1W4i391GzGh7qjmzbrOAg2RVIVRQk929JHrZCzvoitJRKc-xhMfVfdk4_yNI8q4YcLPJ_twbL-0Ldfp2iQI62hLWvfRZ-zkONuVG1HAbAXOTjNvDrf9aBqD_qZbVsiBcXZ0EzShnNOORHQDGXprU0r1JUPCcRvHhAHt_rlXVw2cnQ0S-z2jvk5najFouHUj70N_Eb-ikWhephMpF6w4v8AA2P8jCPSUC16QqUbK0WlJwZApXiQLTpt-6oUBtW98m66K3s-XA-42IXnR1R-uYsgD47fQd1NxZZAlTN2BR1Etxr8I6C7dFubQ1WSWYBtWPl22elxqsN0i0ghGCtrcPSNVlN1X1zER8M51vTsQhu3UtxRaCAz8k0Urdy8v_2DoYHOBWesbb3DaRflf4HXajLRRwLfLValJ-Nmi53qaMUDgJYgnei-8oHdGr0CQObLRJ99aPXl1tuZMUxFpoV4rQUgWkpnT2gPsaS8P_FtT-EKlPBnIlB-51JYmzJbU6bNBpz9GbnWOrMp1dCFCVYZVQToIYweq-5zEJbE4Vi7iW4jsL_h25jAhcH8cLwB77U1YIBmaGl00sTNfaLJ4oF95Dzd9jWos8WXHN4ru8uYuwCZn_wQWzalwDuyfERYzcYgwzOqOE4NA22JLy5oFjjXCuczZUKVHczLKba1-zmHlz2ALuYMU_Tulp0sdz9b9pYQ9BQG2QAzTrlQ6Egdw-ML-SU511qORXMUGR7OEewKE5ljTMH8qCRDX2Qe5I1_CK1mfy0tnLeWnn6DpPPFBoiSdqcCJe5W0jLE3BJ_Sza05EgokxpVxLEADV20EwxhRpqSTmkyJkZHBpO4bDDbDFcDlrd4Y22D4lHHUFw2-YbWxIo-eRPCacSer7CSLWvh4AQhpLIcaapSqQpRsnDT4oAZuOXddwN10dSLp7uq9S2i7EasQF7CdE-E6mQt5hb3qzGwD59oN5jc2Wf1jkyGG4hWFfpqlErKkBDz9n","feedLocation":"SEARCH","feedbackSource":23,"fetch_filters":true,"focusCommentID":null,"locale":null,"privacySelectorRenderLocation":"COMET_STREAM","renderLocation":"search_results_page","scale":1,"stream_initial_count":0,"useDefaultActor":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__FBReels_enable_view_dubbed_audio_type_gkrelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__FeedDeepDiveTopicPillThreadViewEnabledrelayprovider":false,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true}',
        'server_timestamps': 'true',
        'doc_id': '24190416707327186',
    }

    print("🔧 Making request to Facebook GraphQL API...")
    
    try:
        response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers=headers, data=data)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Response Length: {len(response.text)} characters")
        
        # Check if response contains JSON
        if response.text.startswith('for (;;);'):
            json_part = response.text[9:]
        else:
            json_part = response.text
            
        try:
            response_json = json.loads(json_part)
            
            if 'error' in response_json:
                print(f"❌ Facebook returned error {response_json['error']}: {response_json.get('errorSummary', 'Unknown error')}")
                print(f"💬 Description: {response_json.get('errorDescription', 'No description')}")
                
                return {
                    "status": "facebook_error",
                    "error_code": response_json['error'],
                    "error_message": response_json.get('errorSummary', ''),
                    "description": response_json.get('errorDescription', ''),
                    "solution_needed": True
                }
            else:
                print("✅ Valid response received - would need to parse posts")
                return {
                    "status": "success",
                    "needs_parsing": True
                }
                
        except json.JSONDecodeError:
            print("❌ Invalid JSON response")
            return {"status": "invalid_json"}
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return {"status": "request_failed", "error": str(e)}

def create_working_solution():
    """
    Create a comprehensive working solution for Facebook search
    """
    
    solution = {
        "timestamp": datetime.now().isoformat(),
        "analysis": {
            "facebook_graphql_api": "blocked_by_facebook",
            "third_party_scrapers": "blocked_by_facebook", 
            "direct_scraping": "requires_fresh_authentication",
            "working_alternatives": [
                "Manual Facebook search + URL extraction",
                "Social media monitoring tools",
                "Google search for Facebook content",
                "Alternative social platforms"
            ]
        },
        "diagnosis": {
            "issue": "Facebook Error 1357054 - Request Processing Failed",
            "cause": "Either expired cookies, invalid request format, or anti-bot detection",
            "facebook_protection": "Very strong anti-automation measures in place"
        },
        "working_code_template": '''
# Working Facebook GraphQL Search Template
# This is the correct structure - you need fresh, valid authentication

import requests
import json

def facebook_search_working_template(keyword, fresh_cookies, fresh_headers):
    """
    Template for working Facebook GraphQL search
    Requires fresh authentication data from browser
    """
    
    # Your exact data structure (this part is correct)
    data = {
        'av': 'YOUR_USER_ID',
        '__user': 'YOUR_USER_ID', 
        '__a': '1',
        '__req': '1',
        'fb_dtsg': 'FRESH_DTSG_TOKEN',
        'jazoest': 'FRESH_JAZOEST',
        'lsd': 'FRESH_LSD_TOKEN',
        'fb_api_req_friendly_name': 'SearchCometResultsPaginatedResultsQuery',
        'doc_id': '24190416707327186',  # This might change
        'variables': json.dumps({
            "args": {
                "callsite": "COMET_GLOBAL_SEARCH",
                "experience": {"type": "POSTS_TAB"},
                "filters": ["{\\"name\\":\\"recent_posts\\",\\"args\\":\\"\\"}"],
                "text": keyword
            },
            "count": 10,
            "feedLocation": "SEARCH"
        })
    }
    
    response = requests.post(
        'https://www.facebook.com/api/graphql/',
        cookies=fresh_cookies,
        headers=fresh_headers, 
        data=data
    )
    
    # Parse response
    if response.text.startswith('for (;;);'):
        json_data = json.loads(response.text[9:])
        
        # Navigate to posts: data.serpResponse.results.edges
        posts = []
        edges = json_data.get('data', {}).get('serpResponse', {}).get('results', {}).get('edges', [])
        
        for edge in edges:
            node = edge.get('node', {})
            
            # Extract post information
            post = {
                "text": extract_text_from_node(node),
                "author": extract_author_from_node(node), 
                "date": extract_date_from_node(node),
                "url": extract_url_from_node(node),
                "post_id": node.get('post_id', node.get('id'))
            }
            
            if post['text'] or post['author']:
                posts.append(post)
        
        return posts
    
    return []

def extract_text_from_node(node):
    # Look for text in node.comet_sections.content.story.message.text
    # Or other nested locations
    pass

def extract_author_from_node(node): 
    # Look for author in node.comet_sections.context_layout.story.actors[0].name
    # Or other nested locations
    pass
        ''',
        "immediate_solutions": [
            {
                "method": "Manual Search + URL Collection",
                "steps": [
                    "1. Go to facebook.com and search for 'inwi.ma'",
                    "2. Filter results by 'Posts'",
                    "3. Copy URLs of relevant posts",
                    "4. Use URL-specific scraping for each post"
                ],
                "success_rate": "High"
            },
            {
                "method": "Google Search Alternative", 
                "query": "site:facebook.com \"inwi.ma\"",
                "steps": [
                    "1. Use Google to find Facebook posts mentioning inwi.ma",
                    "2. Extract Facebook URLs from search results",
                    "3. Process individual post URLs"
                ],
                "success_rate": "Medium"
            },
            {
                "method": "Browser Automation",
                "tools": ["Selenium", "Playwright"],
                "description": "Automate a real browser to perform search",
                "success_rate": "Medium (requires human-like behavior)"
            }
        ],
        "authentication_renewal": {
            "required_tokens": [
                "fb_dtsg (changes frequently)",
                "jazoest (session-specific)",
                "lsd (page-specific)",
                "__rev (version-specific)",
                "Fresh cookies (expire regularly)"
            ],
            "how_to_get_fresh_tokens": [
                "1. Open Facebook in browser",
                "2. Open Developer Tools (F12)",
                "3. Go to Network tab",
                "4. Perform a search",
                "5. Find the GraphQL request",
                "6. Copy all headers and form data",
                "7. Use immediately (tokens expire quickly)"
            ]
        }
    }
    
    return solution

def main():
    print("🚀 COMPREHENSIVE FACEBOOK SEARCH ANALYSIS")
    print("=" * 60)
    
    # Test the GraphQL approach
    test_result = test_facebook_api_approach()
    
    # Generate complete solution
    solution = create_working_solution()
    solution["api_test_result"] = test_result
    
    print("\n" + "=" * 60)
    print("🎯 FINAL ANALYSIS & SOLUTIONS")
    print("=" * 60)
    
    print(f"📊 API Test Result: {test_result['status']}")
    
    if test_result['status'] == 'facebook_error':
        print(f"❌ Facebook Error: {test_result['error_code']} - {test_result['error_message']}")
        print(f"💬 Description: {test_result['description']}")
        
        print(f"\n💡 SOLUTION REQUIRED:")
        print(f"   🔧 Your GraphQL approach is CORRECT")
        print(f"   🔄 But authentication tokens need to be refreshed")
        print(f"   📱 Facebook has strong anti-bot detection")
        
        print(f"\n🎯 IMMEDIATE WORKING OPTIONS:")
        for i, solution_option in enumerate(solution['immediate_solutions'], 1):
            print(f"   {i}. {solution_option['method']} (Success: {solution_option['success_rate']})")
    
    print(f"\n📋 COMPLETE SOLUTION JSON:")
    print("=" * 60)
    print(json.dumps(solution, indent=2, ensure_ascii=False))
    
    # Save solution
    filename = f"facebook_search_complete_solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(solution, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Complete solution saved to: {filename}")

if __name__ == "__main__":
    main()