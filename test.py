from datetime import datetime, timedelta

dictio = {}

mode = '30/09/22'

print(f'INFORME DE TAREAS SEMANAL: {(datetime.today() - timedelta(days=5)).strftime("%b %d %Y")}')
datetime_object = datetime.strptime(mode, '%d/%m/%y')
print(f'INFORME DE TAREAS SEMANAL: ', datetime_object)

