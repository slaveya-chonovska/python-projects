import requests
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor

def request_get_by_url(url:str,*,auth_token = None) -> float:
    start = perf_counter()
    if auth_token:
        try:
            requests.get(url,auth=auth_token)
        except (requests.exceptions.MissingSchema,requests.exceptions.InvalidURL):
            raise ValueError("WRONG URL!")
    else:
        try:
            requests.get(url)
        except (requests.exceptions.MissingSchema,requests.exceptions.InvalidURL):
            raise ValueError("WRONG URL!")
    end = perf_counter()
    return end-start

def http_caller(url:str,paralell_req:int,*,auth_token = None) -> str :
    urls = tuple(url for _ in range(paralell_req))
    with ThreadPoolExecutor(max_workers=paralell_req) as pool:
        if auth_token:
            times = (list(pool.map(request_get_by_url,urls,auth_token)))
        else:
            times = (list(pool.map(request_get_by_url,urls)))
    return f"Request for {url}:\nFastest time: {min(times)} seconds\nSlowest time: {max(times)} seconds\nAvg time: {sum(times)/len(times)} seconds"

if __name__ == "__main__":

    url = input("Website to request call: ")
    while True:
        try:
            paralell_req = int(input("How many number of paralel requests should be made? "))
            break
        except ValueError:
            print("Needs to be a number! Try again.")
            continue
    auth_token = input("Authentication (leave blank if not any): ")

    print(http_caller(url,paralell_req,auth_token = auth_token))



