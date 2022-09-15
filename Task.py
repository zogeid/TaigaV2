import datetime


class Task:
    def __init__(self, task_id, ref, subject, description, us, assigned, status, init_date, fin_date, hours):
        self.task_id = task_id
        self.ref = ref
        self.subject = subject.encode('latin-1', 'replace').decode('latin-1')
        self.description = description.encode('latin-1', 'replace').decode('latin-1').replace("{", "_").replace("}", "_")
        self.us = us
        self.assigned = assigned.encode('latin-1', 'replace').decode('latin-1')
        self.status = status
        self.init_date = init_date
        self.fin_date = fin_date
        self.hours = hours
        self.calculo_horas()
        self.url = f'https://tree.taiga.io/project/dalares-notificaciones/task/{self.ref}'

    def __repr__(self):
        return str(self.__dict__)

    def calculo_horas(self):
        if self.hours == "":
            if datetime.datetime.now().month == (7 or 8):
                self.hours = '7'
            else:
                self.hours = '8.5'
        self.hours.replace(",", ".")
