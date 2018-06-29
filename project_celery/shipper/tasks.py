from __future__ import absolute_import
import os
import pandas
from os.path import splitext
from django.conf import settings
from celery import current_app
from shipper.models import Report
from django.contrib.auth import get_user_model

app = current_app


@app.task()
def test_shipper():
    files = os.listdir(settings.REPORTS_DIR_FILES)

    print("Report Files")

    for file in files:
        print(f"[+] file: {file}")


columns = ["id", "last_login", "is_superuser", "username",
           "first_name", "last_name", "email", "is_staff",
           "is_active", "date_joined"]

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
                # print(f"[+] Save user #{index+1} with username {row['username']}")
                User(password='',
                     last_login=row['last_login'],
                     is_superuser=row['is_superuser'],
                     first_name=row['first_name'],
                     last_name=row['last_name'],
                     email=row['email'],
                     is_staff=row['is_staff'],
                     is_active=row['is_active'],
                     date_joined=row['date_joined'],
                     username=row['username']
                     ).save()

        except Exception as e:

            print(f"[-] Error file to register user wrong, {e}")




