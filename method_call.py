import pandas as pd
from dbConnection import DBConnection


# mail send
import smtplib
import ssl
from email.message import EmailMessage

class methodCall():
    def __init__(self):
        self.DBConnect = DBConnection()
    def get_logining(self,new_user=None,new_user_pass=None):
        new_db_connection = None
        user_verify = False
        try:
            try:
                if type(new_user) != str(new_user):
                    new_user=str(new_user)
                elif type(new_user_pass)!=str(new_user_pass):
                    new_user_pass = str(new_user_pass)
            except Exception as ex:
                return ex
            query = "select * from public.users"

            new_db_connection = self.DBConnect.get_connection()
            data = pd.read_sql_query(query,new_db_connection)

            if new_user in data['username'].tolist():
                if new_user_pass in data['password'].tolist():
                    user_verify=True

            return user_verify
        except Exception as ex:
            return ex
        # finally:
        #     if new_db_connection is not None:
        #         self.DBConnect.release_connection(new_db_connection)

    def create_new_user(self,new_user=None,new_user_pass=None,email_id=None,name=None):
        try:
            try:
                if type(new_user) != str(new_user):
                    new_user=str(new_user)
                elif type(new_user_pass)!=str(new_user_pass):
                    new_user_pass = str(new_user_pass)
                elif type(email_id) != str(email_id):
                    email_id = str(email_id)
                elif type(name)!=str(name):
                    name = str(name)
            except Exception as ex:
                return ex
            new_db_connection = self.DBConnect.get_connection()
            new_cursor = new_db_connection.cursor()
            query = f"insert into users(username,password,name,email) values('{new_user}','{new_user_pass}','{name}','{email_id}')"
            print(query)
            new_cursor.execute(query)
            new_db_connection.commit()
            self.sendMail(email_sender='tsumit1998@gmail.com',email_receiver=email_id)
            return "succesfull created new user"
        except Exception as ex:
            return ex

    def sendMail(self,email_sender=None,email_receiver=None):
        # Define email sender and receiver
        # email_sender = 'tsumit1998@gmail.com'
        email_sender = email_sender
        # email_password = 'asdf_445@hajmola'
        email_password = 'jomqqljkblldciay'  # generated password using (https://myaccount.google.com/u/0/apppasswords?pli=1&rapt=AEjHL4NmeBXL9UOfglxEegUP40kYiZyMy7waAswuKoiSAozlSNlMwmOOv3LEu8bg30AVfaeLACOfQ-A08t63ZaL2rQcaDX6IaQ)
        email_receiver = email_receiver
        # email_receiver = 'sumitpanchbhai1998@gmail.com'

        # Set the subject and body of the email
        subject = 'new user created'
        body = """
                Thank you to create an accound and be the part of the it......!
                """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())