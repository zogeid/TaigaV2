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