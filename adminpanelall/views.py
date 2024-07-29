from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

# Create your views here.

def index(request):
    return HttpResponse('ok')


from rest_framework import viewsets

from cusauth.models import  Company, Role, User, ProfileUpdate, UserRole
from shlord.models import ShareHolder,RDInt, RDColl, LoanInt, LoanColl, StaffSalary, Partuclars, FixedDeposite, Asset, Person

from .serializers import (
    CompanySerializer, RoleSerializer, UserSerializer, ProfileUpdateSerializer,
    UserRoleSerializer, PersonSerializer, ShareHolderSerializer, RDIntSerializer,
    RDCollSerializer, LoanIntSerializer, LoanCollSerializer, StaffSalarySerializer,
    PartuclarsSerializer, FixedDepositeSerializer, AssetSerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileUpdateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ProfileUpdate.objects.all()
    serializer_class = ProfileUpdateSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class ShareHolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = ShareHolder.objects.all()
    serializer_class = ShareHolderSerializer

class RDIntViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = RDInt.objects.all()
    serializer_class = RDIntSerializer

class RDCollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = RDColl.objects.all()
    serializer_class = RDCollSerializer

class LoanIntViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = LoanInt.objects.all()
    serializer_class = LoanIntSerializer

class LoanCollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = LoanColl.objects.all()
    serializer_class = LoanCollSerializer

class StaffSalaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = StaffSalary.objects.all()
    serializer_class = StaffSalarySerializer

class PartuclarsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Partuclars.objects.all()
    serializer_class = PartuclarsSerializer

class FixedDepositeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = FixedDeposite.objects.all()
    serializer_class = FixedDepositeSerializer

class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer





