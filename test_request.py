import time
import threading
import multiprocessing
from multiprocessing.pool import ThreadPool
import requests

def make_request(url):
    time.sleep(1)
    # response = requests.get(url)
    # print(response.status_code)

def single_threaded(urls):
    start_time = time.time()
    for url in urls:
        make_request(url)
    end_time = time.time()
    return end_time - start_time

def multi_threaded(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        t = threading.Thread(target=make_request, args=(url,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    return end_time - start_time

def multi_thread_with_pool(urls, num_thread=4):
    start_time = time.time()
    with ThreadPool(num_thread) as pool:
        pool.map(make_request, urls)
    end_time = time.time()
    return end_time - start_time

def multi_process(urls):
    start_time = time.time()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=make_request, args=(url,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    end_time = time.time()
    return end_time - start_time

def multi_process_with_pool(urls, num_proc=4):
    start_time = time.time()
    with multiprocessing.Pool(num_proc) as pool:
        pool.map(make_request, urls)
    end_time = time.time()
    return end_time - start_time

def multi_thread_multi_process(urls, num_proc=4, num_thread=4):

    batch_size = len(urls) // num_proc
    start_time = time.time()
    
    args = [
        (urls[batch_size*i:batch_size*(i+1)], num_thread)
        for i in range(num_proc+1)
    ]
    # import IPython ; IPython.embed()
    with multiprocessing.Pool(num_proc) as pool:
        pool.starmap(multi_thread_with_pool, args)
    end_time = time.time()
    return end_time - start_time

if __name__ == '__main__':
    urls = ['https://www.google.com', 'https://www.facebook.com', 'https://www.apple.com']*10
    
    single_threaded_time = single_threaded(urls)
    print(f"Single-threaded time: {single_threaded_time:.3f} seconds")
    
    multi_threaded_time = multi_threaded(urls)
    print(f"Multithreaded time: {multi_threaded_time:.3f} seconds")
    
    multi_process_time = multi_process(urls)
    print(f"Multiprocessing time: {multi_process_time:.3f} seconds")

    multi_thread_with_pool_time = multi_thread_with_pool(urls, num_thread=1000)
    print(f"Multithreading with pool time: {multi_thread_with_pool_time:.3f} seconds")

    multi_process_with_pool_time = multi_process_with_pool(urls, num_proc=3)
    print(f"Multiprocessing with pool time: {multi_process_with_pool_time:.3f} seconds")

    multi_thread_multi_process_time = multi_thread_multi_process(urls, num_proc=3, num_thread=10)
    print(f"multithread multiprocess with pool time: {multi_thread_multi_process_time:.3f} seconds")
