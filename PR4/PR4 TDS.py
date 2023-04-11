import random
import threading

# Задаємо розмір матриці
SIZE = 5

# Генеруємо матрицю розміром SIZE х SIZE з випадковими числами від 1 до 100
matrix = [[random.randint(1, 100) for j in range(SIZE)] for i in range(SIZE)]


def process_element(row, col):
    total_weight = 0
    # Обчислюємо суму ваг для всіх елементів у рядку, крім поточного
    for j in range(SIZE):
        if j != col:
            total_weight += matrix[row][j]
    # Обчислюємо суму ваг для всіх елементів у стовпці, крім поточного
    for i in range(SIZE):
        if i != row:
            total_weight += matrix[i][col]
    # Повертаємо сумарну вагу елемента
    return total_weight

# Ініціалізуємо змінні для зберігання максимальної ваги, максимального елемента та елементів з максимальною вагою
max_weight = 0
max_elem = 0
max_weight_elements = []

# Створюємо об'єкт блокування для забезпечення синхронізації доступу до загальних змінних
lock = threading.Lock()

def process_thread(start_row, end_row):
    global max_weight, max_weight_elements, max_elem
    # Проходимо по всіх елементах у діапазоні рядків
    for i in range(start_row, end_row):
        for j in range(SIZE):
            # Обчислюємо вагу поточного елемента
            weight = process_element(i, j)
            # Отримуємо блокування для зміни загальних змінних
            with lock:
                if weight > max_weight:
                    # Якщо вага поточного елемента більша за максимальну, то оновлюємо максимальну вагу,
                    # максимальний елемент та список елементів з максимальною вагою
                    max_weight = weight
                    max_weight_elements = [(i, j)]
                    max_elem = matrix[i][j]
                elif weight == max_weight:
                    # Якщо вага поточного елемента дорівнює максимальному, то додаємо його до списку елементів з максимальною вагою
                    max_weight_elements.append((i, j))

# Створюємо список потоків
threads = []
for i in range(0, SIZE, SIZE // 4):
    # Створюємо потік і додаємо його до списку
    thread = threading.Thread(target=process_thread, args=(i, i + SIZE // 4))
    threads.append(thread)
    # Запускаємо потік
    thread.start()

# Очікування завершення всіх потоків
for thread in threads:
    thread.join()

# Виведення матриці на екран
print("Matrix:")
for row in matrix:
    print(row)

# Виведення максимальної ваги, елементів з максимальною вагою та максимальний елемент на екран
print("Elements with max weight {}: {}".format(max_weight, max_weight_elements))
print("Element:", max_elem)
