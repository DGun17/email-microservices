from django.forms import ModelForm
from shipper.models import Report
from shipper.tasks import test_shipper, shipper_lastest


class ReportUpload(ModelForm):
    class Meta:
        model = Report
        fields = ('shipper', )

    def save(self, commit=True):
        file = super(ReportUpload, self).save(commit=commit)
        shipper_lastest.delay(file.id)
        test_shipper.delay()
