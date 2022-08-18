def dbConnection(username, password):
    from pymongo import MongoClient

    CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@cluster0.bbxnito.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    return client

username = input("$ MongoDB Connection\nUsername: ")
password = input("Password: ")

client = dbConnection(username, password)

print(client.list_database_names())

db = client.get_database('')
col = db.get_collection('')