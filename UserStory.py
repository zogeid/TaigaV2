class UserStory:
    def __init__(self, us_id, ref, subject, description, assigned, status, init_date, fin_date, tasks):
        self.us_id = us_id
        self.fin_date = fin_date
        self.init_date = init_date
        self.status = status.encode('latin-1', 'replace').decode('latin-1')
        self.assigned = assigned.encode('latin-1', 'replace').decode('latin-1')
        self.description = description.encode('latin-1', 'replace').decode('latin-1').replace("{", "_").replace("}", "_")
        self.subject = subject.encode('latin-1', 'replace').decode('latin-1')
        self.tasks = [int(i) for i in tasks.split(",")] if tasks != '' else []
        self.ref = ref
        self.task_dict = {}
        self.url = f'https://tree.taiga.io/project/dalares-notificaciones/us/{self.ref}'

    def __repr__(self):
        return str(self.__dict__)