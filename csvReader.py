import time
import csv
from fpdf import FPDF
import requests
from datetime import date, datetime, timedelta
import json
from Epic import Epic
from UserStory import UserStory
from Task import Task
start = time.time()

# path = 'C:/Users/dalares/PycharmProjects/TaigaV2'  # Ruta donde descargamos y creamos el .pdf
# path = 'C:/Users/Popolo/PycharmProjects/TaigaV2'  # Ruta donde descargamos y creamos el .pdf
path = ''

todayF = date.today().strftime("%d-%b-%Y")  # ddmmaaaa
epic_dict = {}
us_dict = {}
task_dict = {}

# TITULO GENERAL, 1, 1.1, 1.1.1

# mode: w:week, None:all
def struc_task(mode):
    task_url = 'https://api.taiga.io/api/v1/tasks/csv?uuid=7db9148a134947d89c13468473c193a0'
    filename = "Task" + " - " + str(todayF)
    request = requests.get(task_url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
    open(path + filename + '.csv', 'wb').write(request.content)
    with open(path + filename + '.csv', encoding="UTF-8") as csv_file:
        struc_csv_reader = csv.reader(csv_file, delimiter=',')
        for row in struc_csv_reader:
            if struc_csv_reader.line_num > 1:
                task = Task(row[0], row[1], row[2], row[3], row[4], row[11], row[13], row[23], row[25], row[28])
                if mode == 'w' and datetime.strptime(task.init_date[2:19], '%y-%m-%d %H:%M:%S') > (datetime.today() - timedelta(days=5)):
                    task_dict[int(task.ref)] = task


# mode: w:week, None:all
def struc_us(mode):
    us_url = 'https://api.taiga.io/api/v1/userstories/csv?uuid=c5994f0ac74c46bd84adb5e061546f86'
    filename = "US" + " - " + str(todayF)
    request = requests.get(us_url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
    open(path + filename + '.csv', 'wb').write(request.content)
    with open(path + filename + '.csv', encoding="UTF-8") as csv_file:
        struc_csv_reader = csv.reader(csv_file, delimiter=',')
        for struc_row in struc_csv_reader:
            if struc_csv_reader.line_num > 1:
                us = UserStory(struc_row[0], struc_row[1], struc_row[2], struc_row[3], struc_row[10], struc_row[14], struc_row[25], struc_row[27], struc_row[35])
                for related_task in us.tasks:
                    try:
                        temp_task = task_dict[int(related_task)]
                        us.task_dict[temp_task.ref] = temp_task
                    except KeyError:
                        pass
                if (mode == 'w' and us.task_dict) or mode != 'w':
                    us_dict[int(us.ref)] = us


# mode: w:week, None:all
def struc_epic(mode):
    epic_url = 'https://api.taiga.io/api/v1/epics/csv?uuid=1430473ef51d404384cdfcc4a19f631a'
    filename = "Epic" + " - " + str(todayF)
    request = requests.get(epic_url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
    open(path + filename + '.csv', 'wb').write(request.content)
    with open(path + filename + '.csv', encoding="UTF-8") as csv_file:
        struc_csv_reader = csv.reader(csv_file, delimiter=',')
        for struc_row in struc_csv_reader:
            if struc_csv_reader.line_num > 1:
                epic = Epic(struc_row[0], struc_row[1], struc_row[2], struc_row[3], struc_row[6], struc_row[8], struc_row[16], struc_row[17], struc_row[18])
                for rel_us in epic.uss:
                    try:
                        temp_us = us_dict[int(rel_us)]
                        epic.us_dict[temp_us.ref] = temp_us
                    except KeyError:
                        pass
                if (mode == 'w' and epic.us_dict) or mode != 'w':
                    epic_dict[epic.epic_id] = epic


def estructura_epic_userstory_task(mode):
    struc_task(mode)
    struc_us(mode)  # genero las us para luego generar Epics y poder coger del dict cada una de las ya creadas
    struc_epic(mode)
    # print(epic_dict[166984])


def epic_dict_printer():
    filename = "pdf_v2"

    # open pdf and set styles
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)

    for e in epic_dict:
        epic = epic_dict[e]
        pdf.set_font("Arial", 'B', 15)
        pdf.multi_cell(200, 10, txt=f'EPIC #{epic.ref} - {epic.subject} - @{epic.assigned}', align='L')
        pdf.set_font("Arial", size=15)

        pdf.multi_cell(200, 10, txt=f'DESC: {str(epic.description)}', align='L')
        pdf.multi_cell(200, 10, txt=f'STATUS: {epic.status}', align='L')
        pdf.multi_cell(200, 10, txt=f'INIT DATE: {epic.init_date}', align='L')
        pdf.multi_cell(200, 10, txt=f'END DATE: {epic.fin_date}', align='L')
        pdf.multi_cell(200, 10, txt=f'--> USER STORIES: {epic.uss}', align='L')

        for us in epic.uss:
            try:
                user_story = us_dict[us]
                pdf.set_font("Arial", 'B', 15)
                pdf.multi_cell(200, 10, txt=f'      USER STORY #{user_story.ref} - {user_story.subject} - @{user_story.assigned}', align='L')
                pdf.set_font("Arial", size=15)

                pdf.multi_cell(200, 10, txt=f'DESC: {str(user_story.description)}', align='L')
                pdf.multi_cell(200, 10, txt=f'STATUS: {user_story.status}', align='L')
                pdf.multi_cell(200, 10, txt=f'INIT DATE: {user_story.init_date}', align='L')
                pdf.multi_cell(200, 10, txt=f'END DATE: {user_story.fin_date}', align='L')
                pdf.multi_cell(200, 10, txt=f'--> TASKS: {user_story.tasks}', align='L')

                for t in user_story.tasks:
                    try:
                        task = task_dict[t]
                        pdf.set_font("Arial", 'B', 15)
                        pdf.multi_cell(200, 10, txt=f'            TASK #{task.ref} - {task.subject} - @{task.assigned}', align='L')
                        pdf.set_font("Arial", size=15)

                        pdf.multi_cell(200, 10, txt=f'DESC: {str(task.description)}', align='L')
                        pdf.multi_cell(200, 10, txt=f'STATUS: {task.status}', align='L')
                        pdf.multi_cell(200, 10, txt=f'INIT DATE: {task.init_date}', align='L')
                        pdf.multi_cell(200, 10, txt=f'END DATE: {task.fin_date}', align='L')
                        pdf.multi_cell(200, 10, txt=f'HOURS: {task.hours}', align='L')
                    except KeyError:
                        pass
            except KeyError:
                pass
        pdf.multi_cell(200, 10, txt="", align='L')
    pdf.output(filename + ".pdf")


# csv_reader()
estructura_epic_userstory_task('w')
epic_dict_printer()
# print(json.dumps(epic_dict, default=lambda o: o.__dict__, sort_keys=True, indent=0))
# epic_dict_printer()
print(f'Time elapsed: ', timedelta(seconds = time.time()-start))
