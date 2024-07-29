
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, RoleViewSet, UserViewSet, ProfileUpdateViewSet, UserRoleViewSet,
    PersonViewSet, ShareHolderViewSet, RDIntViewSet, RDCollViewSet, LoanIntViewSet,
    LoanCollViewSet, StaffSalaryViewSet, PartuclarsViewSet, FixedDepositeViewSet,
    AssetViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)
router.register(r'profileupdates', ProfileUpdateViewSet)
router.register(r'userroles', UserRoleViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'shareholders', ShareHolderViewSet)
router.register(r'rdints', RDIntViewSet)
router.register(r'rdcolls', RDCollViewSet)
router.register(r'loanints', LoanIntViewSet)
router.register(r'loancolls', LoanCollViewSet)
router.register(r'staffsalaries', StaffSalaryViewSet)
router.register(r'partuclars', PartuclarsViewSet)
router.register(r'fixeddeposits', FixedDepositeViewSet)
router.register(r'assets', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]