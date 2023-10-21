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

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages=Message.query.all()
        messages_to_pass=[]
        for message in messages:
            messages_dict = {
                "id":message.id,
            "body":message.body,
            "username":message.username,
            "created_at":message.created_at,
            "updated_at":message.updated_at,
            }
            messages_to_pass.append(messages_dict)
        return make_response(jsonify(messages_to_pass), 200)
    elif request.method == "POST":
        body=request.form.get("body")
        username=request.form.get("username")
        message=Message(body=body, username=username)
        db.session.add(message)
        db.session.commit()

        message_dict =  {
            "id":message.id,
            "body":message.body,
            "username":message.username,
            "created_at":message.created_at,
            "updated_at":message.updated_at,
            }

        return make_response(jsonify(message_dict), 200)
    return ''

@app.route('/messages/<int:id>', methods=["PATCH", "DELETE"])
def messages_by_id(id):
    message=Message.query.get(id)
    if not message:
            return make_response("Message does not exist", 404)
    if request.method == "PATCH":
        
        
        form_data = request.form.to_dict()

    # Iterate through the form data and update the model dynamically
        for field, value in form_data.items():
            if hasattr(message, field):
                setattr(message, field, value)
        db.session.commit()
        message_dict =  {
            "id":message.id,
            "body":message.body,
            "username":message.username,
            "created_at":message.created_at,
            "updated_at":message.updated_at,
            }

        return make_response(jsonify(message_dict), 200)
    
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        return make_response("deleted successfully", 200)



if __name__ == '__main__':
    app.run(port=5555)
