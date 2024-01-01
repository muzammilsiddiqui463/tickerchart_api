# tickerchartapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.http import JsonResponse
from .models import Data
from .serializers import DataSerializer
from .bot.scrapper import Scraper
import threading

scraper  = Scraper()
class DataListCreateView(APIView):
    def get(self, request):
        data = Data.objects.all()
        serializer = DataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DataSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        data = Data.objects.all()
        for tobe_delete in data:
            tobe_delete.delete()
        return Response({"Message":"Data Deleted"},status=status.HTTP_204_NO_CONTENT)

class DataRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        data = get_object_or_404(Data, pk=pk)
        serializer = DataSerializer(data)
        return Response(serializer.data)

    def put(self, request, pk):
        data = get_object_or_404(Data, pk=pk)
        serializer = DataSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        data = get_object_or_404(Data, pk=pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def start_(request):
    global scraper
    s = threading.Thread(target=scraper.run_process)
    s.start()
    # Return a JSON response indicating the process has started
    return JsonResponse({'message': 'Process started successfully'})

def stop_(request):
    global scraper

    scraper.close_browser()

    return JsonResponse({'message': 'Process stopped successfully'})

