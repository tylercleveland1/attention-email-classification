from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as httpstatus

#pysource
from .python_source.EmailClassifier import *

# Create your views here.

def index(request):
    return render(request, 'index.html')

class SpamTest(APIView):
	def post(self, request, format=None):
		email_text = request.data.get('emailText', None)

		email_classifier = EmailClassifier()
		
		return get_success_200_reponse(email_text)

class SpamOrHam(APIView):
	def post(self, request, format=None):
		email_text = request.data.get('emailText', None)

		email_classifier = EmailClassifier()

		out = email_classifier.get_prediction_and_data(email_text)
		
		return get_success_200_reponse(out)

def get_success_200_reponse(data):
	return Response(data, status=httpstatus.HTTP_200_OK)