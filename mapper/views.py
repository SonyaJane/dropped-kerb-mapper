from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .forms import ReportForm
from .models import Report, Photo

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


def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user if request.user.is_authenticated else None
            report.save()

            # Save up to 3 photos
            # photos = request.FILES.getlist('photos')
            # for photo in photos[:3]:  # Limit to 3 photos
            #     Photo.objects.create(report=report, photo=photo)

            return redirect('reports-list')  # Redirect to the reports list page
    else:
        form = ReportForm()

    return render(request, 'mapper/create_report.html', {'form': form})