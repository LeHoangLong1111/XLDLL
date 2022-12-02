import threading

x = 0

def function1():
    global x
    x += 1

def thread1():
    for i in range(100000):
        function1()

def thread2():
    global x
    x=0
    t1=threading.Thread(target=thread1)
    t2=threading.Thread(target=thread1)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    for i in range(10):
        thread2()
        print("Iteration {0}: x={1} ".format(i,x))