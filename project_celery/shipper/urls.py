from django.conf.urls import url
from shipper.views import UploadReport

app_name = "shipper"
urlpatterns = [
    url(r'^upload/$', UploadReport.as_view(), name='upload_report')
]
