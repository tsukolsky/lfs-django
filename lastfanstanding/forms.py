from django import forms
from .models import LFSTeam

class TeamPickerForm(forms.Form):
    my_choices = (
        ('value1', 'Display Value 1'),
        ('value2', 'Display Value 2'),
        ('value3', 'Display Value 3'),
    )
    my_field = forms.ChoiceField(choices=my_choices)
