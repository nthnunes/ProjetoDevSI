from flask import Flask, Response, jsonify, request
from bson.objectid import ObjectId
from datetime import datetime
from database import dbConnection
from users import User
from local import Local

db = dbConnection("root", "devsiproject")

#opc = int(input("Run app:\n1 - Local\n2 - In my network\n3 - TCP Tunnel\nOption: "))
opc = 2

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
    query = coll.find_one({'email': req['email']})

    if query == None:
        return Response(status=403)

    if query['senha'] == req['senha']:
        return jsonify({'id': str(query['_id']), 'permissao': query['permissao']})
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


@app.route('/infos')
def infos():
    reservas = 0
    cancelamentos = 0
    ganhos = 0
    locados = 0
    locadosAno = 0

    coll = db.get_collection('reserva')
    start = datetime(datetime.now().year, datetime.now().month, 1)
    end = datetime(datetime.now().year, datetime.now().month, 30)

    query = coll.find({'status': 'aberto', 'data': {'$gte': start, '$lt': end}})
    for item in query:
        reservas = reservas + 1

    query = coll.find({'status': 'cancelado', 'data': {'$gte': start, '$lt': end}})
    for item in query:
        cancelamentos = cancelamentos + 1

    query = coll.find({'status': 'fechado', 'data': {'$gte': start, '$lt': end}})
    for item in query:
        ganhos = ganhos + item['valor']

    query = coll.find({'status': 'fechado', 'data': {'$gte': start, '$lt': end}})
    for item in query:
        locados = locados + 1

    start = datetime(datetime.now().year, 1, 1)
    end = datetime(datetime.now().year, 12, 30)
    query = coll.find({'status': 'fechado', 'data': {'$gte': start, '$lt': end}})
    for item in query:
        locadosAno = locadosAno + 1

    data = {
        'reservas': reservas,
        'cancelamentos': cancelamentos,
        'ganhos': ganhos,
        'locados': locados,
        'locadosAno': locadosAno
    }
    
    return jsonify(data)


# retorna as datas reservadas do calendário
@app.route('/calendar')
def calendar():
    # cria um objeto com as informações dos locais do BD
    coll = db.get_collection('local')
    query = coll.find()
    locais = []
    for local in query:
        locais.append(Local(local['nome'], local['valor'], str(local['_id'])))

    # identifica a quais locais as reservas pertecem e add ao respectivo objeto
    coll = db.get_collection('reserva')
    query = coll.find({"status": {'$ne': 'cancelado'}})
    for reserva in query:
        for local in locais:
            if local.getId() == str(reserva['id_local']):
                local.addReserva(str(reserva['_id']))

    # construção do json
    data = []
    for local in locais:
        days = []
        for i in local.getReservas():
            query = coll.find_one({"_id": ObjectId(i)})
            days.append(query['data'].strftime('%Y-%m-%d'))

        temp = {
            "nome": local.getNome(),
                "reservas": days
        }
        data.append(temp)

    res = {
        "data": data
    }

    return res


# nao terminado
@app.route('/searchCalendar')
def searchCalendar():
    req = request.get_json()
    coll = db.get_collection('reserva')
    find = datetime(req['year'], req['month'], req['day'])
    query = coll.find_one({"data": find})

    date = query['data']

    coll = db.get_collection('apto')
    query = coll.find_one({"_id": ObjectId(str(query['_id']))})

    print(query)

    return Response(status=200)


@app.route('/password', methods=['GET', 'POST'])
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