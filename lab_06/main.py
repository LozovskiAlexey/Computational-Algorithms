from math import log

# функция, которую дифференцируем
# отсюда получаем значения y
def f(x):
    return x/(1+2*x)


# функция которой дифференцируем 
def fi(x0, y0, x1, y1):
    # x0, y0 - точка 1
    # x1, y1 - точка 2
    # по этим точкам считается dy/dx
    return (y1-y0) / (x1-x0)


# формирование первого и второго столбцов таблицы - x, y
def generateData():
    x = [float(i) for i in range(1, 12)]
    y = [f(x[i]) for i in range(len(x))]
    
    return x, y


# односторонная разность - первая формула дифференцирования
def oneSidedDiff(x, y, length):
    oneSided = ["-" for i in range(length)]  # столбец производных, заполняем его -
    x0, y0 = x[0], y[0]  # определяем начальную точку

    # проходим по массивам х, у слева направо
    # используем левостороннюю разность (Fi+1 - Fi)/(Xi+1 - Xi)
    for tmp in range(1, length):
        
        x1, y1 = x[tmp], y[tmp]
        oneSided[tmp] = fi(x0, y0, x1, y1)
        x0, y0 = x1, y1
        
    return oneSided


# центральная разность
# для каждой точки берется следующая и предыдущая и считается производная
# (Fi+1 - Fi-1)/(Xi+1 - Xi-1)
def centralDiff(x, y, length):
    centralDiff = ["-" for i in range(length)]

    for tmp in range(1, length-1):
        prev = tmp-1
        next = tmp+1

        centralDiff[tmp] = fi(x[prev], y[prev], x[next], y[next])
    return centralDiff


# не помню как называется метод, не так, как функция
# используется формула Градова и по не высчитываются с повышенной точностью
# значения производной на концах отрезка
# если рассматривать массив [1, 2, 3, 4, 5, 6]
# чтобы вычислить первое значение берутся точки 1, 2, 3
# для второго значения нужны 6, 5, 4
def leftSideDiff(x, y, length):
    lsDiff = ["-" for i in range(length)]
    
    h = x[2] - x[0]  # шаг
    lsDiff[0] = (-3*y[0] + 4*y[1] - y[2]) / h  # первое значения 
    lsDiff[-1] = (3*y[-1] - 4*y[-2] + y[-3]) / h  # последнее значения 
    return lsDiff


# формула Рунге, считает также с повышенной точностью
# последние два значения в таблице отсутствуют, потому что используется
# левосторонняя разность, т.е для высчитывания производной в текущей точке
# используются две следующие за ней точки, если проходить по всем точкам
# мы выйдем за границы массива 
def rungeDiff(x, y, length):
    print("x= ", x)
    rDiff = ["-" for i in range(length)]
    x0, y0 = x[0], y[0]
    x1, y1 = x[1], y[1]

    for i in range(length-2):
        x2, y2 = x[i+2], y[i+2]
        
        rDiff[i] = 2*fi(x0, y0, x1, y1) - fi(x0, y0, x2, y2)
        x0, y0 = x1, y1
        x1, y1 = x2, y2

    # раскомментируй меня, если Градов попросит вывод таблицы для всех точек
    # тут используем правостороннюю разность, т.е для каждой точки используем
    # две предыдущие
    
    # x0, y0 = x[-1], y[-1]
    # x1, y1 = x[-2], y[-2]
    # for i in range(length-3, 2, -1):
    #     x2, y2 = x[i], y[i]
    #     rDiff[i+2] = 2*fi(x0, y0, x1, y1) - fi(x0, y0, x2, y2)
    #     x0, y0 = x1, y1
    #     x1, y1 = x2, y2 
        
    return rDiff



# выравнивающие переменные
# преобразовываем нашую фукнцию так, чтобы в ней можно было заменить
# переменные на новые функции, зависимость которых друг от друга будет линейна
# в коде мы этого не делаем, делаем это ручками, градов любезно сделал это за 
# нас дибилов, в нашей функции этта = 1/y, кси = 1/x
# получили этта = кси + 2
# дальше творится магическое безобразие, мы прогаем его формулу 

def alignDiff(x, y, length):
    etta = [1/y[i] for i in range(length)]
    ksi = [1/x[i] for i in range(length)]
    diff = [y[i]*y[i]/x[i]/x[i] for i in range(length)]  # его формула

    
    alignDiff = ["-" for i in range(length)]
    for i in range(length-1):
        alignDiff[i] = diff[i]*fi(ksi[i], etta[i], ksi[i+1], etta[i+1]) # продолжение его формулы 

    return alignDiff  


# вывод таблицы
def showData(p):
    # p - значения производных и x,y 
    width = len(p)
    height = len(p[0])
    

    print("{0:^13}|{1:^13}|{2:^13}|{3:^13}|"
              "{4:^13}|{5:^13}|{6:^13}|".format("x", "y","OneSide",
                                                      "CentralSide", "leftSide",
                                                      "Runge", "Align"))
    
    for row in range(height):
        print("{0:^13.3}|{1:^13.3}|{2:^13.2}|{3:^13.2}|"
              "{4:^13.2}|{5:^13.2}|{6:^13.2}|"\
              .format(p[0][row],p[1][row],p[2][row],p[3][row],\
                      p[4][row],p[5][row],p[6][row]))

        
            
def main():
    x, y = generateData()
    length = len(x)

    frst = oneSidedDiff(x, y, length)
    scnd = centralDiff(x, y, length)
    thrd = leftSideDiff(x, y, length)
    frth = rungeDiff(x, y, length)
    ffth = alignDiff(x, y, length)

    showData([x, y, frst, scnd, thrd, frth, ffth])


if __name__ == "__main__":
    main()
