import pandas as pd
from dbConnection import DBConnections
import bcrypt
import uuid
import datetime
from validate_email_address import validate_email
# mail send
import smtplib
import ssl
from email.message import EmailMessage


class MainMethods:
    def __init__(self):
        self.db = DBConnections()

    def login_verification(self, username=None, password=None):
        conn = None
        query = f"""select username,password,email,public_id from project_1.user_details where username = '{username}'"""
        try:
            conn = self.db.get_db_connection()
            data = pd.read_sql(query, conn).to_dict()

            if len(data['password']) == 1 and bcrypt.checkpw(password.encode('utf-8'),
                                                             bytes(data['password'][0], encoding='utf-8')):
                email = data['email'][0]
                public_id = data['public_id'][0]
                return {'status': True, 'username': username, 'password': password, 'email': email,
                        'public_id': public_id}
            elif len(data['username']) == 0:
                return {'status': False, 'message': 'user doesnt exist or enter correct username'}
            else:
                return {'status': False, 'message': "enter correct password"}
        except Exception as error:
            # print(error)
            return {'status': False, 'message': error}
        finally:
            if conn is not None:
                conn.close()

    def user_details_public_id(self, public_id):
        conn = None
        query = f'''select * from project_1.user_details where public_id = '{public_id}' '''
        try:
            conn = self.db.get_db_connection()
            data = pd.read_sql_query(query, conn).to_dict()
            print(data)
            return {'status': True, 'username': data['username']}
        except Exception as error:
            return error

    def create_new_user(self, username=None, password=None, email=None):
        conn = None
        cur = None
        public_id = uuid.uuid1()
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(str(password))
        created_on = datetime.datetime.now()
        select_query = f"""select username,password,email,public_id from project_1.user_details 
                        where email = '{email}' """
        select_usernames = '''select username from project_1.user_details'''
        insert_query = f"""insert into project_1.user_details (username,public_id,password,created_on,email) 
                       values ('{username}','{public_id}','{password.decode()}','{created_on}','{email}')"""
        try:
            conn = self.db.get_db_connection()
            email_list = pd.read_sql(select_query, conn).to_dict(orient='list')['email']
            username_list = pd.read_sql(select_usernames, conn).to_dict(orient='list')['username']
            print(username_list)
            print(email_list)
            print(public_id)
            print(insert_query)

            if len(email_list) == 1:
                return {'status': False, "message": "email already got registered"}
            elif len(email_list) == 0:
                count = 0
                for i in username_list:
                    if i == username:
                        count = count + 1
                        return {"status": False, "message": "username exists"}
                    else:
                        continue

                if validate_email(email):
                    cur = conn.cursor()
                    cur.execute(insert_query)
                    conn.commit()
                    return {'status': True, "message": 'registered succesfully'}
                else:
                    return {"status": False, "message": "enter valid mail"}
        except Exception as error:
            print(error)
            return error
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    def sendMail(self, email_sender=None, email_receiver=None):
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

# main = methodCall()
# print(main.login_verification('fjdsfhuus', 'nsbchjdvs'))
# print(main.create_new_user('saikrishna','saikrishna344','saikrishna'))
