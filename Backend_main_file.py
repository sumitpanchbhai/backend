from flask import Flask, request, make_response, jsonify
from method_call import MainMethods
from functools import wraps
import jwt
import datetime
from flask_cors import CORS, cross_origin

method_call = MainMethods()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THIS IS SECRATE KEY'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if token is None:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            validation = token.split(" ")
            data = jwt.decode(validation[1], app.config['SECRET_KEY'])
            current_user = method_call.user_details_public_id(data['public_id'])
        except:
            # print(token)
            return jsonify({'message': 'Token is invalid !!'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/login', methods=['GET'])
@cross_origin()
def user_login():
    if request.args.get('username') is not None:
        username = request.args.get('username')
    else:
        username = None
    if request.args.get('password') is not None:
        password = request.args.get('password')
    else:
        password =  None
    if username is None and password is None:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})
    user = method_call.login_verification(username=username, password =password)

    if user['status'] is False:
        return {'status':False,"message":user['message']}
    if user['status'] is True:
        token = jwt.encode({'public_id': user['public_id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return {'status': True, 'token': token}


@app.route('/createAccount', methods=['GET', 'POST'])
@cross_origin()
def newUSer():
    if request.args.get('username') is not None:
        username = request.args.get('username')
    else:
        username = None
    if request.args.get('email') is not None:
        email = request.args.get('email')
    else:
        email = None
    if request.args.get('password') is not None:
        password = request.args.get('password')
    else:
        password = None
    if request.args.get('name') is not None:
        name = request.args.get('name')
    else:
        name = None
    # data = request.args
    # username, email = data.get('name'), data.get('email')
    # password = data.get('password')
    response = method_call.create_new_user(username=username, email=email, password=password,name=name)
    print("printing response",response)
    try:
        if not response['status']:
            return "already email exists"
        else:
            return response
    except Exception as error:
        print(error)
    return response

@app.route('/validate_user',methods=['GET'])
def validate_user():
    try:
        if request.args.get('username') is not None:
            username = request.args.get('username')
        else:
            username = None
        validate_user = method_call.validate_user(username=username)
        return validate_user
    except Exception as error:
        return {'status': True, 'message': error}




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
