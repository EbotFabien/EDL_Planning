from flask import app, render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin
#from flask_firebase_admin import FirebaseAdmin      
from firebase_admin import  storage
from flask import Flask, request
import os
import shutil

    
db_participant = db.collection('participant')
db_edl= db.collection('edl')
db_user = db.collection('user')
db_rdv = db.collection('rdv')
db_logement = db.collection('logement')
db_type_log = db.collection('type_log')

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
        if rdv["intervenant"]['table'] =="participant":
            rdv["intervenant"] =  getDataByID(db_participant,rdv["intervenant"]['id'])
        else:
            rdv["intervenant"] =  getDataByID(db_user,rdv["intervenant"]['id'])
    
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
    id_user= data_['created_by']
    id_logement=data_['logement']   
    data_['logement'] = getDataByID(db_logement,data_['logement'])
    data_['created_by'] = getDataByID(db_user,data_['created_by'])
    data_['logement']['_id']=id_logement
    data_['created_by']['_id']= id_user
 
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
        print(temp)
        final_.append(temp)
    return jsonify(final_), 200
    
#done

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
@edl.route('/edl/delete/<ide>', methods=['GET', 'DELETE'])
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

    
    
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@edl.route('/edl/synch/<ide>', methods=['POST', 'PUT'])
def synch(ide ):
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
         return jsonify(final_), 20
        
        
        
@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/compte_client/<idClient>', methods=['GET'])
def getEdlByCompteClient(idClient):
    todo = db_edl.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if temp['logement']['client']["_id"] == str(idClient):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/user/<ide>', methods=['GET'])
def getEdlByUser(ide):
    todo = db_edl.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if str(temp['user']['_id']) == str(ide):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200


@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/logement/cc/<ide>', methods=['GET'])
def getLogementByCompteClient(ide):
    todo = db_logement.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if str(temp['client']['_id']) == str(ide):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200



@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/user_compte_client/<ide>', methods=['GET'])
def getUserByCompteClient(idClient):
    
    todo = db_user.stream()
    final_ = []
    temp = {}
    for tod in todo :
       temp = tod.to_dict() 
       if str(temp['logement']['user']["_id"]) == str(idClient):
    
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200


@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/part_compte_client/<id>', methods=['GET'])
def getParticipantByCompteClient(id):
    
    todo = db_participant.stream()
    final_ = []
    temp = {}
    for tod in todo :
       temp = tod.to_dict() 
       if str(temp['logement']['user']["_id"]) == str(id):
    
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200


@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/pie_cles_cpte/<id>', methods=['GET'])
def getPieceClesCmpteurByTypLog(id):
    
    final_ = []
    temp = {}
    todo = db_type_log.stream()    
    
    for tod in todo:
        temp = tod.to_dict()
        #temp['_id'] = tod.id
        
        final={
            'piece':temp['piece'],
            'cles':temp['cles'],
            'compteur':temp['compteur']
        }
        print(temp)
        final_.append(final)
    return jsonify(final_), 200
    
    


''' @cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@edl.route('/edl/edl_ac/<id_ac>', methods=['GET'])
def getEdlByAgentconstat(id_ac):
    todo = db_edl.stream()
    final_ = []
    temp = {}
    for tod in todo :
       temp = tod.to_dict() 
       if str(temp['signataires']['signataire']["_id"]) == str(id_ac):
    
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200 '''



