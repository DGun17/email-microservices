from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, CreateView
from shipper.forms import ReportUpload
# Create your views here.


class UploadReport(FormView):
    template_name = 'shipper/upload.html'
    form_class = ReportUpload
    success_url = reverse_lazy('shipper:upload_report')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # files = request.FILES.getlist('file')
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
