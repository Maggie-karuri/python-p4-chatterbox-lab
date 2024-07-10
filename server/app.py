from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods =['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            msg_dict=message.to_dict()
            messages.append(msg_dict)
        response = make_response(messages,200)
        return response
    
    elif request.method == 'POST':
        new_msg = Message(
            body = request.get_json()["body"],
            username = request.get_json()["username"]
        )
        db.session.add(new_msg)
        db.session.commit()
        msg_dict=new_msg.to_dict()
        response = make_response(msg_dict,201)
        return response

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'GET':
        msg_dict =message.to_dict()
        response = make_response(msg_dict,200) 
        return response
    
    elif request.method == 'PATCH':
        for attr in request.get_json():
            setattr(message,attr,request.get_json()[attr])
        db.session.add(message)
        db.session.commit()
        msg_dict=message.to_dict()
        response= make_response(msg_dict,200)
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        res_body = {"delete_successful":True}
        return make_response(res_body, 200)

if __name__ == '__main__':
    app.run(port=5555)