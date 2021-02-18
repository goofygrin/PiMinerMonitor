import requests
import json


def get_flexpool_values(wallet):
    base_api_url = "https://flexpool.io/api/v1/miner/" + '0x' + wallet
    ret_value = {}

    # Get unpaid
    r = requests.get(base_api_url+"/balance")
    data = json.loads(r.text)
    ret_value["unpaid"] = data["result"]

    # Get unpaid
    r = requests.get(base_api_url+"/workerCount")
    data = json.loads(r.text)
    ret_value["workers"] = data["result"]["online"]

    # Get other stats
    r = requests.get(base_api_url+"/stats")
    data = json.loads(r.text)
    ret_value["reported_hashrate"] = data["result"]["current"]["reported_hashrate"]/1000000
    ret_value["actual_hashrate"] = data["result"]["current"]["effective_hashrate"]/1000000
    ret_value["invalid_shares"] = data["result"]["daily"]["invalid_shares"]
    ret_value["stale_shares"] = data["result"]["daily"]["stale_shares"]
    return ret_value
