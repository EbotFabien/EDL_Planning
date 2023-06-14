from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin



db_participant = db.collection('participant')

participant = Blueprint('participant',__name__)


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@participant.route('/participant/ajouter', methods=['POST'])
def create():
    db_participant.document(request.json['id']).set(request.json)
    #temps,res_= db_participant.add(request.json)
    #todo = db_participant.document(res_.id).get()
    #finzl_= todo.to_dict()
    #finzl_['id_'] = res_.id
    #return jsonify(finzl_), 200
    return jsonify(request.json),200
    
@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@participant.route('/participant/tous', methods=['GET'])
def read():
    ''' all_todos = [doc.to_dict() for doc in db_participant.stream()]
    return jsonify(all_todos), 200 '''
    todo = db_participant.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        temp['_id'] = tod.id
        print(temp)
        final_.append(temp)
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@participant.route('/participant/signataire/<ide>', methods=['GET'])
def read_signe(ide):


    todo_id = str(ide)
    query_ref = db_participant.stream()
    all_todos = []
    for doc in query_ref:
        v=doc.to_dict()
        v['id']=doc.id
        try:
            if v['compte_client'] == todo_id:
                all_todos.append(v)
        except:
            pass
    return jsonify(all_todos), 200    
 

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@participant.route('/participant/<ide>', methods=['GET'])
def read_ind(ide):


    todo_id = str(ide)
    
    if todo_id:
        todo = db_participant.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@participant.route('/participant/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = db_participant.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            db_participant.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200
        
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@participant.route('/participant/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = db_participant.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        db_participant.document(todo_id).delete()
        return jsonify({"success": True}), 200
    

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@participant.route('/logement/user/<ide>', methods=['GET'])
def getparticipantByUser(idClient):
    
    todo = db_participant.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if str(temp['client']["_id"]) == str(idClient):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@participant.route('/participant/compte_client/<ide>', methods=['GET'])
def getParticipantByCompteClient(ide):
    
    todo = db_participant.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if str(temp['client']["_id"]) == str(ide):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@participant.route('/participant/compte_client/<ide>/<role>', methods=['GET'])
def getParticipant_RoleByCompteClient(ide,role):
    
    todo = db_participant.stream()
    role = db_participant.document(role).get()
    user_role = role.to_dict()
    
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if str(temp['participant']["id"]) == str(user_role) and str(temp["client"])==str(ide):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200
