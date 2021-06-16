from booking_app.models import Appointment
import datetime

def is_valid(slot):
    time_min = datetime.time(9,0,0)
    time_max = datetime.time(17,0,0)
    time_in = slot.get('time_in')
    time_out = slot.get('time_out')

    if slot.get('date').weekday() == 6:
        return 'ErrorDay'
    if time_in >= time_out:
        return 'ErrorOrder'
    if time_in < time_min:
        return 'ErrorTimeIn'
    if time_out > time_max:
        return 'ErrorTimeOut'
    return True

def is_free(slot):
    state = is_valid(slot)
    if state == True:
        appointment_list = Appointment.objects.filter(date=slot.get('date'))
        for appointment in appointment_list:
            if not (appointment.time_in >= slot.get('time_out') or appointment.time_out <= slot.get('time_in')) and \
            not (appointment.last_name == slot.get('last_name') and appointment.first_name == slot.get('first_name')):
                return appointment
        return True
    else:
        return state