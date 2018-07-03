from django.conf.urls import url
from shipper.views import UploadReport, send_report

app_name = "shipper"
urlpatterns = [
    url(r'^upload/$', UploadReport.as_view(), name='upload_report'),
    url(r'^send/$', send_report, name='send_report'),
]
