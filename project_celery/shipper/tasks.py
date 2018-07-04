from __future__ import absolute_import
import os
import pandas
import xlsxwriter
from os.path import splitext
from django.conf import settings
from celery import current_app
from shipper.models import Report
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

app = current_app


@app.task()
def test_shipper():
    files = os.listdir(settings.REPORTS_DIR_FILES)

    print("Report Files")

    for file in files:
        print(f"[+] file: {file}")


columns = ["id",
           "password",
           "last_login",
           "is_superuser",
           "username",
           "first_name",
           "last_name",
           "email",
           "is_staff",
           "is_active"
           ]

User = get_user_model()


@app.task()
def shipper_lastest(file_id):

    file = Report.objects.get(pk=file_id)
    print(f"[*] Lastest file upload id-> {file_id}")

    file_ext = splitext(file.shipper.name)[1][1:]
    file_path = file.shipper.path

    if file_ext == 'xls':

        print("[!] Process excel file to register user")

        try:
            user_info = pandas.read_excel(file_path, names=columns)
            for _, row in user_info.iterrows():
                kwargs = dict(row)
                kwargs.pop('id', None)
                User(**kwargs).save()
        except Exception as e:
            print(f"[-] Error file to register user wrong, {e}")


@app.task()
def get_users():
    backup_path = os.path.join(settings.REPORTS_DIR_FILES, 'send')
    filepath = os.path.join(backup_path, 'user_actives.xlsx')

    # Make headers
    workbook = xlsxwriter.Workbook(filepath, {'remove_timezone': True})
    worksheet = workbook.add_worksheet(name='users')
    # Add header
    worksheet.write_row(row=0, col=0, data=columns)

    # Make query
    users = User.objects.filter(is_active=1)

    for idx, user in enumerate(users):
        u = user.__dict__
        u.pop('_password', None)
        u.pop('_state', None)
        u.pop('date_joined', None)

        worksheet.write_row(row=idx+1,
                            col=0,
                            data=u.values()
                            )
    workbook.close()
    return filepath


@app.task()
def send_repo_file(file):
    e = EmailMessage()
    e.subject = "Usuarios activos en la plataforma"
    e.to = ["<send_to>"]
    e.from_email = settings.EMAIL_HOST_USER.strip()
    e.attach_file(file)
    e.send()
    return os.path.dirname(file)


@app.task()
def clean_directory(directory):
    files = os.listdir(directory)
    for file in files:
        filepath = os.path.join(directory, file)
        os.remove(filepath)
    return True
