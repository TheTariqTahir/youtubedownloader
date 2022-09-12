
# str = string.ascii_letters

# # result = ''.join(random.choice(str)for i in range(12))
# # print(result)

# email = 'abc@abc.com'
# # db.child('data').child('id').child(email).set({"email":email,'password':'abc123'})

# # print(email.split('@')[0])

import pyrebase
import random
import string
config = {
  'apiKey': "AIzaSyAYaA6X_Yx5fr0tMmDzZiYIdjJL2LvOSNk",
  'authDomain': "downloader-97343.firebaseapp.com",
  'projectId': "downloader-97343",
  'storageBucket': "downloader-97343.appspot.com",
  'messagingSenderId': "213069231530",
  'appId': "1:213069231530:web:72891f5d9373e437b7a7d3",
  'measurementId': "G-HN4JYZ8P8Z",
  'databaseURL':'https://downloader-97343-default-rtdb.firebaseio.com/'
  }

firebase = pyrebase.initialize_app(config)

db = firebase.database()
def make_password(name,email_):
    str = string.ascii_letters
    try:
        email = email_.split('@')[0]
        password = ''.join(random.choice(str)for i in range(12))
        db.child('data').child(email).set({"name":name,"email":email_,'password':password,"active":'False'})
        return email,password
    except Exception as e:
        return e


# def check_password(email_,password):
#     email = email_.split('@')[0]
#     data = db.child('data').child(email).get()
#     print(data.val()['active'])
#     if data.val()['active'] == 'False':
#         if email_ == (data.val()['email']) and password==data.val()['password']:
#             db.child('data').child(email).update({"active":'True'})
#             return True
#     else:
#         print('Already have active account')
        

# a,b =(make_password('test','a@b.com'))
# # print(check_password('a@b.com','abc123'))
import requests as r
try:
    x=r.get('https://www.google.com')
    if x.status_code=='200':
        pass
    else:
        print('internet error')
        # self.show_dialog('Error','Internet Connection Error')
except Exception as e:
    print(e)
    # self.show_dialog('Error',str(e))