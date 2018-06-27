# -*- coding: utf-8 -*-
"""
Send email with python3.6 by Jrnp97
"""
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address

# Account credentials
with open('credentials', 'r') as f:
    data = f.readlines()
    G_EMAIL = data[0]
    PASSWORD = data[1]

# Configure SMTP
G_MAIL = smtplib.SMTP('smtp.gmail.com', 587)
# # Init TLS
G_MAIL.ehlo()
G_MAIL.starttls()
G_MAIL.set_debuglevel(1)


def send(subject: str,  send_list: list, body: str, from_email: str = None) -> bool:
    """
    Function to send email with a gmail account to use this function you need activate
    the follow permission https://myaccount.google.com/lesssecureapps?pli=1 on gmail account.

    :param subject: email subject
    :param from_email: from email, default None
    :param send_list:  email or list of emails to send
    :param body: email body.
    :return:
    """

    # Make destination list
    destinations = []
    for email in send_list:
        info = email['email'].split('@')
        assert len(info) == 2, "Email incorrect verify list"
        add = Address(display_name=email['name'], username=info[0], domain=info[1])
        destinations.append(add)

    # Login account
    G_MAIL.login(G_EMAIL, PASSWORD)

    # CONFIGURING EMAIL
    MESSAGE = EmailMessage()
    MESSAGE['Subject'] = subject
    MESSAGE['From'] = G_EMAIL
    MESSAGE.set_content(body)
    MESSAGE['To'] = tuple(destinations) if len(destinations) > 1 else destinations[0]

    # Send message
    G_MAIL.send_message(MESSAGE)

    # Close connection
    G_MAIL.quit()
    return True