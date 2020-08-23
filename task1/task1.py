import sys


def itoBase(nb, baseSrc=None, baseDst=None):
    if baseDst is None:
        numbers = []
        result = []
        b = len(baseSrc)
        nb = int(nb)
        while nb > 0:
            numbers.append(nb % b)
            nb = nb // b
        numbers.reverse()
        for i in numbers:
            result.append(str(baseSrc[i]))
        return "".join(result)
    else:
        if isinstance(nb, str):
            n = int(nb, len(baseDst))
        else:
            n = int(nb)
        numbers = []
        result = []
        b = len(baseSrc)
        while n > 0:
            numbers.append(n % b)
            n = n // b
        numbers.reverse()
        for i in numbers:
            result.append(str(baseSrc[i]))
        return "".join(result)


def main():
    try:
        sys.argv = sys.argv[1:]
        if len(sys.argv) == 2:
            nb = sys.argv[0]
            baseSrc = sys.argv[1]
            print(itoBase(nb, baseSrc))
        elif len(sys.argv) == 3:
            nb = sys.argv[0]
            baseSrc = sys.argv[1]
            baseDst = sys.argv[2]
            print(itoBase(nb, baseSrc, baseDst))
        else:
            print('Введено некорректное число аргументов')
    except ValueError:
        print('Введите корректную систему исчесления')
        sys.exit()


if __name__ == '__main__':
    main()
