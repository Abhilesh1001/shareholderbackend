from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cusauth.renderers import UserRenderer
from cusauth.models import User
from .serilizer import PersonSerilizer,ShareHolderFunsSerilizer,ShareHolderFunsDataDisSerializer,SerilzerHOlderFund,RdIntersetOrignalSerilizer,RdIntersetSerilizer,RDColloectionSerilizer,RDCollectionDataallSerializer,RDCollectionDataSerializer,LaonaAmountSerilizer,LaonaAmountIntrestSerilizer,LoanCollectionSerilizer,LoanCollectionDataallSerializer,LoanCollectionDataSerializer,StaffSerilizer ,ParticularSerilizer,FixedDepositeSerilizer,AssetSerilizer,StaffSerilizerwithname,FixedDepositeName,PersonSerializer,ShareHolderFunsSerializer,LoanCollectionDataallSerializerViewData,RDCollectionDataallSerializerViewData
from .models import Person,LoanInt,LoanColl,ShareHolder,RDColl,RDInt,StaffSalary,Partuclars,FixedDeposite,Asset
from collections import defaultdict
from django.utils.timezone import make_aware
from datetime import datetime

# Create your views here.
def index(request):
    return HttpResponse('ok')


class MemberView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()  # Create a mutable copy of the request data
        data['usersf'] = request.user.id  # Set the user field to the current user
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Person added successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        if pk:
            try:
                person = Person.objects.get(pk=pk, usersf__company=request.user.company)
                serializer = PersonSerializer(person)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Person.DoesNotExist:
                return Response({'error': 'Person not found or you do not have permission to access this person.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            persons = Person.objects.filter(usersf__company=request.user.company)
            serializer = PersonSerializer(persons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None, format=None):
        try:
            person = Person.objects.get(pk=pk, usersf__company=request.user.company)
        except Person.DoesNotExist:
            return Response({'error': 'Person not found or you do not have permission to access this person.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()  # Create a mutable copy of the request data
        data['usersf'] = request.user.id  # Ensure the user field is set to the current user
        serializer = PersonSerializer(person, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None, format=None):
        try:
            person = Person.objects.get(pk=pk, usersf__company=request.user.company)
        except Person.DoesNotExist:
            return Response({'error': 'Person not found or you do not have permission to access this person.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()  # Create a mutable copy of the request data
        data['usersf'] = request.user.id  # Ensure the user field is set to the current user
        serializer = PersonSerializer(person, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Person updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShreHolderFundView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()  # Create a mutable copy of the request data
        data['usersf'] = request.user.id  # Set the user field to the current user
        serializer = ShareHolderFunsSerializer(data=data)
        if serializer.is_valid():
            # Check if the person belongs to the same company as the user
            person = Person.objects.get(pk=data['person'])
            if person.usersf.company != request.user.company:
                return Response({'error': 'You do not have permission to add funds for this person.'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            return Response({'msg': 'Data created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        if pk is not None:
            # Ensure that the person belongs to the user's company
            # print('..............ok........')
            try:
                person = Person.objects.get(pk=pk, usersf__company=request.user.company)
            except Person.DoesNotExist:
                return Response({'error': 'Person not found or you do not have permission to access this person.'}, status=status.HTTP_404_NOT_FOUND)
            
            sh = ShareHolder.objects.filter(person=person)
            serializer = ShareHolderFunsDataDisSerializer(sh, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            sh = ShareHolder.objects.filter(person__usersf__company=request.user.company)
            serializer = ShareHolderFunsDataDisSerializer(sh, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None, format=None):
        try:
            sh = ShareHolder.objects.get(shf_id=pk, person__usersf__company=request.user.company)
        except ShareHolder.DoesNotExist:
            return Response({'error': 'ShareHolder not found or you do not have permission to access this ShareHolder.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ShareHolderFunsSerializer(sh, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None, format=None):
        try:
            sh = ShareHolder.objects.get(shf_id=pk, person__usersf__company=request.user.company)
        except ShareHolder.DoesNotExist:
            return Response({'error': 'ShareHolder not found or you do not have permission to access this ShareHolder.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ShareHolderFunsSerializer(sh, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Share Fund updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


def shfview(user):
    # Filter ShareHolder objects based on the user's company
    shf_objects = ShareHolder.objects.filter(person__usersf__company=user.company)

    orignal_pr_line = defaultdict(float)

    for shf_item in shf_objects:
        amount_credit = float(shf_item.amount_credit) if shf_item.amount_credit else 0
        amount_debit = float(shf_item.amount_Debit) if shf_item.amount_Debit else 0
        orignal_pr_line[shf_item.person.person_id] += amount_credit - amount_debit

    dictval = []    
    for item in orignal_pr_line:
        shname = Person.objects.get(person_id=item)
        dict_entry = {
            'shf_id': item,
            'name': shname.name,
            'totalInvested': orignal_pr_line[item]
        }  
        dictval.append(dict_entry) 
    
    return dictval


class CapitalDisclouserview(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        sh=shfview(request.user)
        serilizer =  SerilzerHOlderFund(sh,many= True)
        print(serilizer.data)
        return Response(serilizer.data,status=status.HTTP_200_OK)


class RDintrestView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = RdIntersetOrignalSerilizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'RD Interest Created Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        user_company = request.user.company

        if pk is not None:
            try:
                rdintrest = RDInt.objects.get(rd_id=pk, usersf__company=user_company)
                serializer = RdIntersetSerilizer(rdintrest)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except RDInt.DoesNotExist:
                return Response({'error': 'RD Interest not found or not associated with your company.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            rdintrest = RDInt.objects.filter(usersf__company=user_company)
            serializer = RdIntersetSerilizer(rdintrest, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None, format=None):
        user_company = request.user.company
        try:
            rd = RDInt.objects.get(rd_id=pk, usersf__company=user_company)
            serializer = RdIntersetOrignalSerilizer(rd, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RDInt.DoesNotExist:
            return Response({'error': 'RD Interest not found or not associated with your company.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None, format=None):
        user_company = request.user.company
        try:
            rd = RDInt.objects.get(rd_id=pk, usersf__company=user_company)
            serializer = RdIntersetOrignalSerilizer(rd, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'RD Interest Updated Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RDInt.DoesNotExist:
            return Response({'error': 'RD Interest not found or not associated with your company.'}, status=status.HTTP_404_NOT_FOUND)

def merge_by_collection_date(queryset):
        merged_data = {}
        # print('..........')
        for item in queryset:
            # print(item.rd_interest)
            collection_date = item.collection_date.date()  # Extract date part
            rd_intrest_id = item.rd_interest.rd_id
            if (collection_date, rd_intrest_id) not in merged_data:
                merged_data[(collection_date, rd_intrest_id)] = item
            else:
                # If entry with same collection date and rd_intrest exists, add amount
                merged_data[(collection_date, rd_intrest_id)].amount_collected +=item.amount_collected
        return merged_data.values()




class RDcollectionView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        serilizer = RDColloectionSerilizer(data=request.data,many=True)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'RD Intrest Created Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk=None,format=None):
        if pk is not None:
            rd_collections = RDColl.objects.filter(rd_interest=pk)
            merged_data = merge_by_collection_date(rd_collections)
            serilizer = RDCollectionDataallSerializer(merged_data,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
        else:   
            rdintrest =RDColl.objects.all()
            serilizer = RDColloectionSerilizer(rdintrest,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
        
    def put(self,request,pk=None,format=None):
        loan =  RDColl.objects.get(rd_collection_id=pk)
        serilizer = RDColloectionSerilizer(loan,data=request.data) 
        if  serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk=None,format=None):
        loan =  RDColl.objects.get(rd_collection_id=pk)
        serilizer = RDColloectionSerilizer(loan,data=request.data) 
        if  serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'RDcollection Updated Successfully','data':serilizer.data},status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class RDcollectionPerView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        serilizer = RDColloectionSerilizer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'RD Intrest Created Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class RDcollectionViewDate(APIView):
    renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request, pk=None, format=None):
        collection_date_str = request.data.get('collection_date')
        user_company = request.user.company
        
        if not collection_date_str:
            return Response({'error': 'collection_date parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse the date string to a date object
            collection_date = parse_date(collection_date_str)

            if collection_date is None:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)

            # Make the date timezone-aware
            current_timezone = get_current_timezone()
            collection_date = make_aware(datetime.combine(collection_date, datetime.min.time()), current_timezone)
            print("Parsed and timezone-aware date:", collection_date)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if pk is not None:
            rd_collections = RDColl.objects.filter(
                rd_interest=pk,
                collection_date__date=collection_date.date(),
                usersf__company=user_company
            )
            print("Filtered Loan Collections:", rd_collections)
            print("Database Entries:")
            for rd in RDColl.objects.filter(rd_interest=pk):
                print(f"ID: {rd.rd_collection_id}, Collection Date: {rd.collection_date}, Company: {rd.usersf.company}")

            if rd_collections.exists():
                # Process the loan collections as needed, e.g., serialization
                serializer = RDCollectionDataallSerializerViewData(rd_collections, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No loan collections found for the given date.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'pk parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)


    

   
class RDDataAPIView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        start_date = request.data.get('start_date')  # Format: 'YYYY-MM-DD'
        end_date = request.data.get('end_date')      # Format: 'YYYY-MM-DD'
        user = request.user

        # Convert dates to aware datetime objects
        start_date_aware = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date_aware = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))

        # Filter RDColl objects within the specified date range and company
        rd_collections = RDColl.objects.filter(
            collection_date__range=(start_date_aware, end_date_aware),
            usersf__company=user.company
        )

        # Serialize the filtered RD collections
        serializer = RDCollectionDataSerializer(rd_collections, many=True)

        # Organize the serialized data
        organized_data = self.organize_data(serializer.data)

        return Response(organized_data, status=status.HTTP_200_OK)

    def organize_data(self, serialized_data):
        organized_data = {}

        for item in serialized_data:
            rd_interest = item.get('rd_interest')
            amount_collected = item['amount_collected']
            collection_date = item['collection_date']
            person_name = item['person_name']

            # Only process items with all necessary data
            if rd_interest and amount_collected and collection_date:
                formatted_date = collection_date.split('T')[0]
                key = f"{rd_interest}_{person_name}"

                if key not in organized_data:
                    organized_data[key] = {}

                if formatted_date not in organized_data[key]:
                    organized_data[key][formatted_date] = 0

                # Accumulate amounts for the same date and person
                organized_data[key][formatted_date] += float(amount_collected)

        return organized_data






class OrignalRDcollectionView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    # without adding collection amount 
    def get(self,request,pk=None,format=None):
        if pk is not None:
            rdintrest = RDColl.objects.filter(rd_interest=pk,usersf__company=request.user)
            print(rdintrest)
            serilizer = RDCollectionDataallSerializer(rdintrest,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)



class LaonAmountView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
        data = request.data.copy()
        data['usersf'] = request.user.id  # Set the user field to the current user
        serializer = LaonaAmountSerilizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Loan Amount Created', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None, format=None):
        user_company = request.user.company
        if pk is not None:
            try:
                loan = LoanInt.objects.get(loan_id=pk, usersf__company=user_company)
                serializer = LaonaAmountIntrestSerilizer(loan)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except LoanInt.DoesNotExist:
                return Response({'error': 'Loan not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        else:
            loans = LoanInt.objects.filter(usersf__company=user_company)
            serializer = LaonaAmountIntrestSerilizer(loans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    def put(self, request, pk=None, format=None):
        user_company = request.user.company
        try:
            loan = LoanInt.objects.get(loan_id=pk, usersf__company=user_company)
        except LoanInt.DoesNotExist:
            return Response({'error': 'Loan not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LaonaAmountSerilizer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None, format=None):
        user_company = request.user.company
        try:
            loan = LoanInt.objects.get(loan_id=pk, usersf__company=user_company)
        except LoanInt.DoesNotExist:
            return Response({'error': 'Loan not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LaonaAmountSerilizer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Loan Updated Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def merge_by_collection_date_Loan(queryset):
    merged_data = {}
    for item in queryset:
        
        print(item.collection_date)
        collection_date = item.collection_date.date()  # Extract date part
        # print(item.loan_intrest.loan_id)
        loan_intrest_id = item.loan_intrest.loan_id

        if (collection_date, loan_intrest_id) not in merged_data:
            # If entry with same collection date and loan interest does not exist, add it
            merged_data[(collection_date, loan_intrest_id)] = item
        else:
            # If entry with same collection date and loan interest exists, add amount
            merged_data[(collection_date, loan_intrest_id)].amount_collected += item.amount_collected
    
    return merged_data.values()





class LoanCollectionView(APIView):
    renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serilizer = LoanCollectionSerilizer(data=request.data,many=True)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Loan Intrest Created Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,pk=None,format=None):
        if pk is not None:
            loan_collections = LoanColl.objects.filter(loan_intrest=pk)
            merged_data = merge_by_collection_date_Loan(loan_collections)
            serilizer = LoanCollectionDataallSerializer(merged_data,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
        else:   
            rdintrest =LoanColl.objects.all()
            serilizer = LoanCollectionSerilizer(rdintrest,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk=None,format=None):
        loan =  LoanColl.objects.get(id=pk)
        serilizer = LoanCollectionSerilizer(loan,data=request.data) 
        if  serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk=None,format=None):
        loan =  LoanColl.objects.get(id=pk)
        serilizer = LoanCollectionSerilizer(loan,data=request.data) 
        if  serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Loancollection Updated Successfully','data':serilizer.data},status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST) 
    


def merge_by_collection_date_Loan(queryset):
    merged_data = {}
    for item in queryset:
        
        print(item.collection_date)
        collection_date = item.collection_date.date()  # Extract date part
        # print(item.loan_intrest.loan_id)
        loan_intrest_id = item.loan_intrest.loan_id

        if (collection_date, loan_intrest_id) not in merged_data:
            # If entry with same collection date and loan interest does not exist, add it
            merged_data[(collection_date, loan_intrest_id)] = item
        else:
            # If entry with same collection date and loan interest exists, add amount
            merged_data[(collection_date, loan_intrest_id)].amount_collected += item.amount_collected
    
    return merged_data.values()


class LoanCollectionPerView(APIView):
    renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serilizer = LoanCollectionSerilizer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Loan Intrest Created Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)



from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware, get_current_timezone


class LoanCollectionViewDate(APIView):
    renderer_classes =[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request, pk=None, format=None):
        collection_date_str = request.data.get('collection_date')
        user_company = request.user.company
        
        if not collection_date_str:
            return Response({'error': 'collection_date parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse the date string to a date object
            collection_date = parse_date(collection_date_str)

            if collection_date is None:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)

            # Make the date timezone-aware
            current_timezone = get_current_timezone()
            collection_date = make_aware(datetime.combine(collection_date, datetime.min.time()), current_timezone)
            print("Parsed and timezone-aware date:", collection_date)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if pk is not None:
            loan_collections = LoanColl.objects.filter(
                loan_intrest=pk,
                collection_date__date=collection_date.date(),
                usersf__company=user_company
            )
            print("Filtered Loan Collections:", loan_collections)
            print("Database Entries:")
            for loan in LoanColl.objects.filter(loan_intrest=pk):
                print(f"ID: {loan.loan_collection_id}, Collection Date: {loan.collection_date}, Company: {loan.usersf.company}")

            if loan_collections.exists():
                # Process the loan collections as needed, e.g., serialization
                serializer = LoanCollectionDataallSerializerViewData(loan_collections, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No loan collections found for the given date.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'pk parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)







class LoanDataAPIView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        start_date = request.data.get('start_date')  # Format: 'YYYY-MM-DD'
        end_date = request.data.get('end_date')      # Format: 'YYYY-MM-DD'
        start_date_aware = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date_aware = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
        print(start_date_aware, end_date_aware)
        loan_collections = LoanColl.objects.filter(collection_date__range=(start_date_aware, end_date_aware),usersf__company=user.company)
        serializer = LoanCollectionDataSerializer(loan_collections, many=True)

        # print(serializer)
        # Organize data as needed
        organized_data = self.organize_data(serializer.data)

        return Response(organized_data, status=status.HTTP_200_OK)

    def organize_data(self, serialized_data):
        # Implement logic to organize data as needed
        # For example, create a dictionary with names as keys and lists of amounts as values

        organized_data = {}

        for item in serialized_data:
            
            loan_intrest = item.get('loan_intrest')
            amount_collected = item['amount_collected']
            collection_date = item['collection_date']
            person_name =item['person_name']

            if loan_intrest and amount_collected and collection_date:
                
                formatted_date = collection_date.split('T')[0]
                key = f"{loan_intrest}_{person_name}" 
                print(key)

                if key not in organized_data:
                    organized_data[key] = {}

                if formatted_date not in organized_data[key]:
                    organized_data[key][formatted_date] = 0

                # Accumulate amounts for the same date and person
                organized_data[key][formatted_date] += float(amount_collected)

        return organized_data 
  


from django.db.models import Sum

def collection_summary(company):
    # Ensure filtering by company and that collection_date is not null
    collection_dates = LoanColl.objects.filter(usersf__company=company, collection_date__isnull=False).values('collection_date').annotate(total_amount=Sum('amount_collected'))

    # Construct the summary dictionary
    summary_dict = {}
    local_timezone = get_current_timezone()
    
    for item in collection_dates:
        collection_date = item['collection_date']
        if collection_date:
            # Convert UTC datetime to local timezone
            collection_date_local = collection_date.astimezone(local_timezone)
            # Format the date to 'YYYY-MM-DD'
            formatted_date = collection_date_local.strftime('%Y-%m-%d')
            # Add the total amount to the summary dictionary
            if formatted_date in summary_dict:
                summary_dict[formatted_date] += float(item['total_amount'])
            else:
                summary_dict[formatted_date] = float(item['total_amount'])

    return summary_dict


def collection_summary_RD(company):
    # Ensure filtering by company and that collection_date is not null
    collection_dates = RDColl.objects.filter(usersf__company=company, collection_date__isnull=False).values('collection_date').annotate(total_amount=Sum('amount_collected'))

    # Construct the summary dictionary
    summary_dict = {}
    local_timezone = get_current_timezone()
    
    for item in collection_dates:
        collection_date = item['collection_date']
        if collection_date:
            # Convert UTC datetime to local timezone
            collection_date_local = collection_date.astimezone(local_timezone)
            # Format the date to 'YYYY-MM-DD'
            formatted_date = collection_date_local.strftime('%Y-%m-%d')
            # Add the total amount to the summary dictionary
            if formatted_date in summary_dict:
                summary_dict[formatted_date] += float(item['total_amount'])
            else:
                summary_dict[formatted_date] = float(item['total_amount'])

    return summary_dict

    
    
   

def collection_summary_loanDistribute(company):
    loan = LoanInt.objects.filter(usersf__company=company).values()
    summary_dict = {}

    for item in loan:
        start_date = item['start_date'].strftime('%Y-%m-%d')
        loan_id = item['loan_id']
        person = Person.objects.get(person_id=item['person_id'])

        # person_name = Person.objects.get(person_id=item[''])
        key = f'{start_date}_loan_{loan_id}'  # Create a unique key combining start_date and loan_id
        
        # Check if the key already exists in the summary_dict, if not, initialize it with an empty list
        if key not in summary_dict:
            summary_dict[key] = []
        
        summary_dict[key].append({"loan_amount": float(item['loan_amount']), "loan_id": loan_id,'name':person.name})

   

    return summary_dict

    

def collection_summary_fundcreditdistribute(company):
    sharehol = ShareHolder.objects.filter(uusersf__company=company).values()
    
    summary_dict = {}

    for item in sharehol:
        start_date = item['collection_date'].strftime('%Y-%m-%d')
        sfh_id = item['shf_id']
        person_name = Person.objects.get(person_id=item['person_id'])

        key = f'{start_date}_share_{sfh_id}'  # C reate a unique key combining start_date and loan_id
        
        # Check if the key already exists in the summary_dict, if not, initialize it with an empty list
        if key not in summary_dict:
            summary_dict[key] = []
        
        summary_dict[key].append({"amount_credit": float(item['amount_credit']),"amount_Debit": float(item['amount_Debit']), "shf_id": sfh_id,'name':person_name.name,'person_id':item['person_id']})

  
    return summary_dict






def collection_summary_staffSalary(company):
    staffSalary = StaffSalary.objects.filter(usersf__company=company).values()
    
    summary_dict = {}
 
    for item in staffSalary:
        start_date = item['collection_date'].strftime('%Y-%m-%d')
        sd_id = item['sd_id']
        person_name = Person.objects.get(person_id=item['person_id'])

        key = f'{start_date}_staff_{sd_id}'  # C reate a unique key combining start_date and loan_id
        
        # Check if the key already exists in the summary_dict, if not, initialize it with an empty list
        if key not in summary_dict:
            summary_dict[key] = []
        
        summary_dict[key].append({"amount_Debit": float(item['amount_Debit']), "shf_id": sd_id,'name':person_name.name,'person_id':item['person_id']})

  
    return summary_dict






def collection_summary_particulars(company):
    particulars = Partuclars.objects.filter(usersf__company=company).values()
    
    summary_dict = {}
 
    for item in particulars:
        start_date = item['time'].strftime('%Y-%m-%d')
        p_id = item['p_id']
        

        key = f'{start_date}_particulars_{p_id}'  # C reate a unique key combining start_date and loan_id
        
        # Check if the key already exists in the summary_dict, if not, initialize it with an empty list
        if key not in summary_dict:
            summary_dict[key] = []
        
        summary_dict[key].append({"amount_credit": float(item['amount_credit']),"amount_Debit": float(item['amount_Debit']), "p_id": p_id,'particular':item['particulars']})

  
    return summary_dict

def collection_summary_assets(company):
    particulars = Asset.objects.filter(usersf__company=company).values()
    
    summary_dict = {}
 
    for item in particulars:
        start_date = item['debit_date'].strftime('%Y-%m-%d')
        asset_no = item['asset_no']
        

        key = f'{start_date}_asset_{asset_no}'  # C reate a unique key combining start_date and loan_id
        
        # Check if the key already exists in the summary_dict, if not, initialize it with an empty list
        if key not in summary_dict:
            summary_dict[key] = []
        
        summary_dict[key].append({"amount_Debit": float(item['amount_Debit']), "asset_no": asset_no,'asetname':item['asset_name']})

    return summary_dict

def collection_summary_fixed_deposite(company):
    particulars = FixedDeposite.objects.filter(usersf__company=company).values()
    
    summary_dict = {}
 
    for item in particulars:
        start_date = item['collection_date'].strftime('%Y-%m-%d')
        fd_id = item['fd_id']
        person_name = Person.objects.get(person_id=item['person_id'])
        

        key = f'{start_date}_fd_{fd_id}'  # C reate a unique key combining start_date and loan_id
        
        # Check if the key already exists in the summary_dict, if not, initialize it with an empty list
        if key not in summary_dict:
            summary_dict[key] = []
        
        summary_dict[key].append({"amount_Debit": float(item['amount_Debit']),"amount_credit": float(item['amount_credit']), "person_name": person_name.name,'fd_id':fd_id})

  
    return summary_dict




class CashFlowStatement(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk=None,format=None):
        user_company = request.user.company        
        RDCollection = collection_summary_RD(user_company)
        loan_collectopn = collection_summary(user_company)

        loancoll_date = collection_summary_loanDistribute(user_company)

        shf = collection_summary_fundcreditdistribute(user_company)
        
        dict_rd = []
        for key,value in RDCollection.items():
            dictnew = {
                f'{key}_rdcoll' : value,
            }
            dict_rd.append(dictnew)
        
        dict_loan =[]
        for key,value in loan_collectopn.items():
            dictnew = {
                f'{key}_loancoll' : value,
            }
            dict_loan.append(dictnew)
        
        staffSalary=collection_summary_staffSalary(user_company)
        # print(shf,'shfdata')
        particulars = collection_summary_particulars(user_company)
        # print(particulars)
        asset = collection_summary_assets(user_company)

        fixed_deposite =  collection_summary_fixed_deposite(user_company)
        print(fixed_deposite)

        data = {"data":[dict_rd,dict_loan,shf,loancoll_date,staffSalary,particulars,asset,fixed_deposite]}
   
       
        orignalData = self.datamodify(data)     
        # print(data)          
            # new data 
                

        return Response(orignalData)
    def datamodify(self,data):
        # print('.....',data)
        # print(data['data'][0],'datazero',data['data'][1],data['data'][2],data['data'][3])
        newdata = []
        for item in data['data'][0]:
            # print(item)
            newdata.append(item)
        
        for item in data['data'][1]:
            # print(item)
            newdata.append(item)

        newDatanew = data['data'][2]
        # print(newDatanew,'..........')

        for key, value in newDatanew.items():
            # print(key)
            for item in value:
                # print(item)
                dict = {key:item}
                newdata.append(dict)

        newDatanewnew = data['data'][3]
       
        for key, value in newDatanewnew.items():
            # print(key)
            for item in value:
                # print(item)
                dict = {key:item}
                newdata.append(dict)

        newDatanew = data['data'][4]
        # print(newDatanew,'..........')

        for key, value in newDatanew.items():
            # print(key)
            for item in value:
                # print(item)
                dict = {key:item}
                newdata.append(dict)

        newDatanew = data['data'][5]
        # print(newDatanew,'..........')

        for key, value in newDatanew.items():
            # print(key)
            for item in value:
                # print(item)
                dict = {key:item}
                newdata.append(dict)

        newDatanew = data['data'][6]
        for key, value in newDatanew.items():
            # print(key)
            for item in value:
                # print(item)
                dict = {key:item}
                newdata.append(dict)

        newDatanew = data['data'][7]
        for key, value in newDatanew.items():
            # print(key)
            for item in value:
                # print(item)
                dict = {key:item}
                newdata.append(dict)

        requiredata = []
        sorted_data = sorted(newdata, key=lambda x: list(x.keys())[0])
        for item in sorted_data:
            for key, value in item.items():
                # print(key,value)
                dict =  {
                    key :value 
                }
                requiredata.append(dict)

        
        
        
            
        return requiredata

 
class StaffSalaryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
        data = request.data.copy()
        data['usersf'] = request.user.id
        serilizer = StaffSerilizer(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Staff Amount Deposited Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk=None,format=None):
        user_company=request.user.company
        if pk is not None:
            try:
                staff_salary = StaffSalary.objects.get(sd_id=pk)
                serilizer = StaffSerilizerwithname(staff_salary)
                return Response(serilizer.data,status=status.HTTP_200_OK)
            except StaffSalary.DoesNotExist:
                return Response({'error': 'Staff not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        else:   
            staff_salary =StaffSalary.objects.filter(usersf__company=user_company)
            serilizer = StaffSerilizerwithname(staff_salary,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk=None,format=None):
        user_company=request.user.company
        try:
            staff_sal = StaffSalary.objects.get(sd_id=pk,usersf__company=user_company)
        except StaffSalary.DoesNotExist:
            return Response({'error': 'Staff not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        
        serilizer = StaffSerilizer(staff_sal,data=request.data)
        if  serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request,pk=None,format=None):
        user_company=request.user.company
        try:
            staff_sal = StaffSalary.objects.get(sd_id=pk,usersf__company=user_company)
        except StaffSalary.DoesNotExist:
            return Response({'error': 'Staff not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        serilizer = StaffSerilizer(staff_sal,data=request.data)
        if  serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Salary Updated Succefully','data':serilizer.data},status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST) 

class ParticularView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
        data = request.data.copy()
        data['usersf'] = request.user.id
        serilizer = ParticularSerilizer(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Particulars Amount Deposited Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk=None,format=None):
        user_company = request.user.company
        if pk is not None:
            try:
                particulars = Partuclars.objects.get(p_id=pk,usersf__company=user_company)
                serilizer = ParticularSerilizer(particulars)
                return Response(serilizer.data,status=status.HTTP_200_OK)
            except Partuclars.DoesNotExist:
                return Response({'error': 'Expense not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        else:   
            particulars=Partuclars.objects.filter(usersf__company=user_company)
            serilizer = ParticularSerilizer(particulars,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk=None,format=None):
        user_company = request.user.company
        try:
            staff_sal = Partuclars.objects.get(p_id=pk,usersf__company=user_company)
        except Partuclars.DoesNotExist:
            return Response({'error': 'Expense not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)

        serilizer = ParticularSerilizer(staff_sal,data=request.data)
        if  serilizer.is_valid():   
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST) 
        
    def patch(self,request,pk=None,format=None):
        
        user_company = request.user.company
        try:
            staff_sal = Partuclars.objects.get(p_id=pk,usersf__company=user_company)
        except Partuclars.DoesNotExist:
            return Response({'error': 'Expense not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)

        serilizer = ParticularSerilizer(staff_sal,data=request.data)
        if  serilizer.is_valid():   
            serilizer.save()
            return Response({'msg':'Expense Deposite Updated SuccessFully','data':serilizer.data},status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)  




class FixedDepositeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]  
    def post(self,request,format=None):
        data = request.data.copy()
        data['usersf'] = request.user.id  
        serilizer = FixedDepositeSerilizer(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Fixed Amount Deposited Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk=None,format=None):
        user_company = request.user.company
        if pk is not None:
            try:

                fixed_deposite = FixedDeposite.objects.get(fd_id=pk,usersf__company=user_company)
                serilizer = FixedDepositeName(fixed_deposite)
                return Response(serilizer.data,status=status.HTTP_200_OK)
            except FixedDeposite.DoesNotExist:
                return Response({'error': 'Fixed Deposite not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        else:   
            fixed_deposite =FixedDeposite.objects.filter(usersf__company=user_company)
            serilizer = FixedDepositeName(fixed_deposite,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk=None,format=None):
        user_company = request.user.company
        try:
            fixed_deposite = FixedDeposite.objects.get(fd_id=pk,usersf__company=user_company)
        except FixedDeposite.DoesNotExist:
            return Response({'error': 'FixedDeposite not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        serilizer = FixedDepositeSerilizer(fixed_deposite,data=request.data)
        if  serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def patch(self,request,pk=None,format=None):
        user_company = request.user.company
        print(user_company)
        try:
            fixed_deposite = FixedDeposite.objects.get(fd_id=pk,usersf__company=user_company)
        except FixedDeposite.DoesNotExist:
            return Response({'error': 'FixedDeposite not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        serilizer = FixedDepositeSerilizer(fixed_deposite,data=request.data)
        if  serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Fixed Deposite Updated SuccessFully','data':serilizer.data},status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST) 



class AssetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
   
    def post(self,request,format=None):
        data = request.data.copy()
        data['usersf'] = request.user.id
        serilizer = AssetSerilizer(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Asset has created Successfully','data':serilizer.data},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,pk=None,format=None):
        user_company = request.user.company
        if pk is not None:
            try:
                asset = Asset.objects.get(asset_no=pk,usersf__company=user_company)
                serilizer = AssetSerilizer(asset)
                return Response(serilizer.data,status=status.HTTP_200_OK)
            except Asset.DoesNotExist:
                return Response({'error': 'Asset not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        else:   
            asset =Asset.objects.filter(usersf__company=user_company)
            serilizer = AssetSerilizer(asset,many=True)
            return Response(serilizer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk=None,format=None):
        user_company=request.user.company
        try:
            asset = Asset.objects.get(asset_no=pk,usersf__company=user_company)
        except Asset.DoesNotExist:
            return Response({'error': 'Asset not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        
        serilizer = AssetSerilizer(asset,data=request.data)
        if  serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST) 
        
    def patch(self,request,pk=None,format=None):
        user_company=request.user.company
        try:
            asset = Asset.objects.get(asset_no=pk,usersf__company=user_company)
        except Asset.DoesNotExist:
            return Response({'error': 'Asset not found or not accessible'}, status=status.HTTP_404_NOT_FOUND)
        
        serilizer = AssetSerilizer(asset,data=request.data)
        if  serilizer.is_valid():
            serilizer.save()
            return Response({'msg':'Asset Updated SuccessFully','data':serilizer.data},status=status.HTTP_200_OK)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST) 





# Profit and loss Statement 
# loan collection 
# rd collection 
# fd 
# shareholderfund 
# assets 
# salary 
# particulars 
# profit and  RD collection 


class ProfitandLoss(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        user_company = request.user.company
        start_date = request.data.get('start_date')  # Format: 'YYYY-MM-DD'
        end_date = request.data.get('end_date')      # Format: 'YYYY-MM-DD'
        start_date_aware = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date_aware = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
        # print(start_date_aware, end_date_aware)

        # RD collection 
        RD_intrest = RDInt.objects.filter(usersf__company=user_company)
        serialized_rd_intrest = RdIntersetSerilizer(RD_intrest, many=True)
        

        data = []
        for item in serialized_rd_intrest.data:
            rdColl = RDColl.objects.filter(rd_interest=item['rd_id'])
            merged_data = merge_by_collection_date(rdColl)
            serilizedRDColl =  RDCollectionDataallSerializer(merged_data,many=True)
            # print(item)
            table = render_table_rows(serilizedRDColl.data)
            # print(table)
            update_rd_installment(serilizedRDColl.data, table)
            rd_data = new_data(serilizedRDColl.data,table)
            dict = {
                f"{item['rd_id']}_{item['person_name']}" : rd_data
            }
            data.append(dict)

        rdIntrestval =  AddRdCollectionIntrest(data,start_date,end_date)
       
        
        # loan collection data 
        loan_all_data = []
        loan_int = LoanInt.objects.filter(usersf__company=user_company)
        serialized_loan = LaonaAmountIntrestSerilizer(loan_int, many=True)
        # print(serialized_loan.data,'dataserilize')
        
        for item in serialized_loan.data:
            loanColl = LoanColl.objects.filter(loan_intrest=item['loan_id'])
            
            merge_data = merge_by_collection_date_Loan(loanColl)
            serilizeLoanColl = LoanCollectionDataallSerializer(merge_data,many=True)
            print(serilizeLoanColl.data,'dataserilize')
            table_loan = render_table_rows_loan(serilizeLoanColl.data)
            update_emi_loan(serilizeLoanColl.data,table_loan)
            # print(table_loan)
            loan_data = new_data_lona(serilizeLoanColl.data,table_loan)
            dict = {
                f"{item['loan_id']}_{item['person_name']}" : loan_data
            }
            loan_all_data.append(dict)

        loanIntrestval = AddLoanCollectionIntrest(loan_all_data,start_date,end_date)
        # print(loanIntrestval,'loandtainvestdata')
        
        # print(loan_all_data)
        # asset
        asset = Asset.objects.filter(debit_date__gte=start_date_aware, debit_date__lte=end_date_aware,usersf__company=user_company)
        assetAllData = AssetSerilizer(asset,many=True)
        assetAmount = 0
        for item in assetAllData.data:
            assetAmount += float(item['amount_Debit'])

        # print(assetAmount)


        # expense 
        expense = Partuclars.objects.filter(time__gte=start_date_aware, time__lte=end_date_aware,usersf__company=user_company)
        expenseAllData = ParticularSerilizer(expense,many=True)

        expense_debit = 0
        expense_credit = 0
        for item in expenseAllData.data:
            expense_credit += float(item['amount_credit'])
            expense_debit += float(item['amount_Debit'])

        expenseprofitandLoss = {'expense_debit':expense_debit,'expense_credit':expense_credit}
        print(expenseprofitandLoss)
        # fixedDeposite 
        fixedDeposite = FixedDeposite.objects.filter(collection_date__gte=start_date_aware,collection_date__lte=end_date_aware,usersf__company=user_company)
        fixedDepositeAllData = FixedDepositeSerilizer(fixedDeposite,many=True)

        fd_amount_Debit = 0 
        fd_amount_credit = 0 
        for item in fixedDepositeAllData.data:
            fd_amount_Debit += float(item['amount_Debit'])
            fd_amount_credit += float(item['amount_credit'])

        fixedDepositepl = {'fd_debit':fd_amount_Debit,'fd_credit':fd_amount_credit}
        print(fixedDepositepl)
        # stff Salary 
        staffSalary =  StaffSalary.objects.filter(collection_date__gte=start_date_aware,collection_date__lte=end_date_aware,usersf__company=user_company)
        staffSalaryAllData =  StaffSerilizer(staffSalary,many=True)
        staff_amount = 0 
        for item in staffSalaryAllData.data:
            staff_amount += float(item['amount_Debit'])

        print(staff_amount)




        # allOrignalDAta =  {'msg': 'ok', 'allDataRdColl': data,'allDataLoanColl':loan_all_data,'allDateAsset' : assetAllData.data,'allDataExpense':expenseAllData.data,'allDataFixed':fixedDepositeAllData.data,'allDataStaffSalary':staffSalaryAllData.data}

        # allProfitandLossData = {'rd':rdIntrestval,'loan':loanIntrestval,asset:assetAmount,'expense':expenseprofitandLoss,}




        return Response({'msg': 'ok', 'loan': loanIntrestval,'rd':rdIntrestval,'asset':assetAmount,'expense':expenseprofitandLoss,'staff':staff_amount,'fd':fixedDepositepl})


# Function to calculate interest




from datetime import datetime, timedelta

from datetime import datetime, timedelta
from dateutil.parser import parse

def render_table_rows(prodataitem):
    rows = []

    if not prodataitem or len(prodataitem) == 0:
        return None

    start_date = parse(prodataitem[0]['start_date']).date()
    duration = prodataitem[0]['duration']
    amount_collected = prodataitem[0]['amount_collected']

    if start_date and duration and amount_collected:
        current_date = start_date

        for i in range(1, duration + 1):
            row_data = {
                'date': current_date.strftime('%d-%m-%Y'),
                'days': i,
                'begningvalue': '',
                'rd_installment': '',
                'intrest': '',
                'endingvalue': ''
            }
            rows.append(row_data)
            current_date += timedelta(days=1)  # Increment date by 1 day

    return rows


def update_rd_installment(new_renswreddata, prodataitem):
    for item in new_renswreddata:
        for items in prodataitem:
            collection_date=item['collection_date'].split('T')[0]
            date_obj = datetime.strptime(collection_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d-%m-%Y")
            date = items['date']
            if formatted_date == date:
                items['rd_installment'] = item['amount_collected']



def new_data(prodataitem, new_renswreddata):

    rows = []
    dura, inter = prodataitem[0]['duration'], prodataitem[0]['interest']
    beginning_value = 0  # Initialize beginning value

    for items in new_renswreddata:
        # Convert empty strings to 0
        rd_installment = float(items['rd_installment']) if items['rd_installment'] else 0

        # Calculate interest
        interest = beginning_value * float(inter) * 0.01 / 365

        data = {
            'date': items['date'],
            'days': items['days'],
            'beginning_value': beginning_value,
            'rd_installment': rd_installment,
            'interest': round(interest, 3),
            'ending_value': beginning_value + rd_installment + interest
        }

        rows.append(data)

        beginning_value = data['ending_value']

    return rows



def render_table_rows_loan(prodataitem):
    rows = []
    # print(prodataitem)
    if not prodataitem or len(prodataitem) == 0:
        return None

    start_date = parse(prodataitem[0]['start_date'])
    
    duration = int(prodataitem[0]['duration'])
    amount_collected = float(prodataitem[0]['amount_collected'])

    if start_date and duration and amount_collected:
        current_date = start_date

        for i in range(1, duration + 1):
            row_data = {
                'date': current_date.strftime('%d-%m-%Y'),
                'days': i,
                'balanceamount': '',
                'emi': '',
                'interest': '',
                'principle': '',
                'ending_balance': ''
            }
            rows.append(row_data)
            current_date += timedelta(days=1)  # Increment date by 1 day

    return rows


def update_emi_loan(new_renswreddata,prodataitem):
    for item in new_renswreddata:
        for items in prodataitem:
            collection_date=item['collection_date'].split('T')[0]
            date_obj = datetime.strptime(collection_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d-%m-%Y")
            date = items['date']
            if formatted_date == date:
                items['emi'] = item['amount_collected']


def new_data_lona(prodataitem, new_renswreddata):

    rows = []
    
    if not prodataitem or len(prodataitem) == 0:
        return None

    dura = prodataitem[0]['duration']
    inter = prodataitem[0]['interest']
    loan_amount = prodataitem[0]['loan_amount']
    beginning_value = float(loan_amount)
    ending_value = 0
    interest = 0
    principle = 0

    for items in new_renswreddata:
        # Calculate interest
        interest = beginning_value * float(inter) * 0.01 / 365
        loan_emi = float(items['emi']) if items['emi'] else 0
        principle = loan_emi - round(interest, 2)
        
        data = {
            'date': items['date'],
            'days': items['days'],
            'balanceamount': round(beginning_value, 2),
            'emi': items['emi'],
            'intrest': round(interest, 2),
            'principle': round(principle, 2),
            'endingvalue': round(beginning_value - principle, 2)
        }
        
        rows.append(data)
        # Update endingValue with the current row's endingvalue
        ending_value = data['endingvalue']
        # Update beginningValue for the next iteration
        beginning_value = ending_value

    return rows   




def AddRdCollectionIntrest(allDataRdColl, start_date, end_date):
    total_interest_RD = 0

    # Convert start_date and end_date to datetime objects if they are not already
    formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Iterate over each item in allDataRdColl
    for item in allDataRdColl:
        for data in item.values():
            for rd_data in data:
                rd_date_obj = datetime.strptime(rd_data['date'], "%d-%m-%Y").date()
                # Check if the item date falls within the specified range
                if formatted_start_date <= rd_date_obj <= formatted_end_date:
                    # Accumulate the interest rate
                    total_interest_RD += rd_data['interest']

    return total_interest_RD


def AddLoanCollectionIntrest(allDataLoanColl, start_date, end_date):

    total_interest_loan = 0

    # Convert start_date and end_date to datetime objects if they are not already
    formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Iterate over each item in allDataRdColl
    for item in allDataLoanColl:
        for data in item.values():
            for loan_data in data:
                loan_date_obj = datetime.strptime(loan_data['date'], "%d-%m-%Y").date()
            #     # Check if the item date falls within the specified range
                if formatted_start_date <= loan_date_obj <= formatted_end_date:
            #         # Accumulate the interest rate
                    total_interest_loan += loan_data['intrest']

    return total_interest_loan

class ShreHolderFundGetData(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        user_company = request.user.company

        if pk is not None:
            try:
                shf = ShareHolder.objects.get(shf_id=pk, person__usersf__company=user_company)
                serializer = ShareHolderFunsDataDisSerializer(shf)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ShareHolder.DoesNotExist:
                return Response({'error': 'ShareHolder not found or not associated with your company.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            sh = ShareHolder.objects.filter(person__usersf__company=user_company)
            serializer = ShareHolderFunsDataDisSerializer(sh, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)