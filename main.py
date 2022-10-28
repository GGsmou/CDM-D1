import xml.etree.ElementTree as ET
import threading
import datetime
from xmldiff import main as xmldiffM

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

    def chage_checker():
        if len(xmldiffM.diff_files('data.xml', 'data.xml.temp')) == 0:
            threading.Timer(5.0, chage_checker).start()
        else:
            main()

    for i in range(len(root)):
        datetime_str = root[i].attrib['value']
        print(f'{datetime_str[-2:]} {convert_month(datetime_str[5:7])} ({get_day(datetime_str)})')

        for c in range(len(root[i][0])):
            film_name = root[i][0][c].attrib["name"]
            tab_count = 20 - len(film_name)
            tabs = ' ' * tab_count
            time_str = ''

            for b in range(len(root[i][0][c][0])):
                div_symb = ''
                if b != 0: div_symb = ' | '
                time_str += f'{div_symb}{root[i][0][c][0][b].attrib["time"]}'

            print(f'    {film_name}{tabs}{time_str}')
        print('')
    print('Команди:')
    print('1. Забронювати сеанс')
    print('2. Список заброньованих сеансів')

    chage_checker()

if __name__ == '__main__':
    comand = 0
    main()