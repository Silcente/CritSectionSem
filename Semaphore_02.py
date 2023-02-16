import multiprocessing
import time
import random
N = 8
def is_anybody_inside(critical, tid):
    found = False
    i = 0
    while i<len(critical) and not found:
        found = tid!=i and critical[i]==1
        i += 1
    return found
def task(common, tid, critical, sem):
    a = 0
    for i in range(10):
        print(f'{tid}−{i}: Non−critical Section', flush=True)
        a += 1
        print(f'{tid}−{i}: End of non−critical Section', flush=True)
        while is_anybody_inside(critical, tid):
            pass
        critical[tid] = 1
        sem.acquire()
        print(f'{tid}−{i}: Critical section', flush=True)
        v = common.value + 1
        print(f'{tid}−{i}: Inside critical section', flush=True)
        common.value = v
        print(f'{tid}−{i}: End of critical section', flush=True)
        sem.release()
        critical[tid] = 0
def main():
    lp = []
    sem=multiprocessing.BoundedSemaphore(1)
    common = multiprocessing.Value('i', 0)
    critical = multiprocessing.Array('i', [0]*N)
    for tid in range(N):
        lp.append(multiprocessing.Process(target=task, args=(common, tid, critical, sem)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")
if __name__ == "__main__":
    main()
