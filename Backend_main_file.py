from flask import Flask, request, make_response, jsonify
# import json
from method_call import MainMethods
# from flask_cors import CORS, cross_origin
from functools import wraps
import jwt
import datetime

method_call = MainMethods()

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SECRATE_KEY'] = 'THIS IS SECRATE KEY'


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
# @cross_origin()
def user_login():
    if not request.args.get('username') or not request.args.get('password'):
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})
    user = method_call.login_verification(request.args.get('username'), request.args.get('password'))
    print(user)

    if user['status'] is False:
        print(user)
        return {'status':False,"message":user['message']}
    if user['status'] is True:
        token = jwt.encode({'public_id': user['public_id'], 'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return {'token': token.decode('UTF-8')}


@app.route('/createAccount', methods=['GET', 'POST'])
# @cross_origin()
def newUSer():
    data = request.args
    username, email = data.get('name'), data.get('email')
    password = data.get('password')
    response = method_call.create_new_user(username, email, password)
    try:
        if not response['status']:
            return "already email exists"
        else:
            return response
    except Exception as error:
        print(error)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)
