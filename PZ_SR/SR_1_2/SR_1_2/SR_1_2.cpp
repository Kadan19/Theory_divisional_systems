#include <stdlib.h>
#include <stdio.h>
#include <omp.h>
#include <iostream>
#include <fstream>
#include <chrono>
#include <iomanip>

using namespace std;
using namespace chrono;

const int N = 100; // Встановлюємо максимальний розмір системи

int main() {
	setlocale(LC_ALL, "Russian");

	int m[] = { 1, 2, 4, 6, 8, 10, 20 }; // Масив кількості потоків
	int n; // Розмірність системи
	double a[N][N], b[N], x[N];

	// Вводимо розмір системи
	cout << "Введiть розмiр системи (n): ";
	cin >> n;

	// Вводимо коефіцієнти матриці a
	cout << "Введiть коефiцiєнти матрицi (a[i][j]):" << endl;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cin >> a[i][j];
		}
	}

	// Вводимо стовпець b
	cout << "Введiть стовпець b:" << endl;
	for (int i = 0; i < n; i++) {
		cin >> b[i];
	}

	// Обчислення часу виконання для кожної розмірності системи та кількості потоків
	for (int i = 0; i < 1; i++) {
		for (int j = 0; j < 7; j++) {
			int size = n;
			int num_threads = m[j];
			omp_set_num_threads(num_threads);

			high_resolution_clock::time_point start = high_resolution_clock::now(); // Початкова точка вимірювання часу виконання

			// Пряма елімінація
			for (int k = 0; k < size - 1; k++) {
#pragma omp parallel for
				for (int i = k + 1; i < size; i++) {
					double factor = a[i][k] / a[k][k];
					for (int j = k + 1; j < size; j++) {
						a[i][j] -= factor * a[k][j];
					}
					b[i] -= factor * b[k];
					a[i][k] = 0.0;
				}
			}
				// Обернена підстановка
				for (int k = size - 1; k >= 0; k--) {
					x[k] = b[k] / a[k][k];
#pragma omp parallel for
					for (int i = 0; i < k; i++) {
						b[i] -= a[i][k] * x[k];
						a[i][k] = 0.0;
					}
				}

			high_resolution_clock::time_point end = high_resolution_clock::now(); // Кінцева точка вимірювання часу виконання
			duration<double> time_span = duration_cast<duration<double>>(end - start); // Обчислення тривалості часу виконання

			
			cout << fixed << setprecision(7) << "Час виконання для n = " << size << " та " << num_threads << " потокiв: " << time_span.count() << " секунд" << endl;
		}

		cout << "Розв'язок системи:" << endl;
		for (int i = 0; i < n; i++) {
			cout << "x[" << i << "] = " << x[i] << endl;
		}
	}

	return 0;
}