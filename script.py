#multithreaded
import requests
import random
import concurrent.futures
import time

image_urls = [
    "https://www.moctale.in/media/PC/PC1.jpg",
    "https://www.moctale.in/media/PC/PC2.jpg",
    "https://www.moctale.in/media/PC/PC3.jpg",
    "https://www.moctale.in/media/PC/PC4.jpg",
    "https://www.moctale.in/media/PC/PC5.jpg",
    "https://www.moctale.in/media/PC/PC6.jpg",
    "https://www.moctale.in/media/PC/PC7.jpg",
    "https://www.moctale.in/media/PC/PC8.jpg",
    "https://www.moctale.in/media/PC/PC9.jpg",
    "https://www.moctale.in/media/PC/PC10.jpg",
    "https://www.moctale.in/media/PC/PC11.jpg",
    "https://www.moctale.in/media/PC/PC12.jpg",
    "https://www.moctale.in/media/PC/PC13.jpg",
    "https://www.moctale.in/media/PC/PC14.jpg",
    "https://www.moctale.in/media/PC/PC15.jpg",
    "https://www.moctale.in/media/PC/PC16.jpg",
    "https://www.moctale.in/media/PC/PC17.jpg",
    "https://www.moctale.in/media/PC/PC18.jpg",
    "https://www.moctale.in/media/PC/PC19.jpg",
    "https://www.moctale.in/media/PC/PC20.jpg",
    "https://www.moctale.in/media/PC/PC21.jpg",
    "https://www.moctale.in/media/PC/PC22.jpg",
    "https://www.moctale.in/media/PC/PC23.jpg",
    "https://www.moctale.in/media/PC/PC24.jpg",
    "https://www.moctale.in/media/PC/PC25.jpg",
    "https://www.moctale.in/media/PC/PC26.jpg",
    "https://www.moctale.in/media/PC/PC27.jpg",
    "https://www.moctale.in/media/PC/PC28.jpg",
    "https://www.moctale.in/media/PC/PC29.jpg",
    "https://www.moctale.in/media/PC/PC30.jpg",
    "https://www.moctale.in/media/PC/ComicVerse.jpg",
    "https://www.moctale.in/media/PC/BnFTV.jpg",
    "https://www.moctale.in/media/PC/PJExplained.jpg"
]
headers = {
    "Host": "www.moctale.in",
    "Accept": "*/*",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "pragma": "no-cache",
    "referer": "https://www.moctale.in/",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "Connection": "close",
    "Expires": "0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Priority": "u=0, i"
}
def fetch_url(request_id):
    target_url = random.choice(image_urls)
    try:
        cache_bust_value = int(time.time() * 1000)
        params = {
        "_": cache_bust_value
        }
        response = requests.get(target_url, headers=headers,params=params)
        return f"[{request_id}] Status: {response.status_code} | URL: {target_url}"

    except requests.exceptions.RequestException as e:
        return f"[{request_id}] Error for {target_url}: {e}"
def run_multithreaded_check():
    total_requests = 10000
    max_workers = 500

    print(f"Starting execution: {total_requests} requests with up to {max_workers} concurrent threads...")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_url, i) for i in range(1, total_requests + 1)]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    duration = time.time() - start_time
    print("\n--- Execution Finished ---")
    print(f"Total time: {duration:.2f} seconds")
    print(f"Average throughput: {total_requests / duration:.2f} requests/second")

if __name__ == "__main__":
    run_multithreaded_check()


