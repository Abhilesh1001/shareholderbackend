from django.contrib import admin
from .models import Person,LoanInt,LoanColl,ShareHolder,RDColl,RDInt,StaffSalary,Partuclars,FixedDeposite,Asset

# Register your models here.


@admin.register(Person)
class AdminShareHolderName(admin.ModelAdmin):
    list_display = ['person_id','name','email','pan_no','time']

@admin.register(ShareHolder)
class AdminSShareHolderFuns(admin.ModelAdmin):
    list_display = ['shf_id','person','time','amount_credit','amount_Debit','collection_date','particulars']

@admin.register(RDInt)
class AdminRdintrest(admin.ModelAdmin):
    list_display = ['rd_id','person','time','start_date','closing_date','is_active','duration','interest_rate','usersf']


@admin.register(RDColl)
class AdminRdcollection(admin.ModelAdmin):
    list_display = ['rd_collection_id','rd_interest','collection_date','time','amount_collected','remarks']


@admin.register(LoanInt)
class AdminLoanAmount(admin.ModelAdmin): 
    list_display = ['loan_id' ,'person', 'loan_amount', 'remarks','is_active','time','start_date','days','duration','closing_date','interest_rate']


@admin.register(LoanColl)
class AdminLoanCollection(admin.ModelAdmin):
    list_display = ['loan_collection_id','loan_intrest','time','collection_date','amount_collected','remarks']

@admin.register(StaffSalary)
class AdminLoanStaffSalary(admin.ModelAdmin):
    list_display = ['sd_id','person','time','usersf','collection_date','remarks']
    
@admin.register(Partuclars)
class AdminLoanParicular(admin.ModelAdmin):
    list_display = ['p_id','time','usersf','amount_Debit','amount_credit','particulars']


@admin.register(FixedDeposite)
class AdminFixedDeposite(admin.ModelAdmin):
    list_display = ['fd_id','time','usersf','amount_Debit','amount_credit','collection_date','start_date','closing_date','duration','interest_rate','is_active','person']
@admin.register(Asset)
class AdminAsset(admin.ModelAdmin):
    list_display = ['asset_no','time','usersf','amount_Debit','debit_date']


