# import smtplib
# from email.mime.text import MIMEText

# def send_test_email():
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     smtp_user = 'emrah0denizer.gmail.com'
#     smtp_password = 'frxx edpt ktxq tuzq'

#     msg = MIMEText('Test e-postası gönderildi!')
#     msg['Subject'] = 'Test E-postası'
#     msg['From'] = smtp_user
#     msg['To'] = 'emrah0denizer.gmail.com'  # E-posta gönderim adresiniz

#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(smtp_user, smtp_password)
#         server.sendmail(smtp_user, [msg['To']], msg.as_string())

# send_test_email()
