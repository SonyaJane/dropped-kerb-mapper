from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from .forms import ReportForm
from .models import Report
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

def home(request):
    """
    Render the home page
    """
    return render(request, 'mapper/home.html')
 
 
class ReportList(generic.ListView):
   template_name = "mapper/reports.html"
   paginate_by = 24
   
   def get_queryset(self):
        """
        Return reports created by the logged-in user.
        If the user is a superuser, return all reports.
        """
        if self.request.user.is_superuser:
            # Superuser sees all reports
            return Report.objects.all()
        else:
            # Regular users see only their own reports
            return Report.objects.filter(user=self.request.user)
   
   
def report_detail(request, pk):
   """
   Retrieves a single report from the database and displays it on the page.
   """
   queryset = Report.objects.all()
   report = get_object_or_404(queryset, pk=pk)
   return render(request, "mapper/report_detail.html", {"report": report})


def create_report(request):
    if request.method == 'POST':
        report_form = ReportForm(request.POST, request.FILES)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'Report created successfully!')
            return redirect('reports-list')  # Redirect to the reports list page
    else:
        form = ReportForm()
    return render(request, 'mapper/create_report.html', {'form': form})


class ReportEditView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'mapper/edit_report.html'

    def get_success_url(self):
        # Redirect to the report detail page after editing
        return reverse_lazy('report-detail', kwargs={'pk': self.object.pk})