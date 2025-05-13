import requests
import json

COMPS_DATA_URL = "https://api-hc.metatft.com/tft-comps-api/comps_data"
COMPS_STATS_URL = 'https://api-hc.metatft.com/tft-comps-api/comps_stats?queue={queue}&patch=current&days=2&rank=CHALLENGER,DIAMOND,GRANDMASTER,MASTER&permit_filter_adjustment=true'
UNIT_ITEMS_PROCESSED_URL = 'https://api-hc.metatft.com/tft-comps-api/unit_items_processed'
COMP_DETAILS_URL = 'https://api-hc.metatft.com/tft-comps-api/comp_details?comp={comp_num}&cluster_id=330'

HEADERS = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-TW,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5,id;q=0.4',
        'origin': 'https://www.metatft.com',
        'priority': 'u=1, i',
        'referer': 'https://www.metatft.com/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }

def get_comps_data() -> dict:
    """
    Fetches the latest data from the comps API.
    """
    url = COMPS_DATA_URL
    headers = HEADERS
    
    response = requests.get(url, headers=headers)
    return response.json()

def get_comps_stats(queue:int) -> dict:
    """
    Fetches the latest stats from the comps API.
    """
    url = COMPS_STATS_URL.format(queue=queue)
    headers = HEADERS

    response = requests.get(url, headers=headers)
    return response.json()

def get_unit_items_processed() -> dict:
    """
    Fetches the latest unit items processed data from the comps API.
    """
    url = UNIT_ITEMS_PROCESSED_URL
    headers = HEADERS

    response = requests.get(url, headers=headers)
    return response.json()

def get_comp_details(comp_num:int) -> dict:
    """
    Fetches the details of a specific comp from the comps API.
    """
    url = COMP_DETAILS_URL.format(comp_num=comp_num)
    headers = HEADERS

    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    data = get_comps_data()
    print(data.keys())
    data = get_comps_stats(1100)
    print(data.keys())
    data = get_unit_items_processed()
    print(data.keys())
    data = get_comp_details(3)
    print(data.keys())
