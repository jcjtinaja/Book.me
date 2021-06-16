from django import forms

class AppointmentForm(forms.Form):
    date = forms.DateField(
        label='Date',
        required=True,
        input_formats=['%Y-%m-%d'],
        widget= forms.TextInput(attrs={'type':'date', 'placeholder':'YYYY-MM-DD (e.g. 2021-12-01)', }))
    time_in = forms.TimeField(
        required=True,
        input_formats=['%H:%M'],
        widget= forms.TextInput(attrs={'placeholder':'HH:MM (e.g. 09:00)'}))
    time_out = forms.TimeField(
        required=True,
        input_formats=['%H:%M'],
        widget= forms.TextInput(attrs={'placeholder':'HH:MM (e.g. 17:00)'}))
    last_name = forms.CharField(required=True,max_length=50)
    first_name = forms.CharField(required=True,max_length=50)
    comment = forms.CharField(label='Comment:',required=False)

