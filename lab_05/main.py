from math import pow

CONST = 0  # константа Pнач/Tнач


#  класс функции T(z) чтоб по всем функциям не таскать много перменнных
class T_function(object):
    def __init__(self, t0, tw, m):
        self.T0 = t0
        self.Tw = tw
        self.m = m

    def count(self, z):
        return self.T0 + (self.Tw - self.T0) * pow(z, self.m)


#  функция N(T(z), P)
def N(T, P):
    return 7243 * P / T


#  интеграл функции N(T(z), P)*z
def integrate(a, b, n, T, P):
    # a, b - границы интегрирования
    # n - число разбиений
    # T, P параметры функции N(T(z), P)

    h = float(b-a) / n  # высота трапеций
    res = 0  # результат куда суммируются площади
    z = a

    pr = N(T.count(z), P)*z
    z += h

    while z <= b:
        tmp = N(T.count(z), P)*z
        res += (pr + tmp)*h*0.5

        pr = tmp
        z += h

    return res


#  считает уравнение
def count_eq(T, P):
    global CONST
    n = 10  # число разбиений для метода трапеций

    return 7243*CONST - 2*integrate(0, 1, n, T, P)


#  находит корень уравнения методом дихотомии(половинного деления)
def get_p(T, int_p):
    eps = 1e-12
    st = int_p[0]
    end = int_p[-1]

# TODO если корня на промежутке нет - программа зациклится
    while True:
        # выбираем среднее значение интервала и решаем уравнение
        P = 0.5*(st + end)
        res = count_eq(T, P)

        # обработка получившегося значения
        if abs(res) <= eps:
            break
        elif res < 0:  # если полученное значение меньше нуля
            end = P    # берем интервал [:p]
        elif res > 0:  # иначе
            st = P     # интервал [p:]

    return P


def main():
    global CONST

    # ввод параметров
    p_st = float(input("Введите Pнач: "))
    t_st = float(input("Введите Tнач: "))
    CONST = p_st / t_st

    t0 = float(input("Введите T0: "))
    tw = float(input("Введите Tw: "))
    m = float(input("Введите m: "))

    int_p = [0, 20]
    T = T_function(t0, tw, m)  # сохраняем параметры для высчитывания T(z)
    p = get_p(T, int_p)

    print("Результат вычислений: {:.4f}".format(p))


if __name__ == "__main__":
    main()
