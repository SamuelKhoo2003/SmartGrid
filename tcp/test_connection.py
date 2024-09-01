import queue
import time
import random

def driver(q):
    while True:
        power = random.uniform(0, 1.5)
        dataload = {"client": "load", "power":power}
        dataload1 = {"client": "load1", "power":power}
        data2 = {"client": "bidirectional", "power":random.uniform(0, 1.5)}
        if(q.empty()):
            q.put(dataload)
            q.put(dataload1)
        print(f"QUEUE********************************************************************{list(q.queue)}*************************************")
        time.sleep(5)