import threading
import time
from concurrent.futures import ThreadPoolExecutor


def exception_handler_function(threading_function, args=()):
    try:
        threading_function(*args)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(args)
        print("thread {0} : {1}".format(threading.currentThread().getName(),
                                        str(e)))


def run_threading(number_threads, threading_function, args: tuple=()):
    with ThreadPoolExecutor(max_workers=number_threads) as executor:
        futures = []
        for _ in range(number_threads):
            future = executor.submit(exception_handler_function,
                                   threading_function, args)
            futures.append(future)
        
        # 等待所有任务完成
        for future in futures:
            try:
                future.result()
            except Exception as e:
                error_msg = "error occurred in thread pool: {0}".format(str(e))
                print(error_msg)
