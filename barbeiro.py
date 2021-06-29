import threading
import time
import random

exitFlag = 0

# fila de espera


class queue (threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q

    def run(self):
        fillQ(self.q, 2)

# barbeiro


class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print(self.name + " chegou na barbearia")
        barberGoToWork(self.name, self.q)

# funcao do barbeuro


def barberGoToWork(threadName, q):
    while not exitFlag:
        queueLock.acquire()

        if len(workQueue) > 0:
            data = q.pop()
            queueLock.release()
            print("%s cortando cabelo de %s" % (threadName, data))
            time.sleep(random.randrange(3, 7))
            print("%s cortou cabelo de %s" % (threadName, data))
        else:
            queueLock.release()
            print('%s dormindo' % threadName)
        time.sleep(1)

# cotrola a chegada de clientes na fila


def fillQ(q, delay):
    while True:
        wait = False

        if len(nameList) == 0:
            break
        time.sleep(1)
        queueLock.acquire()
        if len(q) < 4:
            c = nameList.pop()
            workQueue.append(c)
            print("cliente %s chegou na barbearia" % str(c))
        else:
            print("%s foi embora pq a fila esta cheia" % str(nameList[-1]))
            wait = True
        queueLock.release()

        if wait:
            time.sleep(delay*2)  # espera delay para poder voltar a barbearia


threadList = ["Barbeiro-1", "Barbeiro-2", "Barbeiro-3"]
nameList = []
queueLock = threading.Lock()
workQueue = []
threads = []
threadID = 1

tempoDeChegada = random.randrange(3, 10)

# criando 50 clientes
for x in range(50):
    nameList.append(str(x))

# Criando barbeiros
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# thread q controla clientes na fila
qThread = queue(workQueue)
qThread_.start()


# saida do programa quando acabar os clientes
while len(nameList) > 0:
    pass

exitFlag = 1

# esperar quem esta cortando
for t in threads:
    t.join()
print("Exiting Main Thread")
