from flask_pymongo import pymongo
from flask import jsonify, request
# import pandas as pd

con_string = "mongodb+srv://task2:task2@cluster0.w5ng2it.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('Demo')

user_collection = pymongo.collection.Collection(db, 'Test')
print("MongoDB connected Successfully")

def route_endpoint(endpoints):
    @endpoints.route('/POSTData', methods=['POST'])
    def POSTData():
        resp = {}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"Success! The User Data has been successfully stored into your database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/GETData', methods=['GET'])
    def GETData():
        resp = {}
        try:
            users = user_collection.find({})  
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"Successful."
            }
            output = [{'Name' : user['Name'],'Age' : user['Age'], 'Sex' : user['Sex'], 'Practice' : user['Practice']} for user in users]   #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/PUTData',methods=['PUT'])
    def PUTData():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"Name":req_body['Name']}, {"$set": req_body['body']})
            print("Successful.")
            status = {
                "statusCode":"200",
                "statusMessage":"Success! The User Data has now been updated."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/DELETEData',methods=['DELETE'])
    def DELETEData():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"ALERT! An user has been deleted from your database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    
    return endpoints