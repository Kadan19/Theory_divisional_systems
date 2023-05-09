import threading
import time

class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork, semaphore):
        threading.Thread.__init__(self)
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.semaphore = semaphore
        self.state = "не їсть"

    def run(self):
        while True:
            self.think() # філософ розмірковує
            self.semaphore.acquire() # філософ чекає на доступ до вилок
            self.left_fork.acquire() # філософ бере ліву вилку
            self.right_fork.acquire() # філософ бере праву вилку
            self.eat() # філософ їсть
            self.left_fork.release() # філософ кладе ліву вилку
            self.right_fork.release() # філософ кладе праву вилку
            self.semaphore.release() # філософ звільняє доступ до вилок

    def think(self):
        self.state = "розмірковує"
        print(self.name + " розмірковує. ")
        time.sleep(1)
        
    def eat(self):
        self.state = "їсть"
        print(self.name + " починає їсти. ")
        time.sleep(3)
        print(self.name + " закінчує їсти і кладе вилки на стіл. ")

def main():
    forks = [threading.Semaphore(1) for n in range(5)] # створюємо 5 вилок за допомогою семафорів
    semaphore = threading.Semaphore(4) # створюємо семафор для обмеження кількості філософів за столом
    philosophers = ["Філософ " + str(n) for n in range(5)] # створюємо 5 філософів
    dining = [] # список потоків для філософів

    # створюємо потоки для філософів
    for i in range(5):
        dining.append(Philosopher(philosophers[i], forks[i%5], forks[(i+1)%5], semaphore))

    # запускаємо потоки для філософів
    for philosopher in dining:
        philosopher.start()

if __name__ == "__main__":
    main()