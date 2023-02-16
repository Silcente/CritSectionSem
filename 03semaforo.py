import multiprocessing
import time
import random

N = 4
def is_anybody_inside(critical, tid):
    found = False
    i = 0
    while i<len(critical) and not found:
        found = tid!=i and critical[i]==1
        i += 1
    return found

def task(common, tid, critical, sem):
    a = 0
    for i in range(4):
        print(f'{tid}-{i}: Non-critical Section', flush = True)
        a += 1
        time.sleep(random.random())
        print(f'{tid}-{i}: End of non-critical Section', flush = True)
        critical[tid] = 1
        while is_anybody_inside(critical, tid):
            critical[tid] = 0
            print(f'{tid}-{i}: Giving up', flush = True)
            critical[tid] = 1
        sem.acquire()
        print(f'{tid}-{i}: Critical section', flush = True)
        v = common.value + 1
        print(f'{tid}-{i}: Inside critical section', flush = True)
        common.value = v
        print(f'{tid}-{i}: End of critical section', flush = True)
        sem.release()
        critical[tid] = 0

def main():
    lp = []
    common = multiprocessing.Value('i', 0)
    critical = multiprocessing.Array('i', [0]*N)
    sem = multiprocessing.BoundedSemaphore(1)
    for tid in range(N):
        lp.append(multiprocessing.Process(target=task, args=(common, tid, critical,sem)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")
if __name__ == "__main__":
    main()
