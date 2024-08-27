# buy_sell_algo/main.py

from multiprocessing import Process, Queue, set_start_method
from algo_driver import Algorithm
import os
import sys

# Ensure correct import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tcp")))

# Import start_server directly
from tcp_server import start_server

# Use spawn method for multiprocessing
set_start_method('spawn', force=True)

q = Queue()

def main():
    algo = Algorithm()
    server_host = '0.0.0.0'
    server_port = 5550

    # tcp server runs in separate process
    tcp_process = Process(target=start_server, args=(server_host, server_port, q))
    tcp_process.start()
    algo.driver(q)

    tcp_process.join()

if "__main__" == __name__:
    main()
