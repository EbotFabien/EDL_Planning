from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin



db_user = db.collection('user')

user = Blueprint('user',__name__)

def getDataByID(bd,id):
        todo = bd.document(id).get()
        final_= todo.to_dict()
        final_['_id'] = id
        return final_

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@user.route('/user/ajouter', methods=['POST'])
def create():
    db_user.document(request.json['id']).set(request.json)
    '''data_= request.json
    
    temps,res_= db_user.add(data_)
    todo = db_user.document(res_.id).get()
    finzl_= todo.to_dict()
    finzl_['id_'] = res_.id
    return jsonify(finzl_), 200'''
    return 200
     
     
  
      
    
@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@user.route('/user/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in db_user.stream()]
    return jsonify(all_todos), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@user.route('/user/<ide>', methods=['GET'])
def read_ind(ide):


    todo_id = str(ide)
    
    if todo_id:
        todo = db_user.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@user.route('/user/signataire/<ide>', methods=['GET'])
def read_signe(ide):


    todo_id = str(ide)
    query_ref = db_user.where(u'compte_client.id', u'==', todo_id)
    all_todos = []
    for doc in query_ref.stream():
        v=doc.to_dict()
        v['id']=doc.id
        all_todos.append(v)
    return jsonify(all_todos), 200    
    


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@user.route('/user/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = db_user.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            db_user.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200
        
@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@user.route('/user/delete/<ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = db_user.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        db_user.document(todo_id).delete()
        return jsonify({"success": True}), 200