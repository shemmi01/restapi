from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUser(APIView):

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'errors':serializer.errors, 'message': 'something went wrong'})

        serializer.save()

        user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({"payload": serializer.data, 
        'refresh':str(refresh),
        'access': str(refresh.access_token),
        'message':'your data has been saved'})
        
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        student_obj = Student.objects.all()
        serializer=StudentSerializer(student_obj, many=True)
        return Response({"payload": serializer.data})
    
    def post(self,request):

        data = request.data
        serializer = StudentSerializer(data = request.data)

        if int(request.data['age']) < 18:
            return Response({'message': 'age must be > 18'})


        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'errors':serializer.errors, 'message': 'you sent'})

        serializer.save()
        return Response({"payload": serializer.data, 'message':'your data has been saved'})

    def put(self, request):
        try:
            student_obj =Student.objects.get(id = request.data['id'])
            serializer = StudentSerializer(student_obj, data = request.data, partial =False)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'errors':serializer.errors, 'message': 'you sent'})

            serializer.save()

            return Response({"payload": serializer.data, 'message':'your data has been saved'})
        except Exception as e:
            return Response({'message': 'invalid id'})


    def patch(self,request):
        try:
            student_obj =Student.objects.get(id = request.data['id'])
            serializer = StudentSerializer(student_obj, data = request.data, partial =True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'errors':serializer.errors, 'message': 'you sent'})

            serializer.save()

            return Response({"payload": serializer.data, 'message':'your data has been saved'})
        except Exception as e:
            return Response({'message': 'invalid id'})


    

    def delete(self, request):
        try:
            id = request.GET.get('id')
            student_obj = Student.objects.get(id = id)
            student_obj.delete()
            return Response({'message': 'Deleted'})

        except Exception as e:
            print(e)
            return Response({'message':'Invalid id'})

import pandas as pd
from django.conf import settings
import uuid

class ExportImportExcel(APIView):
    def get(self, request):
        student_obj = Student.objects.all()
        serializer =StudentSerializer(student_obj, many= True)
        df = pd.DataFrame(serializer.data)
        print(df)
        df.to_csv("public/excel/{uuid.uuid4()}.csv", encoding="UTF-8",index= False)

        return Response({'status': 200})
    
    def post(self, request):
        excel_upload_obj = ExcelFileUpload.objects.create(excel_file_upload = request.FILES['files'])
        df = pd.read_csv(f"{settings.BASE_DIR}/public/excel/{excel_upload_obj.excel_file_upload}")
        print(df.values.tolist())
        return Response({'status': 200})


# @api_view(['GET'])
# def get_book(request):
#     book_obj = Book.objects.all()
#     serializer = BookSerializer(book_obj, many = True)
#     return Response({"payload":serializer.data})


# @api_view(['GET'])
# def home(request):
#     student_obj = Student.objects.all()
#     serializer=StudentSerializer(student_obj, many=True)
#     return Response({"payload": serializer.data})


# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     serializer = StudentSerializer(data = request.data)

#     if int(request.data['age']) < 18:
#        return Response({'message': 'age must be > 18'})


#     if not serializer.is_valid():
#         print(serializer.errors)
#         return Response({'errors':serializer.errors, 'message': 'you sent'})

#     serializer.save()

#     return Response({"payload": serializer.data, 'message':'your data hasbeen saved'})

# @api_view(['PUT'])
# def update_student(request, id):
#     try:
#         student_obj =Student.objects.get(id = id)
#         serializer = StudentSerializer(student_obj, data = request.data, partial =True)
#         if not serializer.is_valid():
#             print(serializer.errors)
#             return Response({'errors':serializer.errors, 'message': 'you sent'})

#         serializer.save()

#         return Response({"payload": serializer.data, 'message':'your data has been saved'})
#     except Exception as e:
#         return Response({'message': 'invalid id'})

# @api_view(['DELETE'])
# def delete_student(request):
#     try:
#         id = request.GET.get('id')
#         student_obj = Student.objects.get(id = id)
#         student_obj.delete()
#         return Response({'message': 'Deleted'})


#     except Exception as e:
#         print(e)
#         return Response({'message':'Invalid id'})



