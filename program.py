from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import json
import bsonjs
from bson.json_util import dumps
from bson.json_util import loads
import os
import psycopg2


 
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://admin:adminpassword@cluster0.cbya2.gcp.mongodb.net/Cluster0?retryWrites=true&w=majority"
mongo = PyMongo(app)

CORS(app)

# getCourses
@app.route("/programs")
def getAll():
    programs = mongo.db.program.find({})
    return dumps(programs)
    # return jsonify({'result' : programs })
    # return jsonify(json.dumps(programs, default=json_util.default))

@app.route("/programs/<int:programId>")
def getProgramWithId(programId):
    program = mongo.db.program.find_one({"programId" : programId})
    return dumps(program)

@app.route("/programs/progression")
def getProgramWithProgression():
    result = {}
    for data in mongo.db.program.find({}):
        progression = mongo.db.program.find_one({'programId' : data['programId']})
        result[data['programName']] = progression
    return jsonify(result)

@app.route("/programs/dataAnalytics")
def getProgramWithDataAnalytics():
    result = {}
    for data in mongo.db.program.find({}):
        dataAnalytics = mongo.db.dataAnalytics.find({'programId': data['programId']})
        result[data['programName']] = dataAnalytics
    return jsonify(result)

@app.route("/programs/Enroll/<int:studentId>")
def getProgramEnroll(studentId):
    result = {}
    progressionOfStudent = mongo.db.progression.find({"studentId": studentId})
    for item in progressionOfStudent:
        sessionid = item["sessionId"]
        print(sessionid)
        session = mongo.db.session.find_one({"sessionId" : sessionid})
        programId = session["programId"]
        program = json.loads(getProgramWithId(programId))
        result[program["programName"]] = {"currentSessionNo" : session["currentSessionNo"], "totalSessionNo" : session["totalSessionNo"] }
    return jsonify(result)

@app.route("/hello")
def mongoPop():
    count = 20
    number = 1
    programclass = ["Finance for future" , "Planning With Purpose", "Personal Spending 101", 'Business Ethics']
    for i in range(len(programclass)):
        count+=2 
        number += 1
        mongo.db.program.insert({"programId" : number,"programType" : "Secondary", "programName" : programclass[i] , "targetNoOfVolunteers" : count, "actualNoOfVolunteers" : count,
        "targetNoOfStudents" : count, "actualNoOfStudents" : count ,"attendee" : count}) 
    programs = mongo.db.program.find({})
    return dumps(programs)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0' , port=port, debug=False)





# mongo.db.session.insert({"programId" : count , "programName" : "Assure that every student is fully equipped." , "attendee" : count,
#         "courseMaterials" : "English Lesson" , "studentSubmissions" : count, "programId" : count, "dataAnalyticsId" : count,
#          "progressionId" : count , "milestonesId" : count, "totalSessionNo" : count }) 