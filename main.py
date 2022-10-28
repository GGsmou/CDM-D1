import xml.etree.ElementTree as ET
import uuid
import asyncio
from concurrent.futures import ProcessPoolExecutor
import threading
import time
import datetime
from time import strftime

def load_inf():
    tree = ET.parse('data.xml')
    return tree, tree.getroot()

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

def getDay(date):
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

def show_inf(tree_last, root_last):
    tree, root = load_inf()

    def chage_checker

    for i in range(len(root)):
        datetime_str = root[i].attrib['value']
        print(f'{datetime_str[-2:]} {convert_month(datetime_str[5:7])} ({getDay(datetime_str)})')

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

    if root_last != root:
        threading.Timer(5.0, show_inf, [tree, root]).start()

if __name__ == '__main__':
    tree, root = load_inf()
    print(' \x1B[3mневідомий місяць\x1B[0m')
    show_inf(tree, root)

    #exrcutor = ProcessPoolExecutor(2)
    #loop = asyncio.new_event_loop()
    #gI = loop.run_in_executor(exrcutor, getInf)
    #sI = loop.run_in_executor(exrcutor, showInf)
    #loop.run_forever()