import os
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.conf import settings
import csv



class ValidatedInformationView(View):
    def get(self, request, *args, **kwargs):
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'csvfiles/source_file_data.csv')
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                data = [row for row in csv_reader]
                return JsonResponse(data, safe=False)
        except FileNotFoundError:
            return JsonResponse({"error": "File  anot found."}, status=404)




