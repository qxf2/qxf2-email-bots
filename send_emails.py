"""
This module will be used to send out emails
"""

import os,sys,time,smtplib,email,datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import email_credentials as conf_file

class SMTP_Email_Util:
    "Class to interact with SMTP servers"

    def connect(self,smtp_host,smtp_port):
        "Connect with the host"
        self.mail = smtplib.SMTP(smtp_host,smtp_port)
        self.mail.starttls()
        
        return self.mail


    def login(self,username,password):
        "Login to the email"
        result_flag = False
        try:
            self.mail.login(username,password)
        except Exception as e:
            print('\nException in send_emails.login')
            print('PYTHON SAYS:')
            print(e)
            print('\n')
        else:
            result_flag = True

        return result_flag

    def create_body(self,recepient,sender,subject,message):
        "Create an email body based on the sender, receiver, subject and message"
        body = '\r\n'.join(['To: %s' %recepient,
        'From: %s' %sender,
        'Subject: %s' %subject,
        '', 
        message])

        return body 

    def send_email(self,sender,recepient,message):
        "Send an email to a recepient"
        result_flag = False
        try:
            self.mail.sendmail(sender,recepient,message)
        except Exception as e:
            print('\nException in send_emails.send_email')
            print('PYTHON SAYS:')
            print(e)
            print('\n')
        else:
            result_flag = True

        return result_flag

    def quit(self):
        "Quit the connection"
        self.mail.quit()

#---EXAMPLE USAGE---
if __name__=='__main__':
    #Fetching conf details from the conf file
    smtp_host = conf_file.SMTP_HOST
    smtp_port = conf_file.SMTP_PORT
    username = conf_file.USERNAME
    password = conf_file.PASSWORD

    #Initialize the email object
    email_obj = SMTP_Email_Util()

    #Connect to the SMTP host
    email_obj.connect(smtp_host,smtp_port)

    #Login
    if email_obj.login(username,password):
        print("Successfully logged in.")
    else:
        print("Failed to login")

    subject = "Test Email"
    message = "I am sending this email via Python."
    body = email_obj.create_body(username,username,subject,message)
    email_obj.send_email(username,username,body)

    email_obj.quit()