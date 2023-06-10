from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin



db_logement = db.collection('logement')

db_user = db.collection('user')

logement = Blueprint('logement',__name__)


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@logement.route('/logement/ajouter', methods=['POST'])
def create():
    temps,res_= db_logement.add(request.json)
    todo = db_logement.document(res_.id).get()
    finzl_= todo.to_dict()
    finzl_['id_'] = res_.id
    return jsonify(finzl_), 200
    
@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@logement.route('/logement/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in db_logement.stream()]
    return jsonify(all_todos), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@logement.route('/logement/<ide>', methods=['GET'])
def read_ind(ide):


    todo_id = str(ide)
    
    if todo_id:
        todo = db_logement.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@logement.route('/logement/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = db_logement.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            db_logement.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200
        
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@logement.route('/logement/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = db_logement.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        db_logement.document(todo_id).delete()
        return jsonify({"success": True}), 200
    
@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@logement.route('/logement/compte_client/<ide>', methods=['GET'])
def getLogementByCompteClient(idClient):
    
    todo = db_logement.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if str(temp['client']["_id"]) == str(idClient):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@logement.route('/logement/user/<ide>', methods=['GET'])
def getLogementByUser(iduser):
    user= db_user.document(iduser).get()
    client=user.to_dict()
    
    todo = db_logement.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        if str(temp['client']["_id"]) == str(client['compte_client']):
            temp['_id'] = tod.id
            final_.append(temp)
    return jsonify(final_), 200