
import time
import multiprocessing
import threading
from utils import calculate_squares, N_TRIALS

BIG_NUMBER = 10000000

def test_single_thead():
    start_time = time.time()

    for i in range(N_TRIALS):
        calculate_squares(BIG_NUMBER)

    end_time = time.time()

    print("Time taken by single-threaded approach: ", end_time - start_time)

def test_multi_thead():
    start_time = time.time()

    threads = []
    for i in range(N_TRIALS):
        t = threading.Thread(target=calculate_squares, args=(BIG_NUMBER,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    print("Time taken by multithreaded approach: ", end_time - start_time)

def test_multi_process():
    start_time = time.time()

    processes = []
    for i in range(N_TRIALS):
        p = multiprocessing.Process(target=calculate_squares, args=(BIG_NUMBER,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()

    print("Time taken by multiprocessing approach: ", end_time - start_time)

if __name__ == "__main__":
    test_single_thead()
    test_multi_thead()
    test_multi_process()
