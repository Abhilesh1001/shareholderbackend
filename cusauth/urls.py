from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', views.authview),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authreg/',views.UserRegestrationView.as_view()),
    path('authlogin/',views.MyTokenObtainPairView.as_view()),
    path('authuserpro/',views.ProfileView.as_view()),
    path('changepassword/',views.UserChangePasswordView.as_view()),
    path('send-reset-password/',views.SendPasswordEmailView.as_view()),
    path('send-reset-password/<uid>/<token>/',views.UserPassewordResetView.as_view()),
    path('profile/<str:user>/', views.ProfileUpdateAPIView.as_view(), name='profile-detail'),
    path('profile/', views.UserProfileView.as_view(), name='profile-detail'),


# user permissions 
    path('api/permissions/', views.ListPermissionsView.as_view(), name='list_permissions'),
    path('api/permissions/assign/',views.AssignPermissionView.as_view(), name='assign_permission'),
    path('api/permissions/revoke/', views.RevokePermissionView.as_view(), name='revoke_permission'),


#    Role Permissions 
    path('api/roles/', views.ListRolesView.as_view(), name='list_roles'),
    path('api/roles/assign/', views.AssignRoleView.as_view(), name='assign_role'),
    path('api/users/', views.ListUsersView.as_view(), name='list_users'),


# as per company 
    path('api/permissions/company', views.ListPermissionsCompanyView.as_view(), name='list_permissions_company'),
    path('api/permissions/assign/company',views.AssignPermissionCompanyView.as_view(), name='assign_permission/comapny'),
    path('api/permissions/revoke/company', views.RevokePermissionCompanyView.as_view(), name='revoke_permission_company'),


# as per company 
    path('api/roles/company', views.ListRolesCompanyView.as_view(), name='list_roles_company'),
    path('api/roles/assign/company', views.AssignRoleCompanyView.as_view(), name='assign_role_company'),
    path('api/users/company', views.ListUsersComapnyView.as_view(), name='list_users_company'),


]

