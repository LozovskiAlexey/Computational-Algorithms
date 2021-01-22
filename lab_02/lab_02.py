import numpy
from lab_01 import *


def f(x):
    return x*x


def generate_table():
    try:
        xs = float(input('Введите начальный Х: '))
        xf = float(input('Введите конечный X: '))
        step = float(input('Введите шаг: '))

    except:
        print('Некорректный ввод.')

    else:
        x = numpy.arange(xs, xf + step/2, step)
        y = [f(i) for i in x]
        
    return x, y

def get_x(x):
    try:
        x0 = float(input('Введите Х: '))
    except:
        print('Некорректный ввод.')
        return None
    else:
        if x0 < x[0] or x0 > x[len(x)-1]:
            print('X не принаждлежит ни одному из промежутков таблицы.')
            return None
        else: 
            return x0


def show_result(x0, x, a, b, c, d, s):
    line = "_"*60
    print("|{x:^15}|{a:^10}|{b:^10}|{c:^10}|{d:^10}|".format(x = 'x', a = 'a',
                                                             b = 'b', c = 'c', d = 'd'))
    for i in range(len(x)-1):
        print("|{0:7.3f}-{1:^7.3f}|{2:^10.3f}|{3:^10.3f}|{4:^10.3f}|{5:^10.3f}|".\
              format(x[i], x[i+1], a[i], b[i], c[i+1], d[i]))
        
    print(line)
    print("Вычисление сплайнами: ")
    print("f({0}) = {1:.3f}".format(x0, s))
    print("Вычисление Ньютоном: ")

def show_table(x, y):
    for i in range(len(x)):
        print("| x = {0:<10.2f} | f(x) = {1:<10.2f}".format(x[i], y[i]))

    
def get_step(x):
    h = [x[i] - x[i-1] for i in range(1, len(x))]
    return h


def count_A(h):
    A = [h[i-1] for i in range(1, len(h))]
    return A


def count_B(h):
    B = [-2*(h[i-1] + h[i]) for i in range(1, len(h))]
    return B


def count_D(h):
    D = [h[i] for i in range(len(h)-1)]
    return D


def count_F(y, h):
    F = list()
    j = 2
    for i in range(1, len(h)):
        Fi = -3*((y[j]-y[j-1])/h[i-1] - (y[j-1]-y[j-2])/h[i-2])
        F.append(Fi)
        j += 1

    return F


def count_ksi(A, B, D):
    ksi = list()
    ksi.append(0) # первый кси по формуле равен нулю

    for i in range(1, len(A)+1):
        ksi_i = D[i-1]/(B[i-1] - A[i-1]*ksi[i-1])
        ksi.append(ksi_i)

    return ksi


def count_etta(A, B, D, F, ksi):
    etta = list()
    etta.append(0) # первая этта по формуле равен нулю

    for i in range(1, len(A)+1):
        etta_i = (A[i-1]*etta[i-1] + F[i-1]) / (B[i-1] - A[i-1]*ksi[i-1])
        etta.append(etta_i)

    return etta


def count_U(ksi, etta):
    n = len(ksi)+2
    U = [0]*n

    for i in range(n-3, 1, -1):
        U[i] = ksi[i-1] * U[i+1] + etta[i-1]
    return U


def count_a(y):
    a = list()
    for i in range(1, len(y)):
        ai = y[i-1]
        a.append(ai)

    return a


def count_d(c, h):
    d = list()
    for i in range(1, len(c)-1):
        di = (c[i+1] - c[i]) / (3*h[i-1])
        d.append(di)

    return d


def get_pos(x, x0):
    pos = None
    for i in range(1, len(x)):
        
        if x[i-1] <= x0 < x[i]:
            pos = i - 1
            break
    return pos
            

def count_b(y, h, c):
    b = list()
    for i in range(1, len(h)+1):
        bi = (y[i]-y[i-1])/ h[i-1] - 1/3*h[i-1]*(c[i+1]+2*c[i])
        b.append(bi)

    return b

    
def cubicspline(x, y, x0):
    # x0 - введенное значение
    
    # шаг
    h = get_step(x)

    # считает коэффициенты прогонки
    A = count_A(h)
    B = count_B(h)
    D = count_D(h)
    F = count_F(y, h)

    ksi = count_ksi(A, B, D)
    etta = count_etta(A, B, D, F, ksi)
    U = count_U(ksi, etta)

    # считаем маленькие коэффициенты сплайна
    c = U
    a = count_a(y)
    b = count_b(y, h, c)
    d = count_d(c, h)
        
    # поиск индекса промежутка которому принадлежит введенный икс
    pos = get_pos(x, x0)
    
    s = a[pos] + b[pos]*(x0-x[pos]) +\
        c[pos+1]*(x0-x[pos])**2 + \
        d[pos]*(x0-x[pos])**3

    return a, b, c, d, s


def main():
    # Ввод таблицы 
    x, y = generate_table()
    show_table(x, y)

    # Ввод икса 
    x0 = get_x(x)
    if x0 is not None:
        a, b, c, d, s =  cubicspline(x, y, x0)
        show_result(x0, x, a, b, c, d, s)

        # интерполяция ньютоном
        data = [[x[i], y[i]] for i in range(len(x))]
        n = interpolation(data, 2, x0)
        print("f({0}) = {1:.3f}".format(x0, n))
    
    # вывод полинома ньютона 

if __name__ == '__main__':
    main()
    
            
