from django.shortcuts import render,HttpResponse
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from cusauth.models import User,Role

# Create your views here.

def authview(request):
    return HttpResponse('auth view change')
    
from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serilizers import UserRegestrationSerilizer,UserLoginSerilizer,UserProfileSerilizer,ChangePasswordSerilizer,SendPasswordResetEmailSerilizer,UserPasswordResetPasswordreset,UserProfileSErilizer,ProfileUpdateSerializer,UserProfileSerializer,RoleSerializer,AssignRoleSerializer,UserSerializer
from django.contrib.auth import login,authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import ProfileUpdate
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import api_view

# Create your views here.

# Token generation

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...
        
        return  token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data
        user = serializer.user
        # Customize your response format here
        response_data = {
            'token' : tokens,
            'msg': 'Login Success',
            'status' : status.HTTP_200_OK
        }
       
        if user is not None:
                return Response(response_data)
        else: 
            return Response({'errors':{'non_fields_errors':['Email or password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
    



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        'refresh':  refresh_token,
        'access': access_token,
    }




class UserRegestrationView(APIView):
    renderer_classes=[UserRenderer]
    
    def post(self,request,format=None):
        serilizer = UserRegestrationSerilizer(data=request.data) 
        # print(serilizer)  
        if serilizer.is_valid(raise_exception=True):
            user =serilizer.save()  
            return Response({'msg':"Regestration success"},status=status.HTTP_201_CREATED)
        
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serilizers = UserLoginSerilizer(data=request.data)
        print('error')
        print(serilizers)
        if serilizers.is_valid(raise_exception=True):
            email = serilizers.data.get('email')
            password = serilizers.data.get('password')
            user=authenticate(email=email,password=password)
            token=get_tokens_for_user(user)
            if user is not None:
                return Response({'token':token,'msg':'Login Successs'},status=status.HTTP_200_OK)
            else: 
                return Response({'errors':{'non_fields_errors':['Email or password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
        return Response(serilizers.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serilzer = UserProfileSerilizer(request.user)
        return Response(serilzer.data,status=status.HTTP_200_OK)
    


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serilizer = ChangePasswordSerilizer(data=request.data,context = {'user':request.user})
        if serilizer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successufully'},status=status.HTTP_200_OK)

        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
class SendPasswordEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serilizer = SendPasswordResetEmailSerilizer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send Please check your Email'},status=status.HTTP_200_OK)
        
        return Response(serilizer.errors,status=status.HTTP_400)



class UserPassewordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid,token,format=None):
        print('uidhome',uid)
        serilizers = UserPasswordResetPasswordreset(data=request.data,context ={'uid':uid,'token':token})
        if serilizers.is_valid(raise_exception=True):
            return Response({'msg':'Pasword Reset Sucefully'},status=status.HTTP_200_OK)
        return Response(serilizers.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    renderer_classes = [UserRenderer] 

    def get(self, request, format=None):
        profiles = ProfileUpdate.objects.all()
        serializer = UserProfileSerializer(profiles, many=True) 
        return Response(serializer.data)



class ProfileUpdateAPIView(APIView):
    def get_object(self, user):
        try:
            return ProfileUpdate.objects.get(user=user)
        except ProfileUpdate.DoesNotExist:
            return None

    def get(self, request, user):
        profile = self.get_object(user)
        if profile:
            serializer = ProfileUpdateSerializer(profile)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user):
        profile = self.get_object(user)
        if profile:
            serializer = ProfileUpdateSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user):
        profile = self.get_object(user)
        if profile:
            serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)




# Permissions classes 


class ListPermissionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        permissions = Permission.objects.all().values('id', 'name', 'codename', 'content_type__model')
        return Response(permissions)

class AssignPermissionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = User.objects.get(id=request.data['user_id'])
        permission = Permission.objects.get(id=request.data['permission_id'])
        user.user_permissions.add(permission)
        return Response({'status': 'permission assigned'})

class RevokePermissionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = User.objects.get(id=request.data['user_id'])
        permission = Permission.objects.get(id=request.data['permission_id'])
        user.user_permissions.remove(permission)
        return Response({'status': 'permission revoked'})



# roleview 
class ListRolesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    

class AssignRoleView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data['user_id'])
            role = Role.objects.get(id=serializer.validated_data['role_id'])
            user.roles.add(role)  # Add the role to the user
            for perm in role.permissions.all():
                user.user_permissions.add(perm)  # Add the permissions of the role to the user
            user.save()
            return Response({'status': 'role assigned'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    




# for perticular copmpany permissions 



class IsCompanyAdminUser(IsAdminUser):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_authenticated and request.user.is_active and request.user.company == view.get_company(request)

class ListPermissionsCompanyView(APIView):
    permission_classes = [IsCompanyAdminUser]

    def get_company(self, request):
        return request.user.company

    def get(self, request):
        permissions = Permission.objects.filter(
            content_type__app_label__in=[
                'cusauth',
                'shlord',  # Replace with the actual app names you want to filter by
            ]
        ).values('id', 'name', 'codename', 'content_type__model')
        return Response(permissions)

class AssignPermissionCompanyView(APIView):
    permission_classes = [IsCompanyAdminUser]

    def get_company(self, request):
        return request.user.company

    def post(self, request):
        user = User.objects.get(id=request.data['user_id'])
        if user.company != request.user.company:
            return Response({'error': 'You can only assign permissions to users within your company.'}, status=status.HTTP_403_FORBIDDEN)

        permission = Permission.objects.get(id=request.data['permission_id'])
        user.user_permissions.add(permission)
        return Response({'status': 'permission assigned'})

class RevokePermissionCompanyView(APIView):
    permission_classes = [IsCompanyAdminUser]

    def get_company(self, request):
        return request.user.company

    def post(self, request):
        user = User.objects.get(id=request.data['user_id'])
        if user.company != request.user.company:
            return Response({'error': 'You can only revoke permissions from users within your company.'}, status=status.HTTP_403_FORBIDDEN)

        permission = Permission.objects.get(id=request.data['permission_id'])
        user.user_permissions.remove(permission)
        return Response({'status': 'permission revoked'})

class ListRolesCompanyView(APIView):
    permission_classes = [IsCompanyAdminUser]

    def get_company(self, request):
        return request.user.company

    def get(self, request):
        roles = Role.objects.filter(company=request.user.company)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class AssignRoleCompanyView(APIView):
    permission_classes = [IsCompanyAdminUser]

    def get_company(self, request):
        return request.user.company

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data['user_id'])
            if user.company != request.user.company:
                return Response({'error': 'You can only assign roles to users within your company.'}, status=status.HTTP_403_FORBIDDEN)

            role = Role.objects.get(id=serializer.validated_data['role_id'])
            if role.company != request.user.company:
                return Response({'error': 'You can only assign roles from within your company.'}, status=status.HTTP_403_FORBIDDEN)

            user.roles.add(role)  # Add the role to the user
            for perm in role.permissions.all():
                user.user_permissions.add(perm)  # Add the permissions of the role to the user
            user.save()
            return Response({'status': 'role assigned'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListUsersComapnyView(APIView):
    permission_classes = [IsCompanyAdminUser]

    def get_company(self, request):
        return request.user.company

    def get(self, request):
        users = User.objects.filter(company=request.user.company)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    








        





