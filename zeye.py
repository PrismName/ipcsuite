import os
import time
import logging
import threading

from lib.data import VERSION, AUTHOR, POCS_PATHS, POCS, WORKER
from lib.requests import patch_session, _disable_warnings
from lib.cmd import set_commandline_options
from lib.loader import loader_string_to_module
from lib.threads import run_threading
from lib.color import Colors
from lib.logger import logger
from commons.outputs import save_result


def banner():
    logo = """{}       
       _                   _ __
      (_)__  _______ __ __(_) /____
     / / _ \\/ __(_-</ // / / __/ -_)
    /_/ .__/\\__/___/\\_,_/_/\\__/\\__/
   /_/
            {} #dev {}

            {}{}{}
    """.format(Colors.BLUE, Colors.YELLOW, VERSION, Colors.YELLOW,
               Colors.FUCHSIA, AUTHOR, Colors.FUCHSIA)
    print(logo)
    logger.info("Starting ipcsuite...")


def init():
    logger.info("Initializing system...")
    patch_session()
    _disable_warnings()

    _pocs = []

    for root, dirs, files in os.walk(POCS_PATHS):
        files = filter(lambda x: not x.startswith("__") and x.endswith(".py"),
                      files)
        _pocs.extend(map(lambda x: os.path.join(root, x), files))

    logger.info(f"Found {len(_pocs)} POC modules")
    for poc in _pocs:
        try:
            with open(poc, "r") as fs:
                module = loader_string_to_module(fs.read())
                # 验证POC模块是否包含必要的函数
                if not hasattr(module, "audit"):
                    logger.warning(f"POC module {poc} missing required 'audit' function")
                    continue
                POCS.append(module)
                logger.debug(f"Loaded POC module: {poc}")
        except Exception as e:
            logger.error(f"Failed to load POC module {poc}: {str(e)}")
            continue

    if not POCS:
        logger.warning("No valid POC modules loaded")
    else:
        logger.info(f"Successfully loaded {len(POCS)} POC modules")


def start():
    options, parser = set_commandline_options()

    if options.version:
        logger.info(f"Ipcsuite version: {VERSION}")
        print(f"Ipcsuite version: {VERSION}")
        exit(0)

    if options.target is None:
        logger.error("No target specified")
        exit(0)

    if options.debug:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Starting scan against target: {options.target}")
    for poc in POCS:
        WORKER.put((options.target, poc))

    run(options)


def worker(options=None):
    results = []
    while True:
        try:
            if WORKER.empty():
                break
            arg, poc = WORKER.get()
            try:
                # 确保URL包含scheme
                if not arg.startswith(('http://', 'https://')):
                    arg = 'http://' + arg
                logger.info(f"正在执行POC模块: {poc.__name__} -> 目标: {arg}")
                ret = poc.audit(arg)
                if ret:
                    if ret.get('status', False):
                        logger.info(f"[+] 在目标 {arg} 中发现漏洞")
                        logger.info(f"    漏洞名称: {ret.get('vuln_name', 'Unknown')}")
                        logger.info(f"    详细信息: {ret.get('msg', '')}")
                        if ret.get('payload'):
                            logger.info(f"    Payload: {ret['payload']}")
                    result = {"target": arg, "vulnerability": ret, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
                    results.append(result)
                    if ret.get('status', False):
                        print(f"{Colors.GREEN}[*]{Colors.GREEN} {ret}")
                    else:
                        logger.info(f"[-] POC {poc.__name__} 未在目标 {arg} 中发现漏洞")
            except Exception as e:
                logger.error(f"Error during POC execution: {str(e)}")
                logger.debug(f"Detailed error: ", exc_info=True)
            finally:
                WORKER.task_done()
        except Exception as e:
            logger.error(f"Error in worker thread: {str(e)}")
            logger.debug(f"Detailed error: ", exc_info=True)
            break

    return results

def run_threading(thread_count, target):
    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=target)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def run(options):
    all_results = []
    run_threading(options.threads, lambda: all_results.extend(worker(options)))
    
    # 所有POC执行完成后，统一保存结果
    if all_results:
        save_result({"results": all_results}, options.output, options.format)


def end():
    end_time = time.strftime("%X")
    logger.info(f"Scan completed at {end_time}")
    print("{0}[*]{1} end shutdown {2}".format(Colors.GREEN, Colors.GREEN, end_time))


def main():
    try:
        banner()
        init()
        start()
        end()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        exit(0)
