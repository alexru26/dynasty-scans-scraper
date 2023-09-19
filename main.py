from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

from datetime import date, timedelta
from pytz import timezone

import requests
from bs4 import BeautifulSoup

def make_reading_list():
    with open("list.txt", "r") as file:
        text = file.readlines()

    reading_list = []
    for line in text:
        reading_list.append(line.strip())

    return reading_list

def convert_title(title):
    cutoff = -1

    for i in range(len(title)):
        if(title[i].isdigit() and title[i-1] == "h"):
            cutoff = i
            break
    if(cutoff == -1):
        return title
    else:
        return title[:(cutoff-3)]

def send_email(title):

    subject = "New " + title + " chapter!"
    body = "It's gonna be a good night today :)"
    sender = "rualex2008@gmail.com"
    recipients = ["rualex2008@gmail.com"]
    p = 'cwsc ljix uedc uzvs'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, p)
       smtp_server.sendmail(sender, recipients, msg.as_string())

def main():
    today = date.today()
    yesterday = today - timedelta(days=1)

    print(today.strftime("%B %d, %Y"))
    print(yesterday.strftime("%B %d, %Y"))

    response = requests.get("https://dynasty-scans.com/chapters/added")
    soup = BeautifulSoup(response.text, 'html.parser')

    #IMPLEMENT SOME METHOD TO TELL MOST RECENT UPLOAD DATE

    doujin_titles_today = soup.find('dt', string=today.strftime("%B %d, %Y")).find_next_siblings("dd")
    doujin_titles_yesterday = soup.find('dt', string=yesterday.strftime("%B %d, %Y")).find_next_siblings("dd")

    reading_list = make_reading_list()
    
    for title in doujin_titles_today:
        if(title in doujin_titles_yesterday):
            break
        else:
            a = title.find('a', class_="name")
            good_title = convert_title(a.text).strip()
            if(good_title in reading_list):
                send_email(good_title)

    print("\nI think it worked...?")

if __name__ == '__main__':
    main()