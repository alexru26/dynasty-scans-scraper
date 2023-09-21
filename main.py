from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

def make_reading_list():
    # returns a list of titles reading currently

    # open file
    with open("list.txt", "r") as file:
        text = file.readlines()

    # go through file line by line and get list of titles
    reading_list = []
    for line in text:
        reading_list.append(line.strip())

    return reading_list

def get_new_titles(soup, reading_list):
    # gets the most recent titles and return titles that are in reading list today

    # step 1: look at titles and find ones that are released today
    now = datetime.now()
    today = now.strftime("%B %d, %Y")
    yesterday = (now - timedelta(days=1)).strftime("%B %d, %Y")
    date = soup.find('dt', string=today)

    titles_today = []
    a = date.find_next_sibling()
    while(True):
        check = a
        titles_today.append(convert_title(check.find('a').text))
        a = a.find_next_sibling()
        if(a.text == yesterday):
            break

    print(titles_today)

    # step 2: look at reading list to find matches
    good_titles_today = []
    for title in titles_today:
        if(title.strip() in reading_list):
            good_titles_today.append(title.strip())

    # step 3: return list of matches
    return good_titles_today

def convert_title(title):
    # convert from ... ch__ to ...

    # index to find ch
    cutoff = -1

    # finds ch and when char before is digit
    for i in range(len(title)):
        if(title[i].isdigit() and title[i-1] == "h"):
            cutoff = i
            break
    if(cutoff == -1):
        # if no such thing is found, just return title
        return title
    else:
        # if there is such thing, do some indexing
        return title[:(cutoff-3)]

def send_email(title):
    # automates sending emails with correct subject line

    # opens text file for info
    with open("gmail.txt", "r") as file:
        text = file.readlines()

    # input data for email
    subject = "New " + title + " chapter!"
    body = "It's gonna be a good night today :)"
    sender = text[0].strip()[17:]
    recipients = []
    p = text[1].strip()[5:]
    for i in range(len(text)-4):
        recipients.append(text[i+4].strip())

    # creates actual email and sends it
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, p)
       smtp_server.sendmail(sender, recipients, msg.as_string())

def main():
    # sets up everything, gets the job done

    # get website and get its html stuff
    response = requests.get("https://dynasty-scans.com/chapters/added")
    soup = BeautifulSoup(response.text, 'html.parser')

    # list of titles currently looking out for
    reading_list = make_reading_list()

    print(reading_list)

    # returns title that released today and is in reading list
    oh_yeah = get_new_titles(soup, reading_list)
   
    for title in oh_yeah:
        print(title)
        send_email(title)

    print("\nI think it worked...?")
    
if __name__ == '__main__':
    main()