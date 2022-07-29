import csv
from fpdf import FPDF
import requests
from datetime import date, datetime, timedelta
import json

class Epic:
    def populate_us_list(self, related_us):
        return [int(i) for i in related_us.replace("dalares-notificaciones#", "").split(",")]

    def __init__(self,  epic_id, ref, subject, description, assigned, status, init_date, fin_date, related_us):
        self.epic_id = int(epic_id)
        self.fin_date = fin_date
        self.init_date = init_date
        self.status = status
        self.assigned = assigned
        self.description = description.replace("{", "_").replace("}", "_")
        self.subject = subject
        self.related_us = self.populate_us_list(related_us)
        self.ref = ref
        self.us_dict = {}

    def __repr__(self):
        return str(self.__dict__)


class UserStory:
    def populate_tasks_list(self, tasks):
        return [int(i) for i in tasks.split(",")]

    def __init__(self, us_id, ref, subject, description, assigned, status, init_date, fin_date, tasks):
        self.us_id = us_id
        self.fin_date = fin_date
        self.init_date = init_date
        self.status = status
        self.assigned = assigned
        self.description = description.replace("{", "_").replace("}", "_")
        self.subject = subject
        self.tasks = self.populate_tasks_list(tasks) if tasks is not '' else []
        self.ref = ref
        self.task_dict = {}

    def __repr__(self):
        return str(self.__dict__)


class Task:
    def __init__(self, task_id, ref, subject, description, us, assigned, status, init_date, fin_date, hours):
        self.task_id = task_id
        self.ref = ref
        self.subject = subject
        self.description = description.replace("{", "_").replace("}", "_")
        self.us = us
        self.assigned = assigned
        self.status = status
        self.init_date = init_date
        self.fin_date = fin_date
        self.hours = hours.replace(",", ".")

    def __repr__(self):
        return str(self.__dict__)


path = 'C:/Users/dalares/PycharmProjects/TaigaV2'  # Ruta donde descargamos y creamos el .pdf
todayF = date.today().strftime("%d-%b-%Y")  # ddmmaaaa
epic_dict = {}
us_dict = {}
task_dict = {}


def struc_epic():
    epic_url = 'https://api.taiga.io/api/v1/epics/csv?uuid=1430473ef51d404384cdfcc4a19f631a'
    filename = "Epic" + " - " + str(todayF)
    request = requests.get(epic_url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
    open(path + filename + '.csv', 'wb').write(request.content)
    with open(path + filename + '.csv', encoding="latin-1") as csv_file:
        struc_csv_reader = csv.reader(csv_file, delimiter=',')
        for struc_row in struc_csv_reader:
            if struc_csv_reader.line_num > 1:
                epic = Epic(struc_row[0], struc_row[1], struc_row[2], struc_row[3], struc_row[6], struc_row[8], struc_row[16], struc_row[17], struc_row[18])
                for rel_us in epic.related_us:
                    temp_us = us_dict[int(rel_us)]
                    epic.us_dict[temp_us.ref] = temp_us
                epic_dict[epic.epic_id] = epic


def struc_us():
    us_url = 'https://api.taiga.io/api/v1/userstories/csv?uuid=c5994f0ac74c46bd84adb5e061546f86'
    filename = "US" + " - " + str(todayF)
    request = requests.get(us_url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
    open(path + filename + '.csv', 'wb').write(request.content)
    with open(path + filename + '.csv', encoding="latin-1") as csv_file:
        struc_csv_reader = csv.reader(csv_file, delimiter=',')
        for struc_row in struc_csv_reader:
            if struc_csv_reader.line_num > 1:
                us = UserStory(struc_row[0], struc_row[1], struc_row[2], struc_row[3], struc_row[10], struc_row[14], struc_row[25], struc_row[27], struc_row[35])

                for related_task in us.tasks:
                    temp_task = task_dict[int(related_task)]
                    us.task_dict[temp_task.ref] = temp_task
                us_dict[int(us.ref)] = us


def struc_task():
    task_url = 'https://api.taiga.io/api/v1/tasks/csv?uuid=7db9148a134947d89c13468473c193a0'
    filename = "Task" + " - " + str(todayF)
    request = requests.get(task_url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
    open(path + filename + '.csv', 'wb').write(request.content)
    with open(path + filename + '.csv', encoding="latin-1") as csv_file:
        struc_csv_reader = csv.reader(csv_file, delimiter=',')
        for row in struc_csv_reader:
            if struc_csv_reader.line_num > 1:
                task = Task(row[0], row[1], row[2], row[3], row[4], row[11], row[13], row[23], row[25], row[28])
                # print(task)
                task_dict[int(task.ref)] = task


def estructura_epic_userstory_task():
    struc_task()
    struc_us() # genero las us para luego generar Epics y poder coger del dict cada una de las ya creadas
    struc_epic()
    # print(epic_dict)
    json_string = json.dumps(epic_dict, default=lambda o: o.__dict__, sort_keys=True, indent=0)
    print(json_string)
    # print(epic_dict[166984])


def csv_reader():
    # 0- Tasks, 1- User Stories
    modo = 0
    today = date.today()
    todayF = today.strftime("%d-%b-%Y")  # ddmmaaaa
    if modo == 0:
        filename = "Tareas" + " - " + str(todayF)
        url = 'https://api.taiga.io/api/v1/tasks/csv?uuid=7db9148a134947d89c13468473c193a0'
    elif modo == 1:
        filename = "Historias de usuario" + " - " + str(todayF)
        url = 'https://api.taiga.io/api/v1/userstories/csv?uuid=c5994f0ac74c46bd84adb5e061546f86'
    else:
        filename = "Epics" + " - " + str(todayF)
        url = 'https://api.taiga.io/api/v1/epics/csv?uuid=1430473ef51d404384cdfcc4a19f631a'


    path = 'C:/Users/Popolo/PycharmProjects/Taiga'  # Ruta donde descargamos y creamos el .pdf
    #path = 'C:/Users/dalares/Downloads/'  # Ruta donde descargamos y creamos el .pdf
    r = requests.get(url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
    open(path + filename + '.csv', 'wb').write(r.content)

    # open pdf and set styles
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)

    # open weekly pdf
    pdfWeek = FPDF()
    pdfWeek.add_page()
    pdfWeek.set_font("Arial", size=15)

    lista = []
    countAsalomon = 0
    cHorasAsalomon = 0
    textAsalomon = ""
    countAicucu = 0
    cHorasAicucu = 0
    textAicucu = ""
    countJlavina = 0
    textJlavina = ""
    cHorasJlavina = 0

    # para certif SLORAS task 1025, us 734
    horasUS = 0
    userstories =[66,67,68,69,70,71,72,73,74,75,88,91,95,101,79,80,81,82,83,84,85,86,87,169,131,173,76,78,90,96,103,104,105,113,117,170,171,172,174,217,218,246,404,159,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,215,216,219,223,227,12,57,106,107,138,163,176,178,224,241,296,304,305,308,309,310,311,312,313,314,315,316,317,318,319,321,332,333,334,335,342,411,418,420,426,451,463,464,490,501,580,592,593,603,678,692,693,694,696,698,702,724,734,738,745,749,751,754,767,787,825,831,846,851,875,929,991,1002,1137]
    # para certif SLORAS task 1025, us 734

    with open(path + filename + '.csv', encoding="latin-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # loop all files and print pdf
        for row in csv_reader:
            if line_count == 0:
                pdf.cell(200, 10, txt=filename, ln=line_count, align='C')
                pdfWeek.cell(200, 10, txt=filename, ln=line_count, align='C')
                line_count += 1
            else:
                t = Task(row[2], row[3], row[4], row[12], row[13], row[23], row[25], row[28])

                # para certif SLORAS task 1025, us 734
                # task 1025, us 734
                if int(row[4]) in userstories:
                    if row[28] != '':
                        horasUS = horasUS + float(row[28].replace(",", "."))
                    else:
                        horasUS = horasUS + 8.5
                # para certif SLORAS task 1025, us 734
                # task 1025, us 734

                pdf.cell(200, 10, txt='', ln=line_count, align='L')
                pdf.cell(200, 10, txt=str(line_count), ln=line_count, align='L')

                pdf.set_font("Arial", 'B', 15)
                pdf.multi_cell(200, 10, txt=f'{t.assigned} - {t.subject}', align='L')
                pdf.set_font("Arial", size=15)

                pdf.multi_cell(200, 10, txt=str(t.description), align='L')
                pdf.cell(200, 10, txt=f'--> STATUS: {t.status}', ln=line_count, align='L')
                pdf.cell(200, 10, txt=f'--> INIT DATE: {t.init_date[0:19]}', ln=line_count, align='L')
                pdf.cell(200, 10, txt=f'--> END DATE: {t.fin_date[0:19]}', ln=line_count, align='L')

                h = '--> HOURS: 8' if t.hours == '' else f'--> HOURS: {t.hours}'
                pdf.cell(200, 10, txt=h, ln=line_count, align='L')
                pdf.cell(200, 10, txt=f'--> USER STORY: {t.us}', ln=line_count, align='L')
                line_count += 1

                d = datetime.today() - timedelta(days=5)  # weekly pdf with sysdate -5 days
                date_time_str = t.init_date[2:19]
                date_time_obj = datetime.strptime(date_time_str, '%y-%m-%d %H:%M:%S')
                if date_time_obj > d:
                    pdfWeek.cell(200, 10, txt='', ln=line_count, align='L')
                    pdfWeek.cell(200, 10, txt=str(line_count), ln=line_count, align='L')

                    pdfWeek.set_font("Arial", 'B', 15)
                    pdfWeek.multi_cell(200, 10, txt=f'{t.assigned} - {t.subject}', align='L')
                    pdfWeek.set_font("Arial", size=15)

                    pdfWeek.multi_cell(200, 10, txt=str(t.description), align='L')
                    pdfWeek.cell(200, 10, txt=f'--> STATUS: {t.status}', ln=line_count, align='L')
                    pdfWeek.cell(200, 10, txt=f'--> INIT DATE: {t.init_date[0:19]}', ln=line_count, align='L')
                    pdfWeek.cell(200, 10, txt=f'--> END DATE: {t.fin_date[0:19]}', ln=line_count, align='L')

                    h = '--> HOURS: 8' if t.hours == '' else f'--> HOURS: {t.hours}'
                    pdfWeek.cell(200, 10, txt=h, ln=line_count, align='L')
                    pdfWeek.cell(200, 10, txt=f'--> USER STORY: {t.us}', ln=line_count, align='L')

                    # Stats
                    if t.assigned == 'Alessandro':
                        countAsalomon = countAsalomon + 1
                        textAsalomon = textAsalomon + t.subject
                        cHorasAsalomon = cHorasAsalomon + (float(t.hours.replace(',', '.')) if t.hours != '' else 8)

                    elif t.assigned == 'Jlavina':
                        countJlavina = countJlavina + 1
                        textJlavina = textJlavina + t.subject
                        cHorasJlavina = cHorasJlavina + (float(t.hours.replace(',', '.')) if t.hours != '' else 8)

                    elif t.assigned == 'Alexandru Iulian Cucu':
                        countAicucu = countAicucu + 1
                        textAicucu = textAicucu + t.subject
                        cHorasAicucu = cHorasAicucu + (float(t.hours.replace(',', '.')) if t.hours != '' else 8)

        pdfWeek.cell(200, 10, txt='', ln=line_count, align='L')
        pdfWeek.set_font("Arial", 'B', 15)
        pdfWeek.cell(200, 10, txt='ESTADISTICAS', ln=line_count, align='L')
        pdfWeek.set_font("Arial", size=15)

        pdfWeek.cell(200, 10, txt='Alessandro', ln=line_count, align='L')
        pdfWeek.cell(200, 10, txt=f'--> Nº tareas: {countAsalomon}', ln=line_count, align='L')
        pdfWeek.cell(200, 10, txt=f'--> Horas: {countAsalomon}', ln=line_count, align='L')

        pdfWeek.cell(200, 10, txt='Jlavina', ln=line_count, align='L')
        pdfWeek.cell(200, 10, txt=f'--> Nº tareas: {countJlavina}', ln=line_count, align='L')
        pdfWeek.cell(200, 10, txt=f'--> Horas: {cHorasJlavina}', ln=line_count, align='L')

        pdfWeek.cell(200, 10, txt='Aicucu', ln=line_count, align='L')
        pdfWeek.cell(200, 10, txt=f'--> Nº tareas: {countAicucu}', ln=line_count, align='L')
        pdfWeek.cell(200, 10, txt=f'--> Horas: {cHorasAicucu}', ln=line_count, align='L')

    pdf.output(path + filename + ".pdf")
    pdfWeek.output(path + filename + "Week.pdf")
    print(horasUS)


#csv_reader()
estructura_epic_userstory_task()
