import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from swchars.services.chars_backend.manager import SWDataManager

# Create your views here.


class SWCharsAPIView(APIView):

    def get(self, request):
        response = SWDataManager().get_chars(**request.GET)
        return Response(response)


class SWItemsAPIView(APIView):

    def get(self, request):
        response = SWDataManager().get_item(**request.GET)
        return Response(response)
