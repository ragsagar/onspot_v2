from django.contrib import admin
from books.models import Agent, PolicyIssue, Branch, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#To extend the builtin user model
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)


# Model Admin Classes
# To include the following models in admin interface
class PolicyIssueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PolicyIssue._meta.fields]

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        if request.user.get_profile().is_employee:
            obj.branch = request.user.get_profile().branch
        obj.agent_percentage = obj.agent.percentage
        # agent commission will be calculated only if policy_no is not empty
        if obj.policy_no:
            obj.agent_commission = (obj.premium_amount * \
                    (obj.agent_percentage / 100)) - obj.customer_discount
        obj.save()

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.get_profile().is_employee:
            self.model.branch.field.editable = False
        else:
            self.model.branch.field.editable = True
        return super(PolicyIssueAdmin, self).add_view(request, form_url)
        
    #To enable Branch selection for superuser
    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    if db_field.name == "branch":
    #        if not request.user.is_superuser:
    #            #import pdb; pdb.set_trace()
    #            db_field.editable = False
    #        else:
    #            db_field.editable = True
    #    return super(PolicyIssueAdmin, self).formfield_for_foreignkey(db_field,
    #            request, **kwargs)
        
class AgentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Agent._meta.fields]

    
class BranchAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Branch._meta.fields]

admin.site.register(PolicyIssue, PolicyIssueAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Branch, BranchAdmin)
