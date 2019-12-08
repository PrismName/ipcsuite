import threading
import time


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
    threads = []

    for number_threads in range(number_threads):
        thread = threading.Thread(target=exception_handler_function,
                                  name=str(number_threads),
                                  args=(threading_function, args))
        thread.setDaemon(True)
        try:
            thread.start()
        except Exception as e:
            error_msg = "error occurred while starting new thread {0}".format(str(e))
            print(error_msg)
            break
        threads.append(thread)
    alive = True

    while alive:
        alive = False
        for th in threads:
            if th.isAlive():
                alive = True
                time.sleep(0.1)
