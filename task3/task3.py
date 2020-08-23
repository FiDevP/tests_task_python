import csv
import sys


class MyException(Exception):
    """
    Исключенние которое обрабатывает отсутствие
    активных действий за указанный период
    """


# Создадим список с данными из csv файла.
# Вытащим из него значения объем бочки и текущий объем воды в бочке
def csv_file_read(file):
    reader = csv.reader(file)
    log_list = []
    for row in reader:
        log_list.append(row[0])
    return log_list


def execute_current_volume(log_list):
    barrel_volume = log_list.pop(0)
    current_barrel_volume = log_list.pop(0)
    log_list1 = []
    for line in log_list:
        log_list1.append(line.split(' - '))
    return current_barrel_volume


def parse_csv(log_list):
    # убераем лишнее
    # barrel_volume = log_list.pop(0)
    # current_barrel_volume = log_list.pop(0)
    log_list1 = []
    for line in log_list:
        log_list1.append(line.split(' - '))
    return log_list1


def selected_time(log_list1, first_date, second_date):
    # уберем в списке ненужное из даты
    # и в новый списоок добавим необходимый промежуток времени
    log_list_final = []
    for el in log_list1:
        date = el[0][:-5]
        if first_date <= date <= second_date:
            log_list_final.append([date, el[1], el[2]])
    # если за указанную дату не было совершенно никаких действий, тогда вызовем свое исключение
    if len(log_list_final) == 0:
        raise MyException("За указанный период не было совершено активных действий")
    # сделаем список и добавим туда все действия
    return log_list_final


def before_selected_time(log_list1, first_date):
    # создадим список действий до выбранного периода
    log_list_out = []
    for el in log_list1:
        date = el[0][:-5]
        if date < first_date:
            log_list_out.append([date, el[1], el[2]])
    return log_list_out


def top_up_water(log_list_final):
    actions_list = []
    for i in log_list_final:
        actions_list.append(i[2])
    # Посчитаем количество попыток добавить воду
    quantity_top_up = 0
    for el in actions_list:
        if el.find('top up') != -1:
            quantity_top_up += 1

    # Посчитаем процент ошибок
    success = 0
    fail = 0
    for i in actions_list:
        if i.find('top up') != -1:
            if i.find('успех') != -1:
                success += 1
            if i.find('фейл') != -1:
                fail += 1
    total = success + fail
    percent_top_up_fail = int((fail / total) * 100)

    # создадим списки с успешным и неуспешным добавлением воды
    # Посчитаем сколько воды было налито и не налито
    top_up_list_success = []
    top_up_list_fail = []
    for el in actions_list:
        if el.find('top up') != -1:
            if el.find('успех') != -1:
                top_up_list_success.append(el.split())
            if el.find('фейл') != -1:
                top_up_list_fail.append(el.split())
    total_top_up_success = 0
    for i in top_up_list_success:
        top_up_success = i[3][:-1]
        total_top_up_success += int(top_up_success)
    total_top_up_fail = 0
    for i in top_up_list_fail:
        top_up_fail = i[3][:-1]
        total_top_up_fail += int(top_up_fail)
    top_up_results = (quantity_top_up, percent_top_up_fail, total_top_up_success, total_top_up_fail)
    return top_up_results


def scoop_water(log_list_final):
    actions_list = []
    for i in log_list_final:
        actions_list.append(i[2])
    # посчитаем количество попыток вычерпнуть воду
    quantity_scoop = 0
    for i in actions_list:
        if i.find("scoop") != -1:
            quantity_scoop += 1
    # Посчитаем процент ошибок
    success = 0
    fail = 0
    for i in actions_list:
        if i.find('scoop') != -1:
            if i.find('успех') != -1:
                success += 1
            if i.find('фейл') != -1:
                fail += 1
    total = success + fail
    if total == 0:
        percent_scoop_fail = 0
    else:
        percent_scoop_fail = int((fail / total) * 100)
    # создадим списки с успешным и неуспешным вычерпыванием воды
    # Посчитаем сколько воды было налито и не налито
    scoop_list_success = []
    scoop_list_fail = []
    for el in actions_list:
        if el.find('scoop') != -1:
            if el.find('успех') != -1:
                scoop_list_success.append(el.split())
            if el.find('фейл') != -1:
                scoop_list_fail.append(el.split())
    total_scoop_success = 0
    for i in scoop_list_success:
        scoop_success = i[2][:-1]
        total_scoop_success += int(scoop_success)
    total_scoop_fail = 0
    for i in scoop_list_fail:
        scoop_fail = i[2][:-1]
        total_scoop_fail += int(scoop_fail)
    scoop_results = (quantity_scoop, percent_scoop_fail, total_scoop_success, total_scoop_fail)
    return scoop_results


def calculate_of_volume_water(log_list_final, log_list_out, current_barrel_volume):
    # создадим списки действий до выбранного периода и во время его
    actions_list = []
    for i in log_list_final:
        actions_list.append(i[2])
    actions_list_out = []
    for i in log_list_out:
        actions_list_out.append(i[2])
    # расчитаем объем воды в бочке на начало периода
    # расскидаем поспискам добавление и вычерпывание воды
    top_up_out_success = []
    scoop_out_success = []
    for el in actions_list_out:
        if el.find('успех') != -1:
            if el.find('scoop') != -1:
                scoop_out_success.append(el.split())
            if el.find('top up') != -1:
                top_up_out_success.append(el.split())
    # расчитаем объем воды в бочке на начало выбранного периода
    barrel_volume_before = int(current_barrel_volume)
    for i in top_up_out_success:
        top_up = i[3][:-1]
        barrel_volume_before += int(top_up)
    for i in scoop_out_success:
        scoop = i[2][:-1]
        barrel_volume_before -= int(scoop)
    # рассчитаем объем воды на конец выбранного периода
    top_up_success = []
    scoop_success = []
    for el in actions_list:
        if el.find('успех') != -1:
            if el.find('scoop') != -1:
                scoop_success.append(el.split())
            if el.find('top up') != -1:
                top_up_success.append(el.split())
    barrel_volume_after = barrel_volume_before
    for i in top_up_success:
        top_up = i[3][:-1]
        barrel_volume_after += int(top_up)
    for i in scoop_success:
        scoop = i[2][:-1]
        barrel_volume_after -= int(scoop)
    volume_results = (barrel_volume_before, barrel_volume_after)
    return volume_results


def write_csv(top_up_results, scoop_results, volume_results):
    column_name = (
        'Количество попыток налить воду',
        'Процент ошибок налить воду',
        'Было налито',
        'Было не налито',
        'Количество попыток вычерпнуть воду',
        'Процент оишбок вычерпнуть воду',
        'Было вычерпнуто',
        'Не было вычерпнуто',
        'Объем воды на начало выбранного периода',
        'Объем воды на конец выбранного ппериода'
    )
    column_data = top_up_results + scoop_results + volume_results
    total_column = list(zip(column_name, column_data))

    with open('output.csv', "w", newline='') as out_file:
        writer = csv.writer(out_file, delimiter=':')
        for line in total_column:
            writer.writerow(line)


def main():
    try:
        path, date_first, date_second = sys.argv[1:]
        with open(path, 'r') as file_obj:
            func = csv_file_read(file_obj)
            current_volume = execute_current_volume(func)
            parse = parse_csv(func)
            selected = selected_time(parse, date_first, date_second)
            before_selected = before_selected_time(parse, date_first)
            top_up_func = top_up_water(selected)
            scoop_func = scoop_water(selected)
            calculate_func = calculate_of_volume_water(selected, before_selected, current_volume)
            write_csv(top_up_func, scoop_func, calculate_func)
    except ValueError:
        print("Аргумента должно быть 3")
        sys.exit()
    except FileNotFoundError:
        print("Введите корректный путь до файла")
        sys.exit()
    except ZeroDivisionError:
        print("Неккоректно введена дата")
        sys.exit()


if __name__ == '__main__':
    main()
