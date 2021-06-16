from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from .models import Appointment, ChangeLog
from .forms import AppointmentForm
from .booking_functions.functions import is_free
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    UpdateView,
    DeleteView,
)
# Create your views here.

class AppointmentListView(ListView):
    model = Appointment

class AppointmentDetailView(DetailView):
    model = Appointment

class AppointmentFormView(FormView):
    model = Appointment
    template_name = 'appointment_form.html'
    form_class = AppointmentForm
    success_url = '/booking/list/'

    def form_valid(self, form):
        slot = form.cleaned_data
        free = is_free(slot)
        last_name = slot.get('last_name')
        first_name = slot.get('first_name')
        time_in = slot.get('time_in')
        time_out = slot.get('time_out')
        date = slot.get('date')
        comment = slot.get('comment')
        if free == True:
            booking = Appointment.objects.create(
                user = self.request.user,
                date_created = timezone.now(),
                date = date,
                time_in = time_in,
                time_out = time_out,
                last_name = last_name,
                first_name = first_name,
                comment = comment
                )
            booking.save()
            log = f'CREATE SUCCESS. Appointment<{first_name} {last_name}: {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}> ON {timezone.now()} BY {self.request.user}'
            changelog = ChangeLog.objects.create(log = log, date_logged = timezone.now())
            changelog.save()
            messages.success(self.request, f'Created appointment for {first_name} {last_name}: {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}')
            return super().form_valid(form)
        else:
            if free == 'ErrorTimeIn':
                messages.error(self.request, 'Create failed: Invalid time in. Appointments are only allowed from 9:00 AM to 5:00 PM.')
            elif free == 'ErrorTimeOut':
                messages.error(self.request, 'Create failed: Invalid time out. Appointments are only allowed from 9:00 AM to 5:00 PM.')
            elif free == 'ErrorOrder':
                messages.error(self.request, 'Create failed: Invalid time in/time out. Time in must be earlier than time out.')
            elif free == 'ErrorDay':
                messages.error(self.request, 'Create failed: Invalid date. Appointments are only allowed from Monday to Saturday.')
            else:
                messages.error(self.request, f'Create failed: Conflict with:\
                {free.first_name} {free.last_name}: {free.time_in.strftime("%H:%M")}-{free.time_out.strftime("%H:%M")}, {free.date}')
            log = f'CREATE FAILED. Appointment<{first_name} {last_name}: {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}> ON {timezone.now()} BY {self.request.user}'
            changelog = ChangeLog.objects.create(log = log, date_logged = timezone.now())
            changelog.save()
            return self.render_to_response(self.get_context_data(form=form))

class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ['date', 'time_in', 'time_out', 'last_name', 'first_name', 'comment']

    def form_valid(self, form):
        slot = form.cleaned_data
        last_name = slot.get('last_name')
        first_name = slot.get('first_name')
        time_in = slot.get('time_in')
        time_out = slot.get('time_out')
        date = slot.get('date')
        free = is_free(slot)
        if free == True:
            messages.success(self.request, f'Updated appointment of {first_name} {last_name} to {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}')
            log = f'UPDATE SUCCESS. Appointment<{first_name} {last_name}: {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}> ON {timezone.now()} BY {self.request.user}'
            changelog = ChangeLog.objects.create(log = log, date_logged = timezone.now())
            changelog.save()
            return super().form_valid(form)
        else:
            if free == 'ErrorTimeIn':
                messages.error(self.request, 'Update failed: Invalid time in. Appointments are only allowed from 9:00 AM to 5:00 PM.')
            elif free == 'ErrorTimeOut':
                messages.error(self.request, 'Update failed: Invalid time out. Appointments are only allowed from 9:00 AM to 5:00 PM.')
            elif free == 'ErrorOrder':
                messages.error(self.request, 'Update failed: Invalid time in/time out. Time in must be earlier than time out.')
            elif free == 'ErrorDay':
                messages.error(self.request, 'Update failed: Invalid date. Appointments are only allowed from Monday to Saturday.')
            else:
                messages.error(self.request, f'Update failed: Conflict with:\
            {free.first_name} {free.last_name}: {free.time_in.strftime("%H:%M")}-{free.time_out.strftime("%H:%M")}, {free.date}')
            log = f'UPDATE FAILED. Appointment<{first_name} {last_name}: {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}> ON {timezone.now()} BY {self.request.user}'
            changelog = ChangeLog.objects.create(log = log, date_logged = timezone.now())
            changelog.save()
            return self.render_to_response(self.get_context_data(form=form))

class SuccessDeleteMessageMixin:
    success_message = ''

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        success_message = self.get_success_message()
        if success_message:
            messages.warning(self.request, success_message)
        return response

    def get_success_message(self):
        return self.success_message

class AppointmentDeleteView(SuccessDeleteMessageMixin, DeleteView):
    model = Appointment
    success_url = '/booking/list/'

    def get_success_message(self):
        last_name = self.object.last_name
        first_name = self.object.first_name
        time_in = self.object.time_in
        time_out = self.object.time_out
        date = self.object.date
        log = f'DELETE. Appointment<{first_name} {last_name}: {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}> ON {timezone.now()} BY {self.request.user}'
        changelog = ChangeLog.objects.create(log = log, date_logged = timezone.now())
        changelog.save()
        return f'Deleted appointment of {first_name} {last_name}: {time_in.strftime("%H:%M")}-{time_out.strftime("%H:%M")}, {date}'

def AppointmentSearchView(request):
    if 'search' in request.POST:
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        result = Appointment.objects.raw('SELECT * FROM booking_app_appointment WHERE date BETWEEN "'+start_date+'" AND "'+end_date+'" ORDER BY date')
        context = {
            'data': result
        }
        return render(request, 'appointment_search.html', context)
    elif 'clear' in request.POST:
        context = {
        'data': Appointment.objects.all().order_by('date')
        }
        return render(request, 'appointment_search.html', context)
    context = {
        'data': Appointment.objects.all().order_by('date')
    }
    return render(request, 'appointment_search.html', context)

def AppointmentLogsView(request):
    context = {
        'data': ChangeLog.objects.all().order_by('-date_logged')
    }
    return render(request, 'changelogs_list.html', context)
