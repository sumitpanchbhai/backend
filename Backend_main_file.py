from flask import Flask,request
import json
from method_call import methodCall
from flask_cors import CORS, cross_origin

method_call = methodCall()

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/login',methods=['GET'])
@cross_origin()
def user_login():
    user_verify = False
    try:
        if request.args.get('username') is not None:
            new_user = request.args.get('username')
        else:
            new_user=None
        if request.args.get('password') is not None:
            new_user_pass = request.args.get('password')
        else:
            new_user_pass = None
        # login user logic
        data = method_call.get_logining(new_user=new_user,new_user_pass=new_user_pass)
        print("prinintg data",data)
        return json.dumps({"data": data,"status":'S'})
    # login user logic
    except Exception as ex:
        return json.dumps({"data": ex,"status":'E'})


@app.route('/createAccount',methods=['GET','POST'])
@cross_origin()
def newUSer():
    try:
        if request.args.get('username')!=None:
            new_user = request.args.get('username')
        else:
            return 'invalid user passes'
        if request.args.get('password')!=None:
            new_user_pass = request.args.get('password')
        else:
            return "invalid user's password passes"
        if request.args.get('name')!=None:
            name = request.args.get('name')
        else:
            return "invalid user's name passes"
        if request.args.get('email_id')!=None:
            email_id = request.args.get('email_id')
        else:
            return "invalid user's email_id passes"
        data = method_call.create_new_user(new_user=new_user,new_user_pass=new_user_pass,name=name,email_id=email_id)
        print(data)
        return json.dumps({
            'message':data,
            "status":'S'
        })
    except Exception as ex:
        return json.dumps({
            'message':ex,
            "status":'E'
        })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)

