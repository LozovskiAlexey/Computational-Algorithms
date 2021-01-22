import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return x - np.sin(x)


def generate_table():

    while True:
        try: 
            xs = float(input("Введите левую границу Х: "))
            xe = float(input("Введите правую границу Х: "))
            step = float(input("Введите шаг: "))
            
        except ValueError:
            print("Некорректный ввод. Введите вещественные значеения.")
            
        else:
            break

    x = np.arange(xs, xe+step/2, step)

    # заполнение файла
    file = open("table.txt", "w")
    for xi in x:
        file.write("{:.3f} {:.3f} {:.3f}\n".format(xi, f(xi), 1)) # 1 - вес, 1 по умолчанию
    file.close()


def get_table():

    file = open("table.txt", "r")
    x, y, w = [], [], []

    for line in file:
        line = list(map(float,line.split()))
        x.append(line[0])
        y.append(line[1])
        w.append(line[2])

    file.close()

    return x, y, w


def get_n():
    while True:
        try:
            n = int(input("Введите степень полинома: "))
        except ValueError:
            print("Некорректный ввод. Введите целое число.")
        else:
            break

    return n

##def mult(x1, x2, i, j, w):
    # i,j - степень
    # w - вес
##    summ = 0

##    n = len(x1)
##    for k in range(n):
##        mult = x1[k]**i * x2[k]**j * w[k]
##        summ += mult

##    return summ


##def generate_mtrx(n, x, y, w):

    # создаем левую и правую часть матрицы
##    r = [mult(y, x, 1, i, w) for i in range(n+1)]
##    l = [[mult(x, x, j, i, w) for j in range(n+1)] for i in range(n+1)]

##    print(l)
##    print(r)
##    return l, r

def mult_right(x, y, w, k):
    n = len(x)
    summ = 0
    for i in range(n):
        summ += w[i] * y[i] * (x[i])**(k)

    return summ


def mult_left(x, w, k, m):
    n = len(x)
    summ = 0
    for i in range(n):
        summ += w[i] * (x[i])**(k+m)

    return summ


def get_mtrx(x, y, w, n):
    left, right = [], []

    for k in range(n+1):
        
        tmp_left = []
        
        for m in range(n+1):
            tmp_left.append(mult_left(x, w, k, m))

        right.append(mult_right(x, y, w, k))
        left.append(tmp_left)

    return left, right
        

def draw(coefs, x0, y0):
    cx = np.arange(x0[0], x0[-1] + 1e-10, 0.1)
    x = list()
    y = list()
    for i in cx:
        x.append(i)
        y.append(fi(i, coefs))

    plt.plot(x, y) # полином 
    plt.scatter(x0, y0, alpha=0.3) 
    
    plt.show()


def fi(x, coefs):
    n = len(coefs)
    fi = 0
    
    for i in range(n):
        fi += x**i * coefs[i]

    return fi

    
def main():
    # генерируем таблицу в файле, по умолчанию вес=1

    # работа с файлом - создать новый, использовать готовый 
    print("Выберите: ")
    print("1. Создать таблицу")
    print("2. Использовать готовую")
    
    choice = int(input("Введите команду: "))
    if choice == 1: 
        generate_table()
        x, y, w = get_table()
    else:
        x, y, w = get_table()

    # считываем из файла таблицу, ввод степени полинома
    n = get_n()

    # матрица коэффициентов
    left, right = get_mtrx(x, y, w, n)# generate_mtrx(n, x, y, w)

    # решаем матрицу, находим коэффициенты        
    coefs = np.linalg.solve(left, right)

    # вывод на экран
    draw(coefs, x, y)
    
if __name__ == '__main__':
    main()
