import sys
import math


def parse_file(path):
    try:
        line = open(path, 'r').read()
        lines = (line.replace('sphere', '"sphere"')
                    .replace('center', '"center"')
                    .replace('radius', '"radius"')
                    .replace('line', '"line"')
                    .replace("{[", "([")
                    .replace("]}", "])")
                    .replace(" ", ""))
        return eval(lines)
    except FileNotFoundError:
        print('Не верный путь к файлу')
        sys.exit()


def parse_dict(line):
    sphere = line.get('sphere')
    straight = line.get('line')
    center = sphere.get('center')
    radius = sphere.get('radius')
    return center, radius, straight


def calculate_intersection(center, radius, straight):
    x1, y1, z1 = straight[0][0], straight[0][1], straight[0][2]
    x2, y2, z2 = straight[1][0], straight[1][1], straight[1][2]
    x0, y0, z0 = center[0], center[1], center[2]
    result = []
    # Найдем коэф. и рассчитаем дискриминант
    a = (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
    b = 2*(x1-x0)*(x2-x1) + 2*(y1-y0)*(y2-y1) + 2*(z1-z0)*(z2-z0)
    c = (x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2 - radius**2
    d = b**2 - 4 * a * c
    if d < 0:
        print('Коллизий не найдено')
    elif d == 0:
        t1 = (-b + math.sqrt(d)) / (2 * a)
        xt1 = x1 + t1 * (x2 - x1)
        result.append(xt1)
        yt1 = y1 + t1 * (y2 - y1)
        result.append(yt1)
        zt1 = z1 + t1 * (z2 - z1)
        result.append(zt1)
        print(f"Координаты:\n x:{result[0]}\n y:{result[1]}\n z:{result[2]}\n")

    elif d > 0:
        t1 = (-b + math.sqrt(d)) / (2 * a)
        t2 = (-b - math.sqrt(d)) / (2 * a)
        xt1 = x1 + t1 * (x2 - x1)
        result.append(xt1)
        yt1 = y1 + t1 * (y2 - y1)
        result.append(yt1)
        zt1 = z1 + t1 * (z2 - z1)
        result.append(zt1)

        xt2 = x1 + t2 * (x2 - x1)
        result.append(xt2)
        yt2 = y1 + t2 * (y2 - y1)
        result.append(yt2)
        zt2 = z1 + t2 * (z2 - z1)
        result.append(zt2)
        print(f"Координаты:\n x1:{result[0]}\n y1:{result[1]}\n z1:{result[2]}\n x2:{result[3]}\n y2:{result[4]}\n z2:{result[5]}\n ")


def main():
    path = sys.argv[1]
    file = parse_file(path)
    center, radius, straight = parse_dict(file)
    calculate_intersection(center, radius, straight)


if __name__ == '__main__':
    main()
