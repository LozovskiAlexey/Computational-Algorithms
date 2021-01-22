def f(x):
    return x*x

def generateTable():
    table = list()
    
    x_start, x_end = map(float, input('Введите крайние значения х: ').split())
    step = float(input('Введите шаг: '))
    
    while x_start <= x_end:
        dot = [x_start, f(x_start)]
        table.append(dot)
        
        x_start += step
        
    print(table)

def main():
    generateTable()


if __name__ == '__main__':
    main()
