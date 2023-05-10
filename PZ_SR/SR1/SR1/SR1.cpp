#include <stdlib.h>
#include <stdio.h>
#include <omp.h>
#include <iostream>
#include <fstream>

using namespace std;

const int N = 100; // Встановлюємо максимальний розмір системи

int main() {
	setlocale(LC_ALL, "Russian");
	int n;
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

	// Пряма елімінація
	for (int k = 0; k < n - 1; k++) {
#pragma omp parallel for // Паралельний блок коду
		for (int i = k + 1; i < n; i++) {
			double factor = a[i][k] / a[k][k]; // Коефіцієнт
			for (int j = k; j < n; j++) {
				a[i][j] -= factor * a[k][j]; // Елімінація елементів матриці a
			}
			b[i] -= factor * b[k]; // Елімінація елементів стовпця b
		}
	}

	// Зворотня підстановка
	x[n - 1] = b[n - 1] / a[n - 1][n - 1]; // Розрахунок останнього кореня
	for (int i = n - 2; i >= 0; i--) {
		double sum = b[i];
		for (int j = i + 1; j < n; j++) {
			sum -= a[i][j] * x[j]; // Обчислюємо суму
		}
		x[i] = sum / a[i][i]; // Розраховуємо корінь
	}

	// Виводимо результат
	cout << "Розв'язок системи:" << endl;
	for (int i = 0; i < n; i++) {
		cout << "x[" << i << "] = " << x[i] << endl;
	}

	return 0;
}