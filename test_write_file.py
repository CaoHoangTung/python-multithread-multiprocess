import time
import threading
import multiprocessing
from multiprocessing.pool import ThreadPool

N_ITER = 100000
proc_lock = multiprocessing.Lock()
thread_lock = threading.Lock()

def write_data(file, data, lock=None):
    with proc_lock:
        with thread_lock:
            with open(f"{file}", 'a') as f:
                f.write(data)
                f.write("\n")

def single_threaded(file, data):
    start_time = time.time()
    for i in range(N_ITER):
        write_data(file, data)
    end_time = time.time()
    return end_time - start_time

def multi_threaded(file, data):
    start_time = time.time()
    threads = []
    for i in range(N_ITER):
        t = threading.Thread(target=write_data, args=(file, data, threading.Lock()))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    return end_time - start_time

def multi_thread_with_pool(file, data, num_thread=4):
    start_time = time.time()
    args = [
        (file, data, threading.Lock()) for i in range(N_ITER)
    ]
    with ThreadPool(num_thread) as pool:
        pool.starmap(write_data, args)
    end_time = time.time()
    return end_time - start_time

def multi_process(file, data):
    start_time = time.time()
    processes = []
    for i in range(N_ITER):
        p = multiprocessing.Process(target=write_data, args=(file, data, multiprocessing.Lock()))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    end_time = time.time()
    return end_time - start_time

def multi_thread_multi_process(file, data, num_proc=4, num_thread=4):
    start_time = time.time()
    args = [
        (file, data, num_thread)
        for i in range(num_proc)
    ]
    with multiprocessing.Pool(num_proc) as pool:
        pool.starmap(multi_thread_with_pool, args)
    end_time = time.time()
    return end_time - start_time

if __name__ == '__main__':
    file = 'output.txt'
    data = 'x' * 1024
    single_threaded_time = single_threaded(file+"single", data)
    print(f"Single-threaded time: {single_threaded_time:.3f} seconds")
    
    multi_threaded_time = multi_threaded(file+"thread", data)
    print(f"Multithreaded time: {multi_threaded_time:.3f} seconds")

    multi_process_time = multi_process(file+"process", data)
    print(f"Multiprocessing time: {multi_process_time:.3f} seconds")
    
    multi_thread_with_pool_time = multi_thread_with_pool(file+"threadpool", data)
    print(f"Multithreaded time: {multi_thread_with_pool_time:.3f} seconds")

    # multi_thread_multi_process_time = multi_thread_multi_process(
    #     file+"multithreadmultiprocess", 
    #     data, 
    #     num_proc=2,
    #     num_thread=50
    # )
    print(f"Multithreaded with pool time: {multi_thread_multi_process_time:.3f} seconds")