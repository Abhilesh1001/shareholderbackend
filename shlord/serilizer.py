from rest_framework import serializers
from .models import Person,LoanInt,LoanColl,ShareHolder,RDColl,RDInt,StaffSalary,Partuclars,FixedDeposite,Asset


class PersonSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class ShareHolderFunsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ShareHolder
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class ShareHolderFunsDataDisSerializer(serializers.Serializer):
    sh_name = serializers.CharField(source='person.name')
    Sh_id = serializers.CharField(source='person.person_id')
    shf_id = serializers.IntegerField()
    amount_credit = serializers.DecimalField(max_digits=10, decimal_places=3,default=0.0, allow_null=True)
    amount_Debit = serializers.DecimalField(max_digits=10, decimal_places=3, default=0.0, allow_null=True)
    collection_date = serializers.DateTimeField(allow_null=True)
    time = serializers.DateTimeField()
    particulars = serializers.CharField()

class SerilzerHOlderFund(serializers.Serializer):
    shf_id = serializers.IntegerField()
    name = serializers.CharField()
    totalInvested = serializers.FloatField()


class RdIntersetOrignalSerilizer(serializers.ModelSerializer):
    class Meta:
        model = RDInt
        fields = '__all__'



class RdIntersetSerilizer(serializers.ModelSerializer):
    person_name= serializers.CharField(source='person.name')
    person_id= serializers.IntegerField(source='person.person_id')
    class Meta:
        model = RDInt
        fields =['rd_id' ,'person_name','person_id','start_date','closing_date','is_active','duration','interest_rate']


class RDColloectionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = RDColl
        fields = '__all__'


class RDCollectionDataallSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source='rd_interest.person.name')
    person_id = serializers.IntegerField(source='rd_interest.person.person_id')
    duration = serializers.IntegerField(source='rd_interest.duration')
    interest = serializers.DecimalField(source='rd_interest.interest_rate', max_digits=10, decimal_places=3)
    start_date = serializers.DateTimeField(source='rd_interest.start_date')
    closing_date = serializers.DateTimeField(source='rd_interest.closing_date')
    is_active = serializers.BooleanField(source='rd_interest.is_active')
    rd_id  = serializers.IntegerField(source='rd_interest.rd_id')

    class Meta:
        model = RDColl
        fields = ['rd_interest', 'person_name', 'duration', 'interest', 'is_active', 'start_date', 'closing_date', 'person_id', 'amount_collected', 'usersf', 'remarks', 'collection_date','rd_id']


class RDCollectionDataSerializer(serializers.ModelSerializer):
    person_name = serializers.CharField(source='rd_interest.person.name')
    person_id = serializers.IntegerField(source='rd_interest.person.person_id')

    class Meta:
        model = RDColl
        fields = ['rd_interest', 'person_name', 'person_id', 'amount_collected', 'usersf', 'remarks', 'collection_date']


class LaonaAmountSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LoanInt
        fields = '__all__'


class LaonaAmountIntrestSerilizer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(source='person.person_id')
    person_name = serializers.CharField(source='person.name')

    class Meta:
        model = LoanInt
        fields = ['loan_id', 'person_id', 'person_name', 'loan_amount', 'usersf', 'remarks', 'is_active', 'time', 'start_date', 'days', 'duration', 'closing_date', 'interest_rate']

class LoanCollectionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LoanColl
        fields = '__all__'


class LoanCollectionDataallSerializer(serializers.ModelSerializer):

    person_name= serializers.CharField(source='loan_intrest.person.name')
    person_id = serializers.IntegerField(source='loan_intrest.person.person_id')
    loan_amount = serializers.IntegerField(source='loan_intrest.loan_amount')
    is_active = serializers.BooleanField(source='loan_intrest.is_active')
    duration= serializers.IntegerField(source='loan_intrest.duration')
    start_date = serializers.DateTimeField(source='loan_intrest.start_date')
    closing_date = serializers.CharField(source='loan_intrest.closing_date')
    interest = serializers.IntegerField(source='loan_intrest.interest_rate')
    loan_id = serializers.IntegerField(source='loan_intrest.loan_id')
    class Meta:
        model = LoanColl
        fields = ['person_name','person_id','loan_amount','is_active','duration','start_date','closing_date','interest','loan_intrest','collection_date','amount_collected','remarks','loan_id']

class LoanCollectionDataallSerializerViewData(serializers.ModelSerializer):
    person_name = serializers.CharField(source='loan_intrest.person.name')
    person_id = serializers.IntegerField(source='loan_intrest.person.person_id')
    loan_amount = serializers.IntegerField(source='loan_intrest.loan_amount')
    is_active = serializers.BooleanField(source='loan_intrest.is_active')
    duration = serializers.IntegerField(source='loan_intrest.duration')
    start_date = serializers.DateTimeField(source='loan_intrest.start_date')
    closing_date = serializers.CharField(source='loan_intrest.closing_date')
    interest = serializers.IntegerField(source='loan_intrest.interest_rate')
    loan_id = serializers.IntegerField(source='loan_intrest.loan_id')
    # collection_date = serializers.DateTimeField('collection_date')

    class Meta:
        model = LoanColl
        fields = [
            'loan_collection_id',
            'person_name',
            'person_id',
            'loan_amount',
            'is_active',
            'duration',
            'start_date',
            'closing_date',
            'interest',
            'loan_intrest',
            'collection_date',
            'amount_collected',
            'remarks',
            'loan_id'
        ]


class LoanCollectionDataallSerializer(serializers.ModelSerializer):

    person_name= serializers.CharField(source='loan_intrest.person.name')
    person_id = serializers.IntegerField(source='loan_intrest.person.person_id')
    loan_amount = serializers.IntegerField(source='loan_intrest.loan_amount')
    is_active = serializers.BooleanField(source='loan_intrest.is_active')
    duration= serializers.IntegerField(source='loan_intrest.duration')
    start_date = serializers.DateTimeField(source='loan_intrest.start_date')
    closing_date = serializers.CharField(source='loan_intrest.closing_date')
    interest = serializers.IntegerField(source='loan_intrest.interest_rate')
    loan_id = serializers.IntegerField(source='loan_intrest.loan_id')
    class Meta:
        model = LoanColl
        fields = ['person_name','person_id','loan_amount','is_active','duration','start_date','closing_date','interest','loan_intrest','collection_date','amount_collected','remarks','loan_id']


class LoanCollectionDataSerializer(serializers.ModelSerializer):
    person_name= serializers.CharField(source='loan_intrest.person.name')
    person_id = serializers.IntegerField(source='loan_intrest.person.person_id')
    class Meta:
        model = LoanColl
        fields = ['person_name','person_id','loan_intrest','collection_date','amount_collected','remarks','usersf']


class StaffSerilizer(serializers.ModelSerializer):
    class Meta:
        model = StaffSalary
        fields = '__all__'

class ParticularSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Partuclars
        fields = '__all__'


class FixedDepositeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = FixedDeposite
        fields = '__all__'


class AssetSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Asset 
        fields = '__all__'


class StaffSerilizerwithname(serializers.ModelSerializer):
    person_name = serializers.CharField(source='person.name')
    person_id = serializers.IntegerField(source='person.person_id')
    class Meta:
        model = StaffSalary
        fields = ['sd_id','person_name','person_id','time','amount_Debit','collection_date','remarks']


class FixedDepositeName(serializers.ModelSerializer):
    person_name = serializers.CharField(source='person.name')
    person_id = serializers.IntegerField(source='person.person_id')
    class Meta:
        model = FixedDeposite
        fields = ['fd_id','person_name','person_id','time','usersf','amount_Debit','amount_credit','collection_date','start_date','closing_date','duration','interest_rate','is_active']


class ShareHolderFunsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareHolder
        fields = '__all__'


