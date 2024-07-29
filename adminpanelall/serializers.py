from rest_framework import serializers
from cusauth.models import Company, Role, User, ProfileUpdate, UserRole
     
from shlord.models import Person, ShareHolder, RDInt, RDColl, LoanInt, LoanColl, StaffSalary, Partuclars, FixedDeposite, Asset

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUpdate
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class ShareHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareHolder
        fields = '__all__'

class RDIntSerializer(serializers.ModelSerializer):
    class Meta:
        model = RDInt
        fields = '__all__'

class RDCollSerializer(serializers.ModelSerializer):
    class Meta:
        model = RDColl
        fields = '__all__'

class LoanIntSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanInt
        fields = '__all__'

class LoanCollSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanColl
        fields = '__all__'

class StaffSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSalary
        fields = '__all__'

class PartuclarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partuclars
        fields = '__all__'

class FixedDepositeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedDeposite
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
