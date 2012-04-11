from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Branch(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=5,decimal_places=2)

    def __unicode__(self):
        return self.name

class PolicyIssue(models.Model):
    BUSINESS_TYPE_CHOICES = (("New", "New"), ("Rollover", "Rollover"),
    ("Renewal", "Renewal"))
    # following two fields will be helpful in future
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    added_by = models.ForeignKey(User, editable=False)
    agent = models.ForeignKey(Agent)
    branch = models.ForeignKey(Branch) 
    # columns copied from excel statement
    policy_no = models.CharField(max_length=30, blank=True) 
    transaction_id = models.CharField(max_length=50, editable=False, blank=True)
    endorsement = models.CharField(max_length=20, editable=False, blank=True)
    policy_date = models.DateTimeField(default=timezone.now, editable=False,
            blank=True)
    branch_code = models.CharField(max_length=10, editable=False, blank=True)
    product_code = models.CharField(max_length=10, editable=False, blank=True)
    product_name = models.CharField(max_length=100, editable=False, blank=True)
    group_name = models.CharField(max_length=50, editable=False, blank=True)
    customer_name = models.CharField(max_length=50)
    mobile_no = models.IntegerField(max_length=11)
    premium_amount = models.DecimalField(max_digits=12, decimal_places=4)
    agent_code = models.CharField(max_length=12, editable=False, blank=True)
    bas_code = models.CharField(verbose_name="BAS Code", max_length=12,
            editable=False, blank=True)
    business_type = models.CharField(choices=BUSINESS_TYPE_CHOICES,
            max_length=10, editable=False, blank=True)
    discount = models.DecimalField(max_digits=9, decimal_places=4,
            editable=False, blank=True, null=True)
    irda_percentage = models.DecimalField(verbose_name="IRDA (%)",max_digits=12,
            decimal_places=4, editable=False, blank=True, null=True)
    bas_percentage = models.DecimalField(verbose_name="BAS (%)", max_digits=12,
            decimal_places=4, editable=False, blank=True, null=True)
    agency_commission = models.DecimalField(max_digits=10, decimal_places=4,
            editable=False, blank=True, null=True)
    bas_commission = models.DecimalField(verbose_name="BAS Commission",
            max_digits=10, decimal_places=4, editable=False, blank=True, null=True)
    process_type = models.CharField(max_length=20, editable=False, blank=True)
    add_irda_percent = models.DecimalField(max_digits=12, decimal_places=4,
            editable=False, blank=True, null=True)
    add_bas_percent = models.DecimalField(max_digits=12, decimal_places=4,
            editable=False, blank=True, null=True)
    add_irda_commission = models.DecimalField(max_digits=12, decimal_places=4,
            editable=False, blank=True, null=True)
    add_bas_commission = models.DecimalField(max_digits=12, decimal_places=4,
            editable=False, blank=True, null=True)
    add_remark = models.CharField(max_length=100, editable=False, blank=True)
    add_pay_date = models.CharField(max_length=20, editable=False, blank=True)
    ops_ref_num = models.CharField(max_length=30, editable=False, blank=True)
    vehicle_make = models.CharField(max_length=40)
    vehicle_model = models.CharField(max_length=50)
    vehicle_no = models.CharField(max_length=30, blank=True)
    rsd = models.CharField(max_length=20, editable=False, blank=True)
    process_date = models.CharField(max_length=20, editable=False, blank=True)
    # fields required that are not with reliance statement
    od_premium = models.DecimalField(verbose_name="OD Premium", max_digits=12,
            decimal_places=4, default=0)
    customer_discount = models.DecimalField(default=0, max_digits=10,
            decimal_places=4, blank=True, null=True)
    # following fields will be automatically populated when object is saved
    agent_percentage = models.DecimalField(max_digits=5, decimal_places=2,
            editable=False, blank=True, null=True)
    agent_commission = models.DecimalField(max_digits=15, decimal_places=4,
            editable=False, blank=True, null=True)
    # Not sure if the following field is required 
    od_discount = models.DecimalField(max_digits=10, decimal_places=4,
            blank=True, null=True)
    cover_note_no = models.CharField(max_length=30, blank=True)


    def __unicode__(self):
        return self.policy_no

class UserProfile(models.Model):
    "Extending the builtin user model"
    branch = models.ForeignKey(Branch,blank=True,null=True)
    is_employee = models.BooleanField(verbose_name="Employee status",
            default=True, help_text="Dont select this if you are an admin")
    user = models.ForeignKey(User, unique=True)

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)
#
#post_save.connect(create_user_profile, sender=User)

    



