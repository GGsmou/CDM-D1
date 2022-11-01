import xml.etree.ElementTree as ET
import threading
import datetime
from xmldiff import main as xmldiffM

comand = 0

def load_inf():
    tree = ET.parse('data.xml')
    return tree, tree.getroot()

def save_inf(root):
    with open('data.xml.temp', 'wb') as f:
        b_tree = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
        f.write(b_tree)

def convert_month(num):
    month_dic = {'01':'січня',
                 '02':'лютого',
                 '03':'березня',
                 '04':'квітня',
                 '05':'травня',
                 '06':'червня',
                 '07':'липня',
                 '08':'серпня',
                 '09':'вересня',
                 '10':'жовтня',
                 '11':'листопада',
                 '12':'грудня'}
    return month_dic[num]

def get_day(date):
    day_dic = {0:'ПН',
               1:'ВТ',
               2:'СР',
               3:'ЧТ',
               4:'ПТ',
               5:'СБ',
               6:'НД',}
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[-2:])

    return day_dic[datetime.datetime(year, month, day).weekday()]

def main():
    tree, root = load_inf()
    save_inf(root)

    def reserv(date, film, time, root):
        print('')
        is_date = False
        is_film = False
        is_time = False

        for i in range(len(root)):
            datetime_str = root[i].attrib['value']
            datetime = f'{datetime_str[-2:]}.{datetime_str[5:7]}'

            if datetime == date:
                is_date = True
                for c in range(len(root[i][0])):
                    film_name = root[i][0][c].attrib["name"]
                    if film_name == film:
                        is_film = True
                        for b in range(len(root[i][0][c][0])):
                            if root[i][0][c][0][b].attrib["reserv"] == 'F':
                                time_str = root[i][0][c][0][b].attrib["time"]
                                if time_str == time:
                                    is_time = True
                                    print(f'Білет на фільм {film} зарезервовано на {time} | {date}')
                                    root[i][0][c][0][b].attrib["reserv"] = 'T'
                                    with open('data.xml', 'wb') as f:
                                        b_tree = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
                                        f.write(b_tree)
        if not is_date:
            print('Такої дати не існує')
            input_text(root)
        elif not is_film:
            print('Такого фільму не існує')
            input_text(root)
        elif not is_time:
            print('Такого часу не існує')
            input_text(root)

    def input_proces(root):
        try:
            global comand
            comand_inp = input('>    ')

            def error_msg():
                print('')
                print('Не коректне значення')
                input_text(root)
                return

            if comand == 1 and comand_inp != '1':
                reserv(comand_inp[0: 5], comand_inp[7: -7], comand_inp[-5:], root)
                return

            else:
                try:
                    comand_inp = int(comand_inp)
                    if comand_inp in [1, 2]:
                        if comand == 0:  comand = comand_inp
                        elif comand == 1: comand = 0
                        elif comand == 2: comand = 0
                        main()
                        return
                    else: error_msg()
                except ValueError: error_msg()
        except UnicodeDecodeError:
            return

    def input_text(root):
        if comand == 0:
            print('')
            print('Команди:')
            print('1. Забронювати сеанс')
            print('2. Список заброньованих сеансів')
        elif comand == 1:
            print('')
            print('Команди:')
            print('1. Повернутися назад')
            print('Щоб забронювати сеанс, введіть дані в форматі: 24.06, Назва, 00:00')
        elif comand == 2:
            print('')
            print('Команди:')
            print('1. Повернутися назад')


        threading.Thread(target=input_proces, args=[root]).start()

    def chage_checker():
        if len(xmldiffM.diff_files('data.xml', 'data.xml.temp')) == 0:
            t = threading.Timer(5.0, chage_checker)
            t.daemon = True
            t.start()
            t.join()
        else:
            main()
    if comand == 0:
        print('')
        for i in range(len(root)):
            datetime_str = root[i].attrib['value']
            print(f'{datetime_str[-2:]} {convert_month(datetime_str[5:7])} ({get_day(datetime_str)})')

            for c in range(len(root[i][0])):
                film_name = root[i][0][c].attrib["name"]
                tab_count = 20 - len(film_name)
                tabs = ' ' * tab_count
                time_str = ''

                for b in range(len(root[i][0][c][0])):
                    if root[i][0][c][0][b].attrib["reserv"] == 'F':
                        div_symb = ' | '
                        if time_str == '': div_symb = ''
                        time_str += f'{div_symb}{root[i][0][c][0][b].attrib["time"]}'
                if time_str == '': time_str = 'Всі білети заброньовано'
                print(f'    {film_name}{tabs}{time_str}')
        input_text(root)
    elif comand == 1:
        print('')
        print('Вільні сеанси:')
        have_print = False
        not_to_print = []

        for i in range(len(root)):
            film_name = False

            for c in range(len(root[i][0])):
                time_str = False

                for b in range(len(root[i][0][c][0])):
                    if root[i][0][c][0][b].attrib["reserv"] == 'F': time_str = True
                    if time_str: break

                if not time_str:
                    not_to_print.append(root[i][0][c])
                else:
                    film_name = True

            if not film_name: not_to_print.append(root[i])

        for i in range(len(root)):
            if not root[i] in not_to_print:
                have_print = True
                datetime_str = root[i].attrib['value']
                print(f'{datetime_str[-2:]} {convert_month(datetime_str[5:7])} ({get_day(datetime_str)})')

                for c in range(len(root[i][0])):
                    if not root[i][0][c] in not_to_print:
                        film_name = root[i][0][c].attrib["name"]
                        tab_count = 20 - len(film_name)
                        tabs = ' ' * tab_count
                        time_str = ''

                        for b in range(len(root[i][0][c][0])):
                            if root[i][0][c][0][b].attrib["reserv"] == 'F':
                                div_symb = ' | '
                                if time_str == '': div_symb = ''
                                time_str += f'{div_symb}{root[i][0][c][0][b].attrib["time"]}'

                        print(f'    {film_name}{tabs}{time_str}')
        if not have_print: print('Немає вільних сеансів')

        input_text(root)
    elif comand == 2:
        print('')
        print('Заброньовані сеанси:')
        have_print = False
        not_to_print = []

        for i in range(len(root)):
            film_name = False

            for c in range(len(root[i][0])):
                time_str = False

                for b in range(len(root[i][0][c][0])):
                    if root[i][0][c][0][b].attrib["reserv"] == 'T': time_str = True
                    if time_str: break

                if not time_str:
                    not_to_print.append(root[i][0][c])
                else:
                    film_name = True

            if not film_name: not_to_print.append(root[i])

        for i in range(len(root)):
            if not root[i] in not_to_print:
                have_print = True
                datetime_str = root[i].attrib['value']
                print(f'{datetime_str[-2:]} {convert_month(datetime_str[5:7])} ({get_day(datetime_str)})')

                for c in range(len(root[i][0])):
                    if not root[i][0][c] in not_to_print:
                        film_name = root[i][0][c].attrib["name"]
                        tab_count = 20 - len(film_name)
                        tabs = ' ' * tab_count
                        time_str = ''

                        for b in range(len(root[i][0][c][0])):
                            if root[i][0][c][0][b].attrib["reserv"] == 'T':
                                div_symb = ' | '
                                if time_str == '': div_symb = ''
                                time_str += f'{div_symb}{root[i][0][c][0][b].attrib["time"]}'

                        print(f'    {film_name}{tabs}{time_str}')
        if not have_print: print('Немає заброньованих сеансів')

        input_text(root)

    chage_checker()

if __name__ == '__main__':
    main()