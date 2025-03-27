from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Report

def home(request):
    """
    Render the home page
    """
    return render(request, 'mapper/home.html')
 
class ReportList(generic.ListView):
   queryset = Report.objects.all()
   template_name = "mapper/reports.html"
   paginate_by = 24
   
   
def report_detail(request, pk):
   """
   Retrieves a single report from the database and displays it on the page.
   """
   queryset = Report.objects.all()
   report = get_object_or_404(queryset, pk=pk)
   return render(request, "mapper/report_detail.html", {"report": report})