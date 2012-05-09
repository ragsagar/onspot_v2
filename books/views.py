from books.models import PolicyIssue, Agent
from books.forms import AgentStatementSelectForm, UploadExcelFileForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from decimal import Decimal
from excel_access import ExcelStatement
from django.core import urlresolvers
import datetime, calendar, mimetypes


@staff_member_required
@permission_required("books.delete_policyissue")
def AgentStatement(request, agent_id, year=None, month=None):
    """ Fetches agent statement for particular month and displays it as a
    table"""
    agent_obj = Agent.objects.get(id=agent_id)
    total_commission = 0
    if month:
        objects = \
                PolicyIssue.objects.filter(policy_date__month=month, \
                policy_date__year=year, agent=agent_obj)
        month_name = calendar.month_name.__getitem__(int(month))
    elif year:
        objects = PolicyIssue.objects.filter(policy_date__year=year, \
                agent=agent_obj)
        month_name = None
    else:
        objects = PolicyIssue.objects.filter(agent=agent_obj)
        month_name = None
    for item in objects:
        if item.agent_commission:
            total_commission = total_commission + item.agent_commission
    return render_to_response("agent_statement_report.html",{ 'agent_name':agent_obj.name,
        'objects':objects, 'agent_id':agent_obj.id,
        'total_commission':total_commission, 'month': month_name, 'year': year })

@staff_member_required
@permission_required("books.delete_policyissue")
def AgentStatementSelect(request):
    """ Displays form to select agent and month """
    if request.method == 'POST':
        form = AgentStatementSelectForm(request.POST)
        if form.is_valid():
            agent = form.cleaned_data['agent']
            month = int(form.cleaned_data['month'])
            year = int(form.cleaned_data['year'])
            if month:
                return HttpResponseRedirect(reverse('AgentStatementURL',\
                        kwargs={"agent_id": int(agent.id), "year": year,
                            "month": month}))
            else:
                return HttpResponseRedirect(reverse('AgentStatementURL',\
                        kwargs={"agent_id": int(agent.id), "year": year}))
    else:
        form = AgentStatementSelectForm()
        return render_to_response('agent_statement_select.html', {'form': \
                    form}, context_instance=RequestContext(request, {}))


@staff_member_required
@permission_required("books.delete_policyissue")
def UploadExcelStatement(request):
    """ Display form to upload excel statement and select month """
    error_message = ""
    if request.method == "POST":
        return HandleExcelStatement(request)
    else:
        form = UploadExcelFileForm()
        return render_to_response("upload_excel_statement.html", {"form":form,
            "error_message": error_message}, context_instance=RequestContext(request, {}))


def HandleExcelStatement(request):
    """ Generates seperated excel statements and provides option to download
    it. Also automatically populates the empty fields in PolicyIssue
    database"""
    if 'our' in request.POST:
        workbook_object = request.session['our_workbook']
        fname = "our_statement" + "_" + request.session['fname'] + ".xls"
        response = HttpResponse(mimetype="application/ms-excel")
        response['Content-Disposition'] = "attatchment; filename=%s" % fname
        workbook_object.save(response)
        return response

    elif 'others' in request.POST:
        workbook_object = request.session['others_workbook']
        fname = "others_statement" + "_" + request.session['fname'] + ".xls"
        response = HttpResponse(mimetype="application/ms-excel")
        response['Content-Disposition'] = "attatchment; filename=%s" % fname
        workbook_object.save(response)
        return response

    form = UploadExcelFileForm(request.POST, request.FILES)
    try:
        uploaded_file = request.FILES['file']
    except:
        error_message = "Please select a file before pressing generate buttton"
    if form.is_valid():
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        month_name = calendar.month_name.__getitem__(int(month)) #for filename
        objects = PolicyIssue.objects.filter(policy_date__month=month,
                policy_date__year=year)
        policy_numbers = [ obj.policy_no for obj in objects if obj.policy_no ]
        excel_statement = ExcelStatement(uploaded_file, policy_numbers)
        our_workbook, others_workbook = \
                excel_statement.generate_statements()

        #Finding objects with error in policy_no field in PolicyIssue database
        error_list = excel_statement.get_unknown_policynums()
        error_objects = []
        for error_num in error_list:
            error_objects.append(PolicyIssue.objects.get(policy_no=error_num))
        
        #Populating the fields in PolicyIssue database from uploaded file
        for policy_number in policy_numbers:
            if policy_number not in error_list:
                values = excel_statement.get_values_with_policynum(policy_number)
                obj = PolicyIssue.objects.get(policy_no=policy_number)
                obj.transaction_id = values[1]
                obj.endorsement = values[2]
                obj.policy_date = \
                        datetime.datetime.utcfromtimestamp((values[3] - 25569) * 86400.0)
                obj.branch_code = values[4]
                obj.product_code = values[5]
                obj.product_name = values[6]
                obj.group_name = values[7]
                obj.customer_name = values[8]
                obj.premium_amount = Decimal(values[9])
                obj.agent_code = values[10]
                obj.bas_code = values[11]
                obj.business_type = values[12]
                obj.discount = Decimal(values[13])
                obj.irda_percentage = Decimal(values[14])
                obj.bas_percentage = Decimal(values[15])
                obj.agency_commission = Decimal(values[16])
                obj.bas_commission = Decimal(values[17])
                obj.process_type = values[18]
                obj.add_irda_percent = Decimal(values[19])
                obj.add_bas_percent = Decimal(values[20])
                obj.add_irda_commission = Decimal(values[21])
                obj.add_bas_commission = Decimal(values[22])
                obj.add_remark = values[23]
                obj.add_pay_date = values[24]
                obj.ops_ref_num = values[25]
                obj.vehicle_make = values[26]
                obj.vehicle_model = values[27]
                obj.rsd = values[28]
                obj.process_date = values[29]
                obj.save()

        request.session['our_workbook'] = our_workbook
        request.session['others_workbook'] = others_workbook
        request.session['fname'] = '_'.join((month_name, year))

        return render_to_response("generate_excel_statement.html", \
                { 'error_objects' : error_objects }, \
                context_instance=RequestContext(request, {}))
    else:
        return render_to_response("upload_excel_statement.html", {"form":form,
            "error_message": error_message}, context_instance=RequestContext(request, {}))



                


        #from django.http import HttpResponse
        #response = HttpResponse(mimetype=f.content_type)
        #response['Content-Disposition'] = 'attachment; filename=%s' % \
                #f.name
        #response.write(f.read())
        #return response
