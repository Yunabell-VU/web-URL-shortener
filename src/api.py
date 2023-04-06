# This file defines APIs the server provides
# Flask library is used to route APIs
# The use of flask references the official documentation of flask:
# https://flask.palletsprojects.com/en/2.2.x/quickstart/

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from apiHandler import apiHandler


app = Flask(__name__)
cors = CORS(app) # cors is added in advance to allow cors requests
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=["GET"])
@cross_origin()
def get_keys():
    keys = apiHandler.get_keys()
    return keys

@app.route('/', methods=["DELETE"])
@cross_origin()
def delete_index():
    return "Error: Invalid request", 404

@app.route('/<string:url_id>', methods=["GET"])
@cross_origin()
def get_url(url_id):
    url = apiHandler.get_url(url_id)
    if url == None:
        return "Error: URL id NOT FOUND", 404
    return url, 301

@app.route('/', methods=["POST"])
@cross_origin()
def post_url():
    if request.method == 'POST':
        get_data=request.args
        get_dict = get_data.to_dict()
        url = get_dict['url']
        if(apiHandler.verify_url(url)):
            if(apiHandler.detect_duplicates(url)):
                return "Error: URL already exists", 400
            
            response = apiHandler.create_url(url)
            return response, 201
        else:
            return "Error: Invalid URL", 400

@app.route('/<string:url_id>', methods=["DELETE"])
@cross_origin()
def delete_url(url_id):
    url = apiHandler.get_url(url_id)
    if url == None:
        return "Error: URL id NOT FOUND", 404
    else:
        apiHandler.delete_url(url_id)
        return "Content deleted", 204

@app.route('/<string:url_id>', methods=["PUT"])
@cross_origin()
def update_url(url_id):
    url = apiHandler.get_url(url_id)
    if url == None:
        return "Error: URL id NOT FOUND", 404
    
    get_data=request.args
    get_dict = get_data.to_dict()
    url = get_dict['url']

    if apiHandler.verify_url(url):
        if(apiHandler.detect_duplicates(url)):
            return "Error: URL already exists", 400
        apiHandler.edit_url(url_id, url)
        return "URL Updated", 200
    else:
        return "Invalid URL to update", 400
        