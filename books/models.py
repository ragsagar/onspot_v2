from django.db import models
from datetime import datetime
from django.contrib.auth.models import User



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
    timestamp = models.DateTimeField(default=datetime.now, editable=False)
    added_by = models.ForeignKey(User, editable=False)
    agent = models.ForeignKey(Agent)
    branch = models.ForeignKey(Branch)
    # columns copied from excel statement
    policy_no = models.CharField(max_length=30, blank=True) 
    transaction_id = models.CharField(max_length=50, editable=False, blank=True)
    endorsement = models.CharField(max_length=20, editable=False, blank=True)
    policy_date = models.DateTimeField(default=datetime.now,
    blank=True)
    branch_code = models.CharField(max_length=10, editable=False, blank=True)
    product_code = models.CharField(max_length=10, editable=False, blank=True)
    product_name = models.CharField(max_length=100, editable=False, blank=True)
    group_name = models.CharField(max_length=50, editable=False, blank=True)
    customer_name = models.CharField(max_length=50)
    mobile_no = models.IntegerField(max_length=11, blank=True)
    premium_amount = models.DecimalField(max_digits=12, decimal_places=4,
            blank=True, null=True)
    agent_code = models.CharField(max_length=12, blank=True)
    bas_code = models.CharField(verbose_name="BAS Code", max_length=12,
            blank=True)
    business_type = models.CharField(choices=BUSINESS_TYPE_CHOICES,
            max_length=10, blank=True)
    discount = models.DecimalField(max_digits=9, decimal_places=4,
            editable=False, blank=True, null=True)
    irda_percentage = models.DecimalField(verbose_name="IRDA (%)",max_digits=12,
            decimal_places=4, blank=True, null=True)
    bas_percentage = models.DecimalField(verbose_name="BAS (%)", max_digits=12,
            decimal_places=4, blank=True, null=True)
    agency_commission = models.DecimalField(max_digits=10, decimal_places=4,
            blank=True, null=True)
    bas_commission = models.DecimalField(verbose_name="BAS Commission",
            max_digits=10, decimal_places=4, blank=True, null=True)
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
    make = models.CharField(max_length=40, editable=False, blank=True)
    model = models.CharField(max_length=50, editable=False, blank=True)
    rsd = models.CharField(max_length=20, editable=False, blank=True)
    process_date = models.CharField(max_length=20, editable=False, blank=True)
    # fields required that are not with reliance statement
    customer_discount = models.DecimalField(default=0, max_digits=10,
            decimal_places=4, blank=True, null=True)
    # following fields will be automatically populated when object is saved
    agent_percentage = models.DecimalField(max_digits=5, decimal_places=2,
            editable=False, blank=True, null=True)
    agent_commission = models.DecimalField(max_digits=15, decimal_places=4,
            editable=False, blank=True, null=True)


    def __unicode__(self):
        return self.policy_no





    



