import requests
import json


def get_ethermine_values(wallet):
    api_url = "https://api.ethermine.org/miner/{}/dashboard".format(wallet)
    r = requests.get(api_url)
    data = json.loads(r.text)
    ret_value = {}
    ret_value["unpaid"] = data["data"]["currentStatistics"]["unpaid"]/1000000000000000000
    ret_value["workers"] = data["data"]["currentStatistics"]["activeWorkers"]
    ret_value["reported_hashrate"] = data["data"]["currentStatistics"]["reportedHashrate"]/1000000
    ret_value["actual_hashrate"] = data["data"]["currentStatistics"]["currentHashrate"]/1000000
    ret_value["invalid_shares"] = data["data"]["currentStatistics"]["invalidShares"]
    ret_value["stale_shares"] = data["data"]["currentStatistics"]["staleShares"]
    return ret_value
