from pymongo import ASCENDING
from flask import Flask, Response, request
from flask_cors import CORS
from bson.objectid import ObjectId
from datetime import datetime
from utils import dbConnection, sendEmail, dayDiff
from users import User
from apto import Apto
from local import Local

db = dbConnection("", "")
app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return {"Name": "Condominium API", "Status": "OK", "Author": "Nathan Nunes"}

# rota de login
@app.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    coll = db.get_collection('users')
    query = coll.find_one({'email': req['email']})

    # caso o email não exista retorna erro
    if query == None:
        return Response(status=403)

    # verifica se a senha recebida é a mesma da presente no BD
    if query['senha'] == req['senha']:
        # verifica as reservas que já passaram da data atual e altera o status para fechado
        coll = db.get_collection('reserva')
        data = coll.find({'status': 'aberto'})

        now = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        for reserva in data:
            if (reserva['data'] - now).days <= 0:
                coll.update_one({"_id": reserva['_id']}, {'$set': {'status': 'fechado'}})

        # retorna o json para usuário administrador ou não
        if query['permissao'] == True:
            return {'id': str(query['_id']), 'permissao': query['permissao']}
        else:
            return {'id': str(query['_id']), 'permissao': query['permissao'], 'nome': query['nome']}
    else:
        return Response(status=401)
    

# cadastro de usuário
@app.route('/register', methods=['POST'])
def register():
    req = request.get_json()

    # verifica se o email a ser cadastrado já existe no banco
    coll = db.get_collection('users')
    query = coll.find_one({'email': req['email']})
    if query != None:
        return Response(status=401)

    # faz uma query em busca do token fornecido pelo usuário
    coll = db.get_collection('apto')
    query = coll.find_one({'token': req['token']})

    # verifica se o token pertence a algum apartamento
    if query == None:
        return Response(status=401)

    # verifica se algum usuário já pertence ao apartamento
    if 'id_user' in query:
        apto = Apto(query['descricao'], query['numero'], str(query['_id']), str(query['id_user']))
        user = User(req['email'], req['senha'], req['nome'], req['telefone'], False)

        # substitui os dados do usuário existente pelo dados fornecidos
        coll = db.get_collection('users')
        coll.update_one({"_id": query['id_user']}, {'$set': {
            "email": user.getEmail(),
            "senha": user.getSenha(),
            "nome": user.getNome(),
            "telefone": user.getTelefone(),
            "permissao": user.getPermissao()
        }})

    # caso n exista nenhum usuário linkado com o apto esse user será criado no banco e linkado com o apto
    else:
        user = User(req['email'], req['senha'], req['nome'], req['telefone'], False)
        data = {
            "email": user.getEmail(),
            "senha": user.getSenha(),
            "nome": user.getNome(),
            "telefone": user.getTelefone(),
            "permissao": user.getPermissao()
        }

        # insere o novo usuário na tabela de users
        coll = db.get_collection('users')
        coll.insert_one(data)
        query = coll.find_one({'email': user.getEmail()})

        # linka o apto com o novo usuário
        coll = db.get_collection('apto')
        coll.update_one({"token": req['token']}, {'$set': {'id_user': query['_id']}})

        # cria um objeto apto para poder acessar a geração de token
        query = coll.find_one({'token': req['token']})
        apto = Apto(query['descricao'], query['numero'], str(query['_id']), str(query['id_user']))

    # gera um novo token para o apto
    coll = db.get_collection('apto')
    coll.update_one({"token": req['token']}, {'$set': {'token': apto.getToken()}})
    
    return Response(status=200)


# redefinir senha
@app.route('/resetpassword', methods=['POST'])
def resetPassword():
    req = request.get_json()

    # verifica se a requisição deve retornar o token ou editar a senha
    if 'email' in req:
        coll = db.get_collection('users')
        query = coll.find_one({'email': req['email']})

        # se o email estiver cadastrado no banco faz o envio do token
        if query != None:
            coll = db.get_collection('apto')
            query = coll.find_one({'id_user': query['_id']})
            sendEmail(req['email'], query['token'])
        return Response(status=200)

    # busca o token no banco
    coll = db.get_collection('apto')
    query = coll.find_one({'token': req['token']})

    # verifica se o token foi encontrado
    if query == None:
        return Response(status=401)
    
    # altera a senha
    coll = db.get_collection('users')
    coll.update_one({'_id': query['id_user']}, {'$set': {'senha': req['senha']}})
    return Response(status=200)


# retorna dados para painel de informações
@app.route('/infos', methods=['POST'])
def infos():
    req = request.get_json()
    coll = db.get_collection('users')
    query = coll.find_one({'_id': ObjectId(req['id'])})

    # verifica se o id do usuário é válido
    if query == None:
        return Response(status=401)
    # continua a execução se o usuário for administrador
    if query['permissao'] != True:
        return {"permissao": query['permissao']}

    reservas = 0
    cancelamentos = 0
    ganhos = 0
    locados = 0
    locadosAno = 0

    coll = db.get_collection('reserva')
    year = datetime.now().year
    month = datetime.now().month
    start = datetime(year, month, 1)
    end = datetime(year, month, dayDiff(year, month))

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

    start = datetime(year, 1, 1)
    end = datetime(year, 12, dayDiff(year, 12))
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
@app.route('/calendar', methods=['GET'])
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
    return {'data': data}


# busca informações de uma reserva
@app.route('/searchcalendar', methods=['POST'])
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


# retorna últimos 5 aluguéis
@app.route('/recent', methods=['POST'])
def recent():
    req = request.get_json()
    coll = db.get_collection('users')
    query = coll.find_one({"_id": ObjectId(req['id'])})

    # verifica qual a permissão do usuário para retornar o devido json
    cont = 0
    if query['permissao'] == True:
        # caso o usuário seja administrador retorna as últimas 5 reservas considerando todos os usuários
        coll = db.get_collection('reserva')
        query = coll.find({'status': 'aberto'}).sort('data', ASCENDING)

        data = []
        for reserva in query:
            cont = cont + 1
            if cont > 5:
                break

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
                'data': date.strftime("%d/%m/%Y"),
                'local': query['nome']
            }
            data.append(temp)

        return {'data': data, 'permissao': True}
    else:
        # caso não seja administrador retorna as últimas 5 reservas do usuários que enviou a requisição
        coll = db.get_collection('apto')
        query = coll.find_one({"id_user": ObjectId(req['id'])})

        coll = db.get_collection('reserva')
        query = coll.find({"id_apto": query['_id'], 'status': 'aberto'}).sort('data', ASCENDING)

        data = []
        for reserva in query:
            cont = cont + 1
            if cont > 5:
                break
            date = reserva['data']
            valor = reserva['valor']

            coll = db.get_collection('local')
            query = coll.find_one({"_id": reserva['id_local']})

            temp = {
                'local': query['nome'],
                'data': date.strftime("%d/%m/%Y"),
                'valor': valor
            }
            data.append(temp)
        
        return {'data': data, 'permissao': False}


# gerencia os apartamentos
@app.route('/apto', methods=['POST'])
def addApto():
    req = request.get_json()
    coll = db.get_collection('apto')

    # deleta um apartamento
    if 'type' in req:
        if coll.find_one({'numero': req['numero']}) == None:
            return Response(status=404)
        coll.delete_one({'numero': req['numero']})
        return Response(status=200)

    # verifica se o apartamento já existe
    if coll.find_one({'numero': req['numero']}) != None:
        return Response(status=409)

    # cria um objeto e inseri o novo apartamento no banco
    apto = Apto(req['descricao'], req['numero'])
    data = {
        'numero': apto.getNumero(),
        'descricao': apto.getDescricao(),
        'token': apto.getToken()
    }
    coll.insert_one(data)
    
    return Response(status=200)


# troca de senha a partir do painel
@app.route('/password', methods=['POST'])
def changePassword():
    req = request.get_json()
    coll = db.get_collection('users')
    query = coll.find_one({"_id": ObjectId(req['id']), "senha": req['password']})

    # verifica se o id é válido
    if query == None:
        return Response(status=401)

    # altera a senha para a nova senha recebida
    coll.update_one({"_id": ObjectId(req['id'])}, {'$set': {"senha": req['newpassword']}})
    return Response(status=200)


# gerencia as configurações de sistema
@app.route('/options', methods=['POST'])
def configs():
    req = request.get_json()

    id = ObjectId("631a7e6387f49dacbfb5efd8")
    coll = db.get_collection('options')
    query = coll.find_one({"_id": id})

    # busca as informações no banco e retorna o json
    if 'type' in req:
        query = coll.find_one({"_id": id})
        return {
            "cancel": query['dias_cancel'],
            "max": query['dias_max_reserva'],
            "min": query['dias_min_reserva']
        }

    # altera os campos de acordo com os campos recebidos na requisição
    if 'cancel' in req:
        coll.update_one({"_id": id}, {'$set': {"dias_cancel": req['cancel']}})
    if 'max' in req:
        coll.update_one({"_id": id}, {'$set': {"dias_max_reserva": req['max']}})
    if 'min' in req:
        coll.update_one({"_id": id}, {'$set': {"dias_min_reserva": req['min']}})

    return Response(status=200)


# gerencia as informações dos locais
@app.route('/local', methods=['POST'])
def local():
    req = request.get_json()
    coll = db.get_collection('local')

    # retorna todos os lugares existentes
    if req['type'] == "get":
        query = coll.find()

        data = []
        for local in query:
            temp = {
                'nome': local['nome'],
                'valor': local['valor']
            }
            data.append(temp)
        return {'data': data}

    # deleta um local
    if req['type'] == "delete":
        coll.delete_one({'nome': req['nome']})
        return Response(status=200)

    local = Local(req['nome'], req['valor'])

    # edita o valor do aluguel de um local
    if req['type'] == "edit":
        coll.update_one({'nome': local.getNome()}, {'$set': {'valor': local.getValor()}})
        return Response(status=200)

    # cria um novo local
    coll.insert_one({'nome': local.getNome(), 'valor': local.getValor()})
    return Response(status=200)


# retorna o token presente no banco
@app.route('/transfer', methods=['POST'])
def transferUser():
    coll = db.get_collection('apto')
    query = coll.find()

    data = []
    for i in query:
        data.append({
            "apto": i['descricao'],
            "token": i['token']
        })
    return {"data": data}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
    #app.run()