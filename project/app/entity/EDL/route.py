from flask import app, render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin
from flask_firebase_admin import FirebaseAdmin      
from firebase_admin import  storage
from flask import Flask, request
import os
import shutil


db_participant = db.collection('participant')
db_edl= db.collection('edl')
db_user = db.collection('user')
db_rdv = db.collection('rdv')
db_logement = db.collection('logement')

edl = Blueprint('edl',__name__)

def getDataByID(bd,id):
        todo = bd.document(id).get()
        final_= todo.to_dict()
      #  final_['_id'] = id
        return final_
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@edl.route('/edl/ajouter', methods=['POST'])
def create():
    users ={}
    participants = {}
    rdvs = {}
    intervenants = {}
    signataires = {}
    i = 1
    data_ = request.json
    for signataire in data_["signataires"].values():
        if signataire['table'] =="participant":
            signataires["signataire"+str(i)] =  getDataByID(db_participant,signataire['id'])
            i+=1
        else:
            signataires["signataire"+str(i)] =  getDataByID(db_user,signataire['id'])
            i+=1
    data_['signataires']=signataires
    
    i=1
    for rdv in data_['rdvs'].values():
        rdv["intervenant"]= getDataByID(db_user,rdv['intervenant'])
    
    '''   uploaded_file =request.files['photo']
    file_path = os.path.join( "/",uploaded_file.filename)
    uploaded_file.save(file_path)
    url=file_path
    fileName = url
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
       
    blob.make_public()
           
    data_['photo'] = blob.public_url '''     
    data_['logement'] = getDataByID(db_logement,data_['logement'])
    data_['user'] = getDataByID(db_user,data_['user'])
 
    temps,res_= db_edl.add(data_)
    todo = db_edl.document(res_.id).get()
    finzl_= todo.to_dict()
    finzl_['id_'] = res_.id
    return jsonify(finzl_), 200
        
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@edl.route('/edl/update/<ide>', methods=['PUT'])
def update(ide):
    todo = db_edl.document(ide)
    final_ = {}
     
    if todo is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        todo.update(request.json)
        todo = db_edl.document(ide).get()
        final_= todo.to_dict()
        
    final_["_id"] = ide
    print(final_["_id"])
    return jsonify(final_), 200     
    
@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/tous', methods=['GET'])
def read():
    todo = db_edl.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        temp['_id'] = tod.id
        final_.append(temp)
    return jsonify(final_), 200
    

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/<ide>', methods=['GET'])
def read_ind(ide):
    todo = db_edl.document(ide)
    final_={}
    if todo is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        final_= todo.get().to_dict()  
    final_["_id"] = ide
    return jsonify(final_), 200
        
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@edl.route('/edl/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = db_edl.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        db_edl.document(todo_id).delete()
        return jsonify({"success": True}), 200
    
    
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@edl.route('/picture', methods=['POST'])
def send_individual_picture():
       
       uploaded_file =request.files['photo']
       file_path = os.path.join( "/",uploaded_file.filename)
       uploaded_file.save(file_path)
       url=file_path
       fileName = url
       bucket = storage.bucket()
       blob = bucket.blob(fileName)
       blob.upload_from_filename(fileName)
       
       blob.make_public()
       
       
       print(blob.public_url)
       return jsonify({"success": True}), 200

    
    
    
''' @cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@edl.route('/synchro', methods=['GET', 'DELETE'])
def synchro(ide):
    todo_id = str(ide)
    todo = db_participant.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        db_participant.document(todo_id).delete()
        return jsonify({"success": True}), 200 '''