from books.models import PolicyIssue, Agent
from books.forms import AgentStatementSelectForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
import datetime, calendar


@staff_member_required
def AgentStatement(request, agent_id, month=None):
    agent_obj = Agent.objects.get(id=agent_id)
    total_commission = 0
    if month:
        objects = \
                PolicyIssue.objects.filter(policy_date__month=month,agent=agent_obj)
        month_name = calendar.month_name.__getitem__(int(month))
    else:
        objects = PolicyIssue.objects.filter(agent=agent_obj)
        month_name = None
    for item in objects:
        if item.agent_commission:
            total_commission = total_commission + item.agent_commission
    return render_to_response("agent_statement_report.html",{ 'agent_name':agent_obj.name,
        'objects':objects, 'agent_id':agent_obj.id,
        'total_commission':total_commission, 'month': month_name })

@staff_member_required
def AgentStatementSelect(request):
    if request.method == 'POST':
        form = AgentStatementSelectForm(request.POST)
        if form.is_valid():
            agent_id = form.cleaned_data['agent']
            month = form.cleaned_data['month']
            if int(month):
                return \
                        HttpResponseRedirect(reverse('AgentStatementSelect')+agent_id+'/'+month+'/')
            else:
                return \
                        HttpResponseRedirect(reverse('AgentStatementSelect')+agent_id+'/')
    else:
        form = AgentStatementSelectForm()
        return render_to_response('agent_statement_select.html', {'form': \
                    form}, context_instance=RequestContext(request, {}))


