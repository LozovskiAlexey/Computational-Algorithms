import numpy
from math import fabs
from lab_01 import *

def f(x,y):
    return x*x + y*y

def generate_table():
    print("Генерация таблицы.")
    print("========================================\n")
    
    # генерация иксов
    xs = float(input("Введите начальный х: "))
    xf = float(input("Введите конечный х: "))
    step = float(input("Введите шаг: "))
    print("========================================\n")

    x = numpy.arange(xs, xf + step/2, step)

    # генерация у
    ys = float(input("Введите начальный y: "))
    yf = float(input("Введите конечный y: "))
    step = float(input("Введите шаг: "))
    print("========================================\n")

    y = numpy.arange(xs, xf + step/2, step)

    # генерация всей таблицы с Z
    data = [[None for _ in range(len(x) + 1)] for __ in range(len(y) + 1)]
     
    for i in range(len(x)):
        data[0][i + 1] = x[i]

    for i in range(len(y)):
        data[i + 1][0] = y[i]

    for i in range(len(y)):
        for j in range(len(x)):
            data[i+1][j+1] = f(x[j], y[i])

    return data


def show_table(table):
    print("\nСгенерированная таблица:\n")
    for item in table:
        print(" ".join("{:^8.2f}".format(el) if el is not None else "{:^8}".format("y \ x") for el in item))



def select_points(data, n, x):
    # n + 1 points

    data = data[1:]
    d_len = len(data)
    new_data = list()

    if d_len < n + 1:
        return None


    left = -1
    index = 0
    right = 1
    mins = fabs(x - data[0][0])
    count = 0

    for i in range(d_len):

        if fabs(x - data[i][0]) < mins:
            left = i - 1
            index = i
            right = i + 1
            mins = fabs(x - data[i][0])

    new_data.append(data[index])

    while left != -1 or right != d_len:
        if right != d_len:
            new_data.append(data[right])
            right += 1
            count += 1

        if count == n:
            break

        if left != -1:
            new_data.insert(0, data[left])
            left -= 1
            count += 1

        if count == n:
            break

    return sorted(new_data)


def bilinear_interpolation(data, nx, ny, x, y):

    data_y = select_points(data, ny, y)

    new_zx = list()

    for item in data_y:
        interpolation_data = [(data[0][i], item[i]) for i in range(1, len(data[0]))]
        
        res = interpolation(interpolation_data, nx, x)
        new_zx.append((item[0], res))
    
    res = interpolation(new_zx, ny, y)

    print("Результат интерполяции: ", res)

    return res

# main


def main():

    table = generate_table()
    show_table(table)

    print("\nВвол степеней полиномов по осям. ")
    nx = int(input('Введите степень полинома по x : '))
    ny = int(input('Введите степень полинома по y : '))

    print("\nВвод координат точки. ")
    x = float(input('Введите x : '))
    y = float(input('Введите y : '))

    bilinear_interpolation(table, nx, ny, x, y)
    print("Истинное значение: ", f(x, y))


if __name__ == '__main__':
    main()
