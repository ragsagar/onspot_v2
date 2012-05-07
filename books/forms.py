from django import forms
from books.models import Agent
from datetime import datetime
import calendar


class AgentStatementSelectForm(forms.Form):
    AGENT_CHOICES = [(obj.id, obj.name) for obj in Agent.objects.all()]
    MONTH_CHOICES = [(0, None)] + [(i, calendar.month_name.__getitem__(i)) \
            for i in range(1,13)]
    agent = forms.ChoiceField(choices=AGENT_CHOICES, required=True)
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)

class UploadExcelFileForm(forms.Form):
    MONTH_CHOICES = [ (i, calendar.month_name.__getitem__(i)) for i in \
            range(1,13) ]
    YEAR_CHOICES = [ (i, i) for i in reversed(range(2000, \
            int(datetime.now().year) + 1)) ]
    file = forms.FileField(required=True)
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True)
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=True)
    
