"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, School, Student
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#@app.route('/user', methods=['GET'])
#def handle_hello():

#    response_body = {
#        "msg": "Hello, this is your GET /user response "
#    }

#    return jsonify(response_body), 200

@app.route('/school/<int:school_id>', methods=['GET'])
def school_data(school_id):

    school= School.query.get(school_id)
    
    return jsonify(school), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def user_data(user_id):

    user= User.query.get(user_id)
    
    return jsonify(user), 200

@app.route('/course/<int:course_id>', methods=['GET'])
def course_data(course_id):

    course= Course.query.get(course_id)
    
    return jsonify(course), 200

@app.route('/student/<int:student_id>', methods=['GET'])
def student_data(student_id):

    student= Student.query.get(student_id)
    
    return jsonify(student), 200

@app.route('/enrollment/', methods=['GET'])
def enrollment_data():

    

    enrollment= Enrollment.query.all()
    all_enrollment= list(map(lambda x: x.serialize(), enrollment))

    
    return jsonify(all_enrollment), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
