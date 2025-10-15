"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/health-check',methods=['GET'])
def health_check():
    return jsonify('ok')

@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members,
                     "len": len(members)
                     
                     }
    return jsonify(members), 200



@app.route('/members/<int:theid>', methods=['GET'])
def get_member(theid):
    member = jackson_family.get_member(theid)
    try:
        if member:
            response_body = member
            return jsonify(response_body),200
        else:
            return jsonify({
                "message": "Member not found"
            }),400

    except Exception as error: return jsonify("Error de la plataforma 500 internal server error"),500

@app.route('/members', methods=['POST'])
def post_member():
    
    data = request.get_json()
    response = jackson_family.add_member(data)
    if response:
        return jsonify(response),200
    else:
        return jsonify("error"),400
    

@app.route('/members/<int:theid>', methods=['DELETE'])
def del_member(theid):
    response = jackson_family.delete_member(theid)
    if response:
        return jsonify({"done" : True}),200
    else:
        return jsonify({"done" : False}),400

# This only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
