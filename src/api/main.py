from flask import Flask, Response, request
from bson.objectid import ObjectId
from datetime import datetime
from database import dbConnection
from users import User
from apto import Apto
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
    return {"Name": "Condominium API", "Status": "OK", "Author": "Nathan Nunes"}


@app.route('/login')
def login():
    req = request.get_json()
    coll = db.get_collection('users')
    query = coll.find_one({'email': req['email']})

    if query == None:
        return Response(status=403)

    if query['senha'] == req['senha']:
        if query['permissao'] == True:
            return {'id': str(query['_id']), 'permissao': query['permissao']}
        else:
            return {'id': str(query['_id']), 'permissao': query['permissao'], 'nome': query['nome']}
    else:
        return Response(status=401)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    req = request.get_json()

    coll = db.get_collection('users')
    query = coll.find_one({'email': req['email']})
    if query != None:
        return Response(status=401)

    coll = db.get_collection('apto')
    query = coll.find_one({'token': req['token']})

    if query == None:
        return Response(status=401)

    if 'id_user' in query:
        apto = Apto(query['descricao'], query['numero'], str(query['_id']), str(query['id_user']))
        user = User(req['email'], req['senha'], req['nome'], req['telefone'], False)

        coll.update_one({"token": req['token']}, {'$set': {'token': apto.getToken()}})

        coll = db.get_collection('users')
        coll.update_one({"_id": query['id_user']}, {'$set': {
            "email": user.getEmail(),
            "senha": user.getSenha(),
            "nome": user.getNome(),
            "telefone": user.getTelefone(),
            "permissao": user.getPermissao()
        }})
    else:
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
        query = coll.find_one({'email': user.getEmail()})

        coll = db.get_collection('apto')
        coll.update_one({"token": req['token']}, {'$set': {'id_user': query['_id']}})
    
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
    
    return data


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


# busca informações de uma reserva
@app.route('/searchCalendar')
def searchCalendar():
    req = request.get_json()

    # busca a data recebida na tabela reserva
    coll = db.get_collection('reserva')
    find = datetime(req['year'], req['month'], req['day'])
    query = coll.find_one({"data": find})

    # salva o valor da reserva encontrada antes da nova query
    valor = query['valor']

    # busca o apartamento que fez a reserva
    coll = db.get_collection('apto')
    query = coll.find_one({"_id": query['id_apto']})

    # busca o usuário que fez a reserva
    coll = db.get_collection('users')
    query = coll.find_one({"_id": query['id_user']})

    data = {
        'nome': query['nome'],
        'email': query['email'],
        'telefone': query['telefone'],
        'valor': valor
    }

    return data


@app.route('/recent')
def recent():
    req = request.get_json()
    coll = db.get_collection('users')
    query = coll.find_one({"_id": ObjectId(req['id'])})

    if query['permissao'] == True:
        coll = db.get_collection('reserva')

        start = datetime(datetime.now().year, datetime.now().month, 1)
        end = datetime(datetime.now().year, datetime.now().month, 30)
        
        query = coll.find({'status': 'aberto', 'data': {'$gte': start, '$lt': end}})

        data = []
        for reserva in query:
            date = reserva['data']
            idLocal = reserva['id_local']

            coll = db.get_collection('apto')
            query = coll.find_one({"_id": reserva['id_apto']})
            coll = db.get_collection('users')
            query = coll.find_one({"_id": query['id_user']})
            nome = query['nome']

            coll = db.get_collection('local')
            query = coll.find_one({"_id": idLocal})

            temp = {
                'nome': nome,
                'data': date,
                'local': query['nome']
            }
            data.append(temp)

        res = {
            'data': data
        }

        return res
    else:
        coll = db.get_collection('apto')
        query = coll.find_one({"id_user": ObjectId(req['id'])})

        coll = db.get_collection('reserva')
        query = coll.find({"id_apto": query['_id'], 'status': 'aberto'})

        data = []
        for reserva in query:
            date = reserva['data']
            valor = reserva['valor']

            coll = db.get_collection('local')
            query = coll.find_one({"_id": reserva['id_local']})

            temp = {
                'local': query['nome'],
                'data': date,
                'valor': valor
            }
            data.append(temp)
        
        res = {
            'data': data
        }

        return res


@app.route('/addApto')
def addLocal():
    req = request.get_json()
    coll = db.get_collection('apto')

    apto = Apto(req['descricao'], req['numero'])

    data = {
        'numero': apto.getNumero(),
        'descricao': apto.getDescricao(),
        'token': apto.getToken()
    }
    coll.insert_one(data)
    
    return Response(status=200)


@app.route('/password')
def changePassword():
    req = request.get_json()
    coll = db.get_collection('users')
    query = coll.find_one({"_id": ObjectId(req['id']), "senha": req['password']})

    if query == None:
        return Response(status=401)

    coll.update_one({"_id": ObjectId(req['id'])}, {'$set': {"senha": req['newpassword']}})
    return Response(status=200)


@app.route('/options')
def configs():
    req = request.get_json()

    id = ObjectId("631a7e6387f49dacbfb5efd8")
    coll = db.get_collection('options')
    query = coll.find_one({"_id": id})

    if 'type' in req:
        query = coll.find_one({"_id": id})
        return {
            "cancel": query['dias_cancel'],
            "max": query['dias_max_reserva'],
            "min": query['dias_min_reserva']
        }

    if 'cancel' in req:
        coll.update_one({"_id": id}, {'$set': {"dias_cancel": req['cancel']}})
    if 'max' in req:
        coll.update_one({"_id": id}, {'$set': {"dias_max_reserva": req['max']}})
    if 'min' in req:
        coll.update_one({"_id": id}, {'$set': {"dias_min_reserva": req['min']}})

    return Response(status=200)


@app.route('/transfer')
def transferUser():
    req = request.get_json()
    coll = db.get_collection('apto')
    query = coll.find_one({"numero": req['numero']})

    return {"token": query['token']}



if __name__ == '__main__':
    if opc == 1:
        app.run(host="localhost", port=5000)
    elif opc == 2:
        app.run(host="0.0.0.0", port=3000)
    elif opc == 3:
        app.run()
    else:
        print("-> Invalid option.")