from math import pow, exp, log
import numpy as np
from time import time
from lab_01 import *

CONST = 0  # константа Pнач/Tнач

# флаги для вывода коэфф-тов
# ---------------------------------
FLAG = 0 # для вывода
Z_FLAG = 0
# ---------------------------------

V = -1  # начальное значение V
X = [3, -1, -20, -20, -20]  # начальные значения X

EPS = 1e-4  # для сходимости

Z = [0, 1, 2, 3, 4]  # для высчитывания dE
alpha = 0.285*pow(10, -11)

# значения из таблицы Градова
E = [12.13, 20.98, 31.00, 45.00]  
Q = [[1.0000, 1.0000, 1.0000, 1.0001, 1.0025, 1.0198, 1.0895, 1.2827, 1.6973, 2.4616, 3.3652, 5.3749, 7.6838],
     [4.0000, 4.0000, 4.1598, 4.3006, 4.4392, 4.5661, 4.6817, 4.7923, 4.9099, 5.0511, 5.2354, 5.4841, 5.8181],
     [5.5000, 5.5000, 5.5116, 5.9790, 6.4749, 6.9590, 7.4145, 7.8370, 8.2289, 8.5970, 8.9509, 9.3018, 9.6621],
     [11.000, 11.000, 11.000, 11.000, 11.000, 11.000, 11.000, 11.000, 11.000, 11.000, 11.000, 11.000, 11.000],
     [15.000, 15.000, 15.000, 15.000, 15.000, 15.000, 15.000, 15.000, 15.000, 15.000, 15.000, 15.000, 15.000]]
const_T = [2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000, 22000, 24000, 26000]


# класс функции T(z) чтоб по всем функциям не таскать много перменнных
# ==========================================================================
class T_function(object):
    def __init__(self, t0, tw, m):
        self.T0 = t0
        self.Tw = tw
        self.m = m

    def count(self, z):
        return self.T0 + (self.Tw - self.T0) * pow(z, self.m)


# вычисление уравнения и поиск P
# ==========================================================================

def count_eq(P, T):
    return 7243*CONST - 2*integrate(0, 1, T, P)


def integrate(a, b, T, P):
    # a, b - границы интегрирования
    # T, P параметры функции N(T(z), P)
    global Z_FLAG
    
    h = 0.05 
    res = 0 
    z = a

    # говорит что обрабатывает начальный Z
    # для вывода значений на экран
    # ---------------------------------------
    Z_FLAG = 1
    pr = N(T.count(z), P)*z 
    Z_FLAG = 0
    # ---------------------------------------
    
    z += h

    while z <= b+h:
        tmp = N(T.count(z), P)*z
        res += (pr + tmp)*h*0.5

        pr = tmp
        z += h
    return res


#  функция N(T(z), P)
def N(T, P):
    
    while True:
        # коэффициенты
        gamma = get_root(0, 3, EPS, count_gamma, T)
        dE = count_dE(gamma, T)
        k = count_K(dE, T)
        alp = alpha * pow(T*gamma, 3)
        
        # генерация матрицы
        right = generate_right(k, P, T, alp)
        left = generate_left()

        # решаем матрицу, получаем dv, dx0,...,dx4
        coefs = np.linalg.solve(left, right)
        dv = coefs[0]
        dx = coefs[1:]


        # обработка результата
        if not is_converge(dv, dx):
            VX_add(dv, dx)  # V+dv, Xi+dXi
        else:

            # вывод коэфф-тов
            # --------------------------------------------------------
            # if FLAG == 1 and Z_FLAG == 1:
            #     print("gamma = ", gamma)
            #     print("exp(V) = ", exp(V))
            #     for i in range(len(X)):
            #         print("exp(X[{0}]) = {1}".format(i+1, exp(X[i])))
            # --------------------------------------------------------

            
            return sum_VX() # sum(V, Xi)

    
        
# обработка dx, dv
# ==========================================================================
def is_converge(dv, dx):  # если сошлось 
    
    if abs(dv/V) > EPS:
        return 0
    
    for i in range(5):
        if abs(dx[i]/X[i]) > EPS:
            return 0
    return 1


# V +dV, X+dX
def VX_add(dv, dx):
    global V, X
    
    V += dv
    for i in range(5):
        X[i] += dx[i]


# N* = Ne + sum(Ni)    
def sum_VX():
    return exp(V) + sum([exp(i) for i in X])


# поиск коэффициентов gamma, dE, k, alpha
# ==========================================================================
def count_gamma(gamma, T):
    
    left = gamma*gamma
    half_gamma = gamma*0.5
    right = exp(V)/(1+half_gamma)
    const = 5.87 * pow(10, 10) / pow(T, 3)
    
    for i in range(5):   
        square_z = Z[i]*Z[i]
        right += (exp(X[i])*square_z/(1+square_z*half_gamma))    
    right *= const
    return left-right


def count_dE(gamma, T):
    const = 8.61*pow(10, -5)*T
    half_gamma = gamma*0.5

    dE = [const for _ in range(4)]

    for i in range(4):
        z0 = Z[i]
        z1 = Z[i+1]
        dE[i] *= log((1 + z1*z1 * half_gamma)*\
                     (1+half_gamma)/(1 + z0*z0 * half_gamma))
    return dE


def count_K(dE, T):
    const = 4.830 * pow(10, -3) * pow(T, 1.5)
    exp_const = 11603/T

    k = [const for _ in range(4)]

    pr_data = [[const_T[j], Q[0][j]] for j in range(len(const_T))]
    pr_Q = interpolation(pr_data, 4, T)
    
    for i in range(4):
        
        tmp_data = [[const_T[j], Q[i+1][j]] for j in range(len(const_T))]
        tmp_Q = interpolation(tmp_data, 4, T)

        k[i] *= (tmp_Q / pr_Q * exp((dE[i]-E[i])*exp_const))
        pr_Q = tmp_Q
    return k


# формировние матрицы 
# ==========================================================================

def generate_right(K, P, T, alp):
    right = [log(K[0])+X[0]-X[1]-V,
             log(K[1])+X[1]-X[2]-V,
             log(K[2])+X[2]-X[3]-V,
             log(K[3])+X[3]-X[4]-V,
             -exp(V)+Z[1]*exp(X[1])+Z[2]*exp(X[2])+Z[3]*exp(X[3])+Z[4]*exp(X[4]),
             exp(V)+exp(X[0])+exp(X[1])+exp(X[2])+exp(X[3])+exp(X[4])-alp-7243*P/T]    
    return right


def generate_left():
    left = [[1, -1, 1, 0, 0, 0],
            [1, 0, -1, 1, 0, 0],
            [1, 0, 0, -1, 1, 0],
            [1, 0, 0, 0, -1, 1],
            [exp(V), 0, -Z[1]*exp(X[1]), -Z[2]*exp(X[2]), -Z[3]*exp(X[3]), -Z[4]*exp(X[4])],
            [-exp(V), -exp(X[0]), -exp(X[1]), -exp(X[2]), -exp(X[3]), -exp(X[4])]]
    return left


# Дихотомия(поиск корня методом половинного деления)
# ==========================================================================

def get_root(start, end, eps, f, *args):
    # res - результат работы функции
    # args - аргументы функции
    
    root = abs(end + start)*0.5
    f_start = f(start, *args)
    
    while abs((end - start)/root) > eps:
        f_root = f(root, *args)
        
        if f_root*f_start < 0:
            end = root
        else:
            start = root
            f_start = f_root

        root = abs(end + start)*0.5        
    return root 

# ==========================================================================

def main():
    global CONST, FLAG
    
    # ввод параметров
    p_st = float(input("Введите Pнач: "))
    t_st = float(input("Введите Tнач: "))
    CONST = p_st / t_st

    t0 = float(input("Введите T0: "))
    tw = float(input("Введите Tw: "))
    m = float(input("Введите m: "))

    T = T_function(t0, tw, m)  # сохраняем параметры для высчитывания T(z)

    start = time()
    p = get_root(2, 20, EPS, count_eq, T)
    end = time()

    # вывод коэфф-тов
    # --------------------------------------------------------
    # FLAG = 1  # говорит функциям выводить коэфф-ты 
    # count_eq(p, T)
    # --------------------------------------------------------

    print("Результат вычислений: {:.4f}".format(p))
    print("Времени затрачено: {:.4f}".format(end - start))

    
if __name__ == "__main__":
    main()
