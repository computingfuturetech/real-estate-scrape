import os
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.conf import settings

class HelloWorldView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World!")

class CSVDataView(View):
    def get(self, request, *args, **kwargs):
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csvfiles/output.csv')

        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
                csv_data = csv_file.read()
            return HttpResponse(csv_data, content_type='text/csv')
        except FileNotFoundError:
            return HttpResponse("File not found.", status=404)




