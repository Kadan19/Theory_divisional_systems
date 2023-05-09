import threading
import time

class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork, waiter):
        threading.Thread.__init__(self)
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.waiter = waiter

    def run(self):
        while True:
            self.waiter.acquire() # Філософ чекає на офіціанта, щоб замовити їжу
            self.left_fork.acquire() # Філософ бере ліву виделку
            self.right_fork.acquire() # Філософ бере праву виделку
            self.eat() # Філософ їсть
            self.right_fork.release() # Філософ повертає праву виделку
            self.left_fork.release() # Філософ повертає ліву виделку
            self.waiter.release() # Філософ відпускає офіціанта
            self.think() # Філософ думає

    def eat(self):
        print(self.name + " починає їсти.")
        time.sleep(2) # Філософ їсть 2 секунди
        print(self.name + " закінчує їсти.")

    def think(self):
        print(self.name + " починає думати.")
        time.sleep(3) # Філософ думає 3 секунди
        print(self.name + " закінчує думати.")

if __name__ == "__main__":
    forks = [threading.Lock() for n in range(5)] # Створення 5 виделок, кожна з яких - потік
    waiter = threading.Lock() # Офіціант - теж потік (Lock)

    philosophers = []
    philosophers.append(Philosopher(" Філософ 1", forks[0], forks[1], waiter))
    philosophers.append(Philosopher(" Філософ 2", forks[1], forks[2], waiter))
    philosophers.append(Philosopher(" Філософ 3", forks[2], forks[3], waiter))
    philosophers.append(Philosopher(" Філософ 4", forks[3], forks[4], waiter))
    philosophers.append(Philosopher(" Філософ 5", forks[4], forks[0], waiter))

    for philosopher in philosophers:
        philosopher.start() # Запуск потоків