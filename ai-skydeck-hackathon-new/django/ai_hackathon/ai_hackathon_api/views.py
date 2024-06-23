from django.shortcuts import render

from .emotions_json_formatter import EmotionsUploader
from .aws_sdxl import SDXL

from .models import Company, CompanyReport, CompanyEmotions
from .serializers import CompanySerializer, CompanyReportSerializer, CompanyEmotionsSerializer
from .sustainability_report_downloader import SustainabilityReportDownloader
from wsgiref.util import FileWrapper
from django.http import HttpResponse, Http404, JsonResponse
import os
from rest_framework import viewsets
from rest_framework.views import APIView

def success_json(msg, data ={}):
     return {
          "message": msg,
          "data": data
          }

def fail_json(msg):
     return {
          "error": msg
          }

class CompanyViewSet(viewsets.ModelViewSet):
	queryset = Company.objects.all()
	serializer_class = CompanySerializer

class CompanyReportViewSet(viewsets.ModelViewSet):
	queryset = CompanyReport.objects.all()
	serializer_class = CompanyReportSerializer

class CompanyEmotionsViewSet(viewsets.ModelViewSet):
	queryset = CompanyEmotions.objects.all()
	serializer_class = CompanyEmotionsSerializer

class GenerateCompanyEmotionsView(APIView):
    def put(self, request, format=None):
        company_name = request.GET.get('companyName', '')
        if not (company_name):
             return JsonResponse("companyName is a required PUT param!")
        
        try:
             company_obj = Company.objects.get(name=company_name)

             emotions = CompanyEmotions.objects.filter(company=company_obj)
             for emotion in emotions:
                  sdxl = SDXL(emotion.emotions)
                  img_bytes = sdxl.get_bytes()
                  self.save_image(img_bytes)
                  
                  company_obj = Company.objects.get(name=self.company_name)
        except Exception as e:
             return JsonResponse(fail_json(str(e)), status=404)

        return JsonResponse(success_json("Successfully updated CompanyEmotions object"), status=200)


class CompaniesView(APIView):
     def get(self, request, format=None):
        try:
             companies = Company.objects.all().values()
             return JsonResponse(success_json("Successfully Got Companies", list(companies)), status=200)
        except Exception as e:
             return JsonResponse(fail_json(str(e)), status=404)

        return JsonResponse(success_json("Successfully updated Company object"), status=200)
     
class CompanyView(APIView):
     def put(self, request, format=None):
        company_name = request.GET.get('companyName', '')
        youtube_url = request.GET.get('youtubeUrl', '')

        if not (company_name and youtube_url):
             return JsonResponse("companyName and youtubeUrl are required GET param!")
        
        try:
             obj = Company.objects.get(name=company_name)
             obj.youtube_url = youtube_url
             obj.save()
        except Exception as e:
             return JsonResponse(fail_json(str(e)), status=404)

        return JsonResponse(success_json("Successfully updated Company object"), status=200)

class FormatCompanyEmotionsView(APIView):
     def get(self, request, format=None):
        company_name = request.GET.get('companyName', '')

        if not company_name:
             return JsonResponse("Missing companyName GET param!")
        
        company_emotions = EmotionsUploader()
        company_emotions.walk_dir()

        return JsonResponse(success_json("Successfully formatted Company emotions"), status=200)
     
class GenerateCompanyReportView(APIView):
    def get(self, request, format=None):
        company_name = request.GET.get('companyName', '')

        if not company_name:
             return JsonResponse("Missing companyName GET param!")
        
        report_downloader = SustainabilityReportDownloader(company_name)
        report_downloader.call_company_api()

        return JsonResponse(success_json("Successfully generated Company reports"), status=200)

class CompanyReportView(APIView):
    def get_company(self, company_name):
        try:
            return Company.objects.get(name=company_name)
        except Company.DoesNotExist:
            raise Http404
        
    def get(self, request, format=None):
        report_url = request.GET.get('reportUrl', '')

        if not report_url:
             return JsonResponse("Missing reportUrl GET param!", status=404)
        
        short_report = open(report_url, 'rb')
        response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
        return response
        
    def delete(self, request, format=None):
        company_name = request.GET.get('companyName', '')

        if not (company_name):
             return JsonResponse(success_json("companyName is a required GET param!"), status=404)
        
        try:
            company_obj = self.get_company(company_name)
            reports = CompanyReport.objects.filter(company=company_obj)
            if len(reports) > 0:
                for report in reports:
                    print("deleting report " + str(report.year))
                    report.delete()
                msg = "Successfully deleted reports for: " + company_name
                return JsonResponse(success_json(msg), status=204)
        except Exception as e:
             return JsonResponse(fail_json(str(e)), status=404)
        
        return JsonResponse(fail_json("Delete was not successfully, probably didn't exist"), status=404)