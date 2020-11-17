from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as httpstatus

# Create your views here.

def index(request):
    return render(request, 'index.html')

class SpamTest(APIView):
	def post(self, request, format=None):
		model_name = request.data.get('email_text', None)
		
		return get_success_200_reponse("test")

def get_success_200_reponse(data):
	return Response(data, status=httpstatus.HTTP_200_OK)