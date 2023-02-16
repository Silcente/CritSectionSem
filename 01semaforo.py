import multiprocessing
import time
import random
 
N = 4
def task(common, tid, sem):
    a = 0
    for i in range(4):
        print(f'{tid}-{i}: Non-critical Section', flush=True)
        a += 1
        time.sleep(random.random())
        print(f'{tid}-{i}: End of non-critical Section', flush=True)
        sem.acquire()
        print(f'{tid}-{i}: Critical section', flush=True)
        v = common.value + 1
        print(f'{tid}-{i}: Inside critical section', flush=True)
        time.sleep(random.random())
        common.value = v
        print(f'{tid}-{i}: End of critical section', flush=True)
        sem.release()

def main():
    lp = []
    common = multiprocessing.Value('i', 0)
    sem = multiprocessing.BoundedSemaphore(1)
    for tid in range(N):
        lp.append(multiprocessing.Process(target=task, args=(common, tid, sem)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")
if __name__ == "__main__":
    main()
