import datetime
from typing import List

content = []
with open('covid.csv', encoding='utf-8-sig') as file_daily:
    line = file_daily.readline().rstrip()
    for x in file_daily:
        content.append(x.rstrip().split(';'))

file_monthly = open('covid_mon.csv', 'w')

file_monthly.writelines('Data;Aktywne przypadki\n')

header = line + ';Aktywne przypadki;Próg'

previous_active = 0
current_active = 0
all_cases = 0
all_deaths = 0
week_cases = []

with open('covid.csv', 'w', encoding='utf-8-sig') as f:
    f.writelines(header)
    f.writelines('\n')
    check = 0
    for y in content:

        if check == 0:
            previous_line: List[str] = y
            check = 1
        all_cases = all_cases + int(y[1])
        all_deaths = all_deaths + int(y[2])
        current_active = previous_active + int(y[1]) - int(y[2]) - int(y[3])
        previous_active = current_active
        y.append(str(current_active))
        week_cases.append(int(y[1]))
        if len(week_cases) > 7:
            week_cases.pop(0)
        average = sum(week_cases) / 7
        prog = (average * 100000) / 37970000
        if prog <= 2:
            y.append('brak')
        elif 2 < prog <= 10:
            y.append('zielona')
        elif 10 < prog <= 25:
            y.append('żółta')
        elif 25 < prog <= 50:
            y.append('czerwona')
        elif 50 < prog <= 70:
            y.append('fioletowa')
        elif prog > 70:
            y.append('czarna')
        f.writelines(';'.join(y) + '\n')

        temp1 = y[0].split('.')
        temp2 = previous_line[0].split('.')
        data1 = datetime.date(int(temp1[2]), int(temp1[1]), int(temp1[0]))
        data2 = datetime.date(int(temp2[2]), int(temp2[1]), int(temp2[0]))

        if data1.month > data2.month:
            file_monthly.writelines(previous_line[0] + ';' + previous_line[4] + '\n')

        previous_line = y

    f.writelines('Wszystkie przypadki:;' + str(all_cases) + '\n')
    f.writelines('Wszystkie śmierci:;' + str(all_deaths) + '\n')

file_monthly.close()
