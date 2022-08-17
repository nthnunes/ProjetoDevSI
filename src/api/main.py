from flask import Flask, jsonify, request

opc = int(input("Run app:\n1 - Local\n2 - In my network\n3 - TCP Tunnel\nOption: "))

app = Flask(__name__)
if opc == 3:
    from flask_ngrok import run_with_ngrok
    run_with_ngrok(app)

@app.route('/')
def homepage():
    return jsonify({"Name": "Condominium API", "Status": "OK", "Author": "Nathan Nunes"})

@app.route('/register', methods=['GET', 'POST'])
def register():
    return request.json


if __name__ == '__main__':
    if opc == 1:
        app.run(host="localhost", port=5000)
    elif opc == 2:
        app.run(host="0.0.0.0", port=3000)
    elif opc == 3:
        app.run()
    else:
        print("-> Invalid option.")