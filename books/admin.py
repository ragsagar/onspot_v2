from django.contrib import admin
from books.models import Agent, PolicyIssue, Branch



# Model Admin Classes
# To include the following models in admin interface


class PolicyIssueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PolicyIssue._meta.fields if \
            field.editable]

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.agent_percentage = obj.agent.percentage
        obj.agent_commission = (obj.premium_amount * \
                (obj.agent_percentage / 100)) - obj.customer_discount
        obj.save()
        
class AgentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Agent._meta.fields]

    
class BranchAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Branch._meta.fields]


admin.site.register(PolicyIssue, PolicyIssueAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Branch, BranchAdmin)
