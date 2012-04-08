from django.contrib import admin
from books.models import Agent, PolicyIssue



# Model Admin Classes
# To include the following models in admin interface


class PolicyIssueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PolicyIssue._meta.fields]

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()
        
class AgentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Agent._meta.fields]


admin.site.register(PolicyIssue, PolicyIssueAdmin)
admin.site.register(Agent, AgentAdmin)
