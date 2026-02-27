import requests
import json
import pandas as pd
import sqlite3
import os
import time

def scrape_airbnb_seoul(max_pages=None):
    url = "https://www.airbnb.co.kr/api/v3/StaysSearch/b29e3db8a086be4ef27ee0f2bd7ee3bbfa09cc2b84a214d5e254103078a4efa2?operationName=StaysSearch&locale=ko&currency=KRW"
    
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "x-airbnb-api-key": "d306zoyjsyarp7ifhu67rjxn52tv0t20",
        "x-airbnb-graphql-platform": "web",
        "x-airbnb-graphql-platform-client": "minimalist-niobe",
        "referer": "https://www.airbnb.co.kr/s/%EC%84%9C%EC%9A%B8/homes",
        "cookie": "_user_attributes=%7B%22curr%22%3A%22KRW%22%7D; bev=1771936728_EAZTdmMWI3MTI1Zm; everest_cookie=1771936728.EAZGYwZjU1NWUxMmM2Nm.PEStc-Q8ndAeyh9ohGZElQATevgxT4CvJMG1uTKBVI4; ak_bmsc=8737165E850163E566269A2F81742979~000000000000000000000000000000~YAAQ0zpvPT4qFYKcAQAASMeojx7vLiH1ZDskiRaYw/JqNjsYBl59/kKmxlZhCd6TgeLTASljKORHpY41TfH7jud+sOz4nCcZPpfkIixnH71pw2KvSU5DsuPQbVSLy+wIr7Rcz1SfO9HrGQ1SX7Tys44Y9r0o+Qff5Q9R5LkGhtVdjMoEZ29P2eJGcvqQFpzyEpKrderGaYeNuLzQHdi/Pie+Np10SZFmUYsLomJC/29LcF3+xldrrO7VqXfEBazgiHUHmhLT12N4Yi30koyWyOFUNC7racJFBLHN79aDtf4RbiqO0+wOmCU3zA3WegAc/3rUZ5oJ6BCq72lJYsWofA5FxxyhDTvYIo2S5xhzcE6X6PK83wLQJHGCIq0XMTny3y2ZKpHK1IgBWeT3MaA=;",
        "x-csrf-token": "1",
        "x-csrf-without-token": "1",
    }

    all_data = []
    current_cursor = "eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjoxOCwidmVyc2lvbiI6MX0="  # 초기 커서 (18개 이후부터)
    page = 1

    while True:
        if max_pages and page > max_pages:
            break
            
        print(f"{page} 페이지 수집 중... (Cursor: {current_cursor})")
        
        payload = {
            "operationName": "StaysSearch",
            "variables": {
                "staysSearchRequest": {
                    "cursor": current_cursor,
                    "metadataOnly": False,
                    "requestedPageType": "STAYS_SEARCH",
                    "treatmentFlags": [
                        "feed_map_decouple_m11_treatment", "recommended_amenities_2024_treatment_b",
                        "filter_redesign_2024_treatment", "filter_reordering_2024_roomtype_treatment",
                        "p2_category_bar_removal_treatment", "selected_filters_2024_treatment",
                        "recommended_filters_2024_treatment_b", "m13_search_input_phase2_treatment",
                        "m13_search_input_services_enabled", "m13_2025_experiences_p2_treatment"
                    ],
                    "maxMapItems": 9999,
                    "rawParams": [
                        {"filterName": "acpId", "filterValues": ["0678003c-2a0a-47a0-97a5-b7cd68d4b09a"]},
                        {"filterName": "cdnCacheSafe", "filterValues": ["false"]},
                        {"filterName": "channel", "filterValues": ["EXPLORE"]},
                        {"filterName": "datePickerType", "filterValues": ["flexible_dates"]},
                        {"filterName": "federatedSearchSessionId", "filterValues": ["5313b965-9177-4ddf-8f7e-1cbab1546071"]},
                        {"filterName": "flexibleTripLengths", "filterValues": ["one_week"]},
                        {"filterName": "itemsPerGrid", "filterValues": ["18"]},
                        {"filterName": "monthlyEndDate", "filterValues": ["2026-06-01"]},
                        {"filterName": "monthlyLength", "filterValues": ["3"]},
                        {"filterName": "monthlyStartDate", "filterValues": ["2026-03-01"]},
                        {"filterName": "placeId", "filterValues": ["ChIJzzlcLQGifDURm_JbQKHsEX4"]},
                        {"filterName": "priceFilterInputType", "filterValues": ["2"]},
                        {"filterName": "query", "filterValues": ["서울"]},
                        {"filterName": "refinementPaths", "filterValues": ["/homes"]},
                        {"filterName": "screenSize", "filterValues": ["large"]},
                        {"filterName": "tabId", "filterValues": ["home_tab"]},
                        {"filterName": "version", "filterValues": ["1.8.8"]}
                    ]
                },
                "staysMapSearchRequestV2": {
                    "cursor": current_cursor,
                    "metadataOnly": False,
                    "requestedPageType": "STAYS_SEARCH",
                    "treatmentFlags": [
                        "feed_map_decouple_m11_treatment", "recommended_amenities_2024_treatment_b",
                        "filter_redesign_2024_treatment", "filter_reordering_2024_roomtype_treatment",
                        "p2_category_bar_removal_treatment", "selected_filters_2024_treatment",
                        "recommended_filters_2024_treatment_b", "m13_search_input_phase2_treatment",
                        "m13_search_input_services_enabled", "m13_2025_experiences_p2_treatment"
                    ],
                    "rawParams": [
                        {"filterName": "acpId", "filterValues": ["0678003c-2a0a-47a0-97a5-b7cd68d4b09a"]},
                        {"filterName": "cdnCacheSafe", "filterValues": ["false"]},
                        {"filterName": "channel", "filterValues": ["EXPLORE"]},
                        {"filterName": "datePickerType", "filterValues": ["flexible_dates"]},
                        {"filterName": "federatedSearchSessionId", "filterValues": ["5313b965-9177-4ddf-8f7e-1cbab1546071"]},
                        {"filterName": "flexibleTripLengths", "filterValues": ["one_week"]},
                        {"filterName": "monthlyEndDate", "filterValues": ["2026-06-01"]},
                        {"filterName": "monthlyLength", "filterValues": ["3"]},
                        {"filterName": "monthlyStartDate", "filterValues": ["2026-03-01"]},
                        {"filterName": "placeId", "filterValues": ["ChIJzzlcLQGifDURm_JbQKHsEX4"]},
                        {"filterName": "priceFilterInputType", "filterValues": ["2"]},
                        {"filterName": "query", "filterValues": ["서울"]},
                        {"filterName": "refinementPaths", "filterValues": ["/homes"]},
                        {"filterName": "screenSize", "filterValues": ["large"]},
                        {"filterName": "tabId", "filterValues": ["home_tab"]},
                        {"filterName": "version", "filterValues": ["1.8.8"]}
                    ]
                },
                "isLeanTreatment": False,
                "aiSearchEnabled": False,
                "skipExtendedSearchParams": False
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "b29e3db8a086be4ef27ee0f2bd7ee3bbfa09cc2b84a214d5e254103078a4efa2"
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"오류 발생: {response.status_code}")
            break

        data = response.json()
        results_container = data.get('data', {}).get('presentation', {}).get('staysSearch', {}).get('results', {})
        search_results = results_container.get('searchResults', [])
        
        if not search_results:
            print("수집할 데이터가 더 이상 없습니다.")
            break

        for item in search_results:
            row = {
                "title": item.get('title'),
                "subtitle": item.get('subtitle'),
                "avg_rating": item.get('avgRatingLocalized'),
                "price": item.get('structuredDisplayPrice', {}).get('primaryLine', {}).get('price'),
                "total_price_label": item.get('structuredDisplayPrice', {}).get('primaryLine', {}).get('accessibilityLabel'),
            }
            all_data.append(row)
        
        # 다음 페이지 커서 업데이트
        pagination_info = results_container.get('paginationInfo', {})
        current_cursor = pagination_info.get('nextPageCursor')
        
        if not current_cursor:
            print("다음 페이지 커서가 없습니다. 수집을 종료합니다.")
            break
        
        page += 1
        # 서버 부하 방지를 위해 짧은 대기
        time.sleep(1)

    if all_data:
        df = pd.DataFrame(all_data)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'airbnb_scraping_seoul.db')
        
        conn = sqlite3.connect(db_path)
        df.to_sql('stays', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"총 {page}페이지에서 {len(df)}건의 데이터를 수집하여 {db_path}에 저장했습니다.")

if __name__ == "__main__":
    scrape_airbnb_seoul(max_pages=None)
