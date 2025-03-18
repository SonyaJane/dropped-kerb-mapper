from django.shortcuts import render
from django.views import generic
from .models import Report

# Create your views here.
class ReportList(generic.ListView):
   queryset = Report.objects.all()
   template_name = "report_list.html"