import csv
from django.http import HttpResponse, HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model
from django.core.exceptions import PermissionDenied

def export_as_csv(qs, file_name=None, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    if not file_name:
        file_name = slugify(model.__name__)
    else:
        file_name = slugify(file_name)
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % file_name
    writer = csv.writer(response)
    
	# Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
#    if headers[0] == 'action_checkbox':
#		del headers[0]        
    writer.writerow(headers)
    
	# Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            val = getattr(obj, field)
            if callable(val):
                val = val()
            row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

