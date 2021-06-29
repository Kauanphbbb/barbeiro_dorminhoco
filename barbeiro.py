from threading import Thread, Semaphore
from time import sleep
import random


class Barber(Thread):
    def __init__(self, chairs, total_customers):
        Thread.__init__(self)
        self.mutex = Semaphore()
        self.s_customers = Semaphore(0)
        self.s_barber = Semaphore()
        self.customers = []
        self.chairs = chairs
        self.customers_count = 0
        self.total_customers = total_customers

    def run(self):
        print("Waiting clients")
        while self.customers_count < self.total_customers:
            self.s_customers.acquire()
            self.mutex.acquire()
            customer = self.customers.pop(0)
            print(f"The customer {customer.name} sat in the chair.")
            customer.cut_hair()
            print(f"The customer {customer.name} left the chair.")
            self.customers_count += 1
            self.mutex.release()
        print("Barber is closed")

    def add_customer(self, customer):
        if len(self.customers) < self.chairs:
            print(f"Customer {customer.name} waiting his turn.")
            self.customers.append(customer)


class Customer(Thread):
    def __init__(self, barber, name):
        Thread.__init__(self)
        self.mutex = Semaphore()
        self.barber = barber
        self.name = name

    def run(self):
        sleep(random.randint(0, 5))
        self.mutex.acquire()
        if len(self.barber.customers) < self.barber.chairs:
            self.barber.add_customer(self)
            self.barber.s_customers.release()
            self.mutex.release()
        else:
            print(f"Barber is full. I'm going home ({self.name})")
            self.mutex.release()

    def cut_hair(self):
        print(f"The customer {self.name} is cutting its hair.")
        self.barber.s_barber.acquire()
        sleep(5)
        self.barber.s_barber.release()


if __name__ == "__main__":
    barber = Barber(3, 10)
    barber.start()
    count = 0
    while count < 50:
        sleep(2)
        customer = Customer(barber, f"Customers {count + 1}")
        customer.start()
        count += 1
    barber.join()
