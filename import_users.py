import csv
import os
import uuid
# path =  "C:\\...." # Set path of new directory here
# os.chdir(path) # changes the directory
from users.models import User # imports the model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage

fp = open(('badge-small.jpg'), 'rb')
msg_img = MIMEImage(fp.read())
fp.close()
msg_img.add_header('Content-ID', '<{}>'.format('badge-small.jpg'))

with open('bsg_data_new.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    p = User(
      username=row['NICKNAME'], 
      email=row['email address'],
      mobile=row['mobile number'],
      facebook=row['facebook account'],
      instagram=row['instagram account'],
      uuid=uuid.uuid4(),
      # password=row['password']
      )
    p.set_password(row['Password'])
    p.save()
    context = {
      'user': p,
      'password' : row['Password']
    }
    print(p.username)
    subject = render_to_string('registration/momzilla_signup_subject.txt', context)
    subject = ''.join(subject.splitlines())
    message_text = render_to_string('registration/momzilla_signup.txt', context)
    message_html = render_to_string('registration/momzilla_signup.html', context)
    msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [p.email, 'issa@babysetgo.ph', 'issarufinasenga@gmail.com'])
    msg.attach_alternative(message_html, "text/html")
    msg.attach(msg_img)
    msg.send()

exit()