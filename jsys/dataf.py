from jsys.models import TheDays, TheCalendar, Employee
from jsys import _D

def form_choices_active_emp():
    list = [(False, '---')]
    guy = Employee.query.filter_by(status='active')
    for x in guy:
        list.append((x.id, x.first_name + ' ' + x.last_name))
        print(list)
        return list
