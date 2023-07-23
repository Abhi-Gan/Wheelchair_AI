# flask --app arcade_server run
# a flask-restful api
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
# AI logic is on different module
import wheelchair_ai
import json
# fix cors issues?
from flask_cors import CORS

# create flask restful app
app = Flask(__name__)
# api object
api = Api(app)

CORS(app)

# each endpoint matches with a resource (which has specific class)

# test resource
class Hello(Resource):
    # get requests
    def get(self):
        return jsonify({'result':'hello Bob'})
    # post requests
    def post(self):
        data = request.get_json()
        print("chkpt a")
        print(data)
        response = jsonify({'result':f'received {data}'})
        response.status_code = 201
        return response # 201 is success status code?
    
# simple resource using params
class QuickMaths(Resource):
    # multiplies 2 numbers
    # requests
    def post(self):
        args = request.get_json()
        a = args["a"]
        b = args["b"]
        return a*b

# responds to arcade prompt
class curbie_prompt(Resource):
    def post(self):
        args = request.get_json()
        print(f"args = {args}")

        usr_quest = args["query"]
        
        result = f"received query: '{usr_quest}'" # wheelchair_ai.run_generic_query(usr_quest)
        print(result)
        return result
    
# gets top 10 reddit posts
class top_reddit_posts(Resource):
    def get(self):
        n = request.args.get('n', default=10)
        return wheelchair_ai.get_top_n_reddit(n)

# add resources to api
api.add_resource(Hello, '/')
api.add_resource(QuickMaths, '/math')
api.add_resource(curbie_prompt, '/curbie_prompt')
api.add_resource(top_reddit_posts, '/top_reddit_posts')

# run flask app
if __name__ == '__main__':
    app.run(debug=True)