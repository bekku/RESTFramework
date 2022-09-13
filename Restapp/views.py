from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render 
from rest_framework import viewsets, filters
from .models import Template

from .serializers import TemplateSerializer
class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer



def index(request):
	return render(request, 'Restapp/index.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class NonSeializers_Api(APIView):
    def get(self, request):
        out_dict = {}
        out_dict['message'] = 'get'
        return Response(out_dict, status=status.HTTP_200_OK)
    def post(self, request):
        out_dict = {}
        out_dict['message'] = 'post'
        return Response(out_dict)