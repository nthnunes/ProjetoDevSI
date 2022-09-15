from flask import Flask, Response, jsonify, request
from bson.objectid import ObjectId
from database import dbConnection
from users import User

print("$ MongoDB Credentials:")
db = dbConnection(input("Username: "), input("Password: "))

opc = int(input("Run app:\n1 - Local\n2 - In my network\n3 - TCP Tunnel\nOption: "))

app = Flask(__name__)
if opc == 3:
    from flask_ngrok import run_with_ngrok
    run_with_ngrok(app)

@app.route('/')
def homepage():
    return jsonify({"Name": "Condominium API", "Status": "OK", "Author": "Nathan Nunes"})


@app.route('/login')
def login():
    req = request.get_json()
    coll = db.get_collection('users')
    data = coll.find_one({'email': req['email']})

    if data == None:
        return Response(status=403)

    if data['senha'] == req['senha']:
        return jsonify({'id': str(data['_id']), 'permissao': data['permissao']})
    else:
        return Response(status=401)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    req = request.get_json()
    user = User(req['email'], req['senha'], req['nome'], req['telefone'], False)

    data = {
        "email": user.getEmail(),
        "senha": user.getSenha(),
        "nome": user.getNome(),
        "telefone": user.getTelefone(),
        "permissao": user.getPermissao()
    }
    coll = db.get_collection('users')
    coll.insert_one(data)
    
    return Response(status=200)


@app.route('/password')
def changePassword():
    req = request.get_json()
    coll = db.get_collection('users')
    coll.update_one({"_id": ObjectId(req['id'])}, {'$set': {"senha": req['password']}})

    return Response(status=200)


if __name__ == '__main__':
    if opc == 1:
        app.run(host="localhost", port=5000)
    elif opc == 2:
        app.run(host="0.0.0.0", port=3000)
    elif opc == 3:
        app.run()
    else:
        print("-> Invalid option.")