"""
This script contains general code needed to send emails.
"""
import os,sys,time,imaplib,email,datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import email_credentials as conf_file

class Email_Util:
    "Class to interact with IMAP servers"

    def connect(self,imap_host):
        "Connect with the host"
        self.mail = imaplib.IMAP4_SSL(imap_host)
        
        return self.mail


    def login(self,username,password):
        "Login to the email"
        result_flag = False
        try:
            self.mail.login(username,password)
        except Exception as e:
            print('\nException in Email_Util.login')
            print('PYTHON SAYS:')
            print(e)
            print('\n')
        else:
            result_flag = True

        return result_flag


    def get_folders(self):
        "Return a list of folders"
        return self.mail.list()


    def select_folder(self,folder):
        "Select the given folder if it exists. E.g.: [Gmail]/Trash"
        result_flag = False
        response = self.mail.select(folder)
        if response[0] == 'OK':
            result_flag = True

        return result_flag


    def get_latest_email_uid(self,subject=None,sender=None,time_delta=10,wait_time=300):
        "Search for a subject and return the latest unique ids of the emails"
        uid = None
        time_elapsed = 0
        search_string = ''
        if subject is None and sender is None:
            search_string = 'ALL'

        if subject is None and sender is not None:
            search_string = '(FROM "{sender}")'.format(sender=sender)

        if subject is not None and sender is None:
            search_string = '(SUBJECT "{subject}")'.format(subject=subject)

        if subject is not None and sender is not None:
            search_string = '(FROM "{sender}" SUBJECT "{subject}")'.format(sender=sender,subject=subject)

        print("  - Automation will be in search/wait mode for max %s seconds"%wait_time) 
        while (time_elapsed < wait_time and uid is None):
            time.sleep(time_delta)
            result,data = self.mail.uid('search',None,str(search_string))

            if data[0].strip() != '': #Check for an empty set
                uid = data[0].split()[-1]
                
            time_elapsed += time_delta

        return uid.decode('utf-8')


    def fetch_email_body(self,uid):
        "Fetch the email body for a given uid"
        email_body = []
        if uid is not None:
            result,data = self.mail.uid('fetch',uid,'(RFC822)')
            raw_email = data[0][1].decode('utf-8')
            email_msg = email.message_from_string(raw_email)
            email_body = self.get_email_body(email_msg)

        return email_body
        
    
    def get_email_body(self,email_msg):
        "Parse out the text of the email message. Handle multipart messages"
        email_body = []
        maintype = email_msg.get_content_maintype()
        if maintype == 'multipart': 
            for part in email_msg.get_payload():
                if part.get_content_maintype() == 'text':
                    email_body.append(part.get_payload())
        elif maintype == 'text':
            email_body.append(email_msg.get_payload())

        return email_body


    def logout(self):
        "Logout"
        result_flag = False
        response, data = self.mail.logout()
        if response == 'BYE':
            result_flag = True

        return result_flag


#---EXAMPLE USAGE---
if __name__=='__main__':
    #Fetching conf details from the conf file
    imap_host = conf_file.IMAPHOST
    username = conf_file.USERNAME
    password = conf_file.PASSWORD

    #Initialize the email object
    email_obj = Email_Util()

    #Connect to the IMAP host
    email_obj.connect(imap_host)
    
    #Login
    if email_obj.login(username,password):
        print("Successfully logged in.")
    else:
        print("Failed to login")
    email_obj.select_folder("Inbox")
    latest_email_uid = email_obj.get_latest_email_uid()
    latest_message = email_obj.fetch_email_body(latest_email_uid)
    print(latest_message)