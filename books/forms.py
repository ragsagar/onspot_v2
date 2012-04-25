from django import forms
from books.models import Agent
import calendar


class AgentStatementSelectForm(forms.Form):
    AGENT_CHOICES = [(obj.id, obj.name) for obj in Agent.objects.all()]
    MONTH_CHOICES = [(0, None)] + [(i, calendar.month_name.__getitem__(i)) \
            for i in range(1,13)]
    agent = forms.ChoiceField(choices=AGENT_CHOICES, required=True)
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
