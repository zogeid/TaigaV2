class Epic:
    def __init__(self,  epic_id, ref, subject, description, assigned, status, init_date, fin_date, related_us):
        self.epic_id = int(epic_id)
        self.fin_date = fin_date
        self.init_date = init_date
        self.status = status
        self.assigned = assigned
        self.description = description.replace("{", "_").replace("}", "_")
        self.subject = subject
        self.related_us = [int(i) for i in related_us.replace("dalares-notificaciones#", "").split(",")]
        self.ref = ref
        self.us_dict = {}

    def __repr__(self):
        return str(self.__dict__)