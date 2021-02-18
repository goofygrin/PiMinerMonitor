import requests
import json


def get_hiveon_values(wallet):
    base_api_url = "https://hiveon.net/api/v1/stats/"
    ret_value = {}

    # Get unpaid
    r = requests.get(base_api_url+"miner/"+wallet+"/ETH/billing-acc")
    data = json.loads(r.text)
    ret_value["unpaid"] = data["totalUnpaid"]

    # Get workers
    r = requests.get(base_api_url+"workers-count?minerAddress="+wallet+"&coin=ETH&window=10m&limit=1")
    data = json.loads(r.text)
    ret_value["workers"] = data["items"][0]["count"]

    # Get hashrate stats
    r = requests.get(base_api_url+"hashrates?minerAddress="+wallet+"&coin=ETH&limit=1")
    data = json.loads(r.text)
    ret_value["reported_hashrate"] = int(data["items"][0]["reportedHashrate"])/1000000
    ret_value["actual_hashrate"] = int(data["items"][0]["hashrate"])/1000000
    
    # Get shares stats
    r = requests.get(base_api_url+"shares?minerAddress="+wallet+"&coin=ETH&window=10m&limit=144")
    data = json.loads(r.text)
    invalid_shares, stale_shares = 0, 0
    for item in data["items"]:
        stale_shares += int(item["staleCount"]) if "staleCount" in item else 0
        invalid_shares += int(item["invalidCount"]) if "invalidCount" in item else 0
    ret_value["invalid_shares"] = str(invalid_shares)
    ret_value["stale_shares"] = str(stale_shares)
    return ret_value
