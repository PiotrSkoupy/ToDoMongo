from flask import Flask
import pymongo
import os
from flask import render_template, request, url_for,redirect
from bson.objectid import ObjectId




DATABASE_URL='mongodb+srv://Peteroko:123456789!@cluster0.dbdwm.mongodb.net/mydb?retryWrites=true&w=majority' # get connection url from environment

mongo=pymongo.MongoClient(DATABASE_URL) # establish connection with database
 # assign database to mongo_db

app = Flask(__name__)

@app.route('/')
def index():
    todos_collection = mongo.db.todos
    todos = todos_collection.find()
    return render_template('index.html', todos=todos)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    todos_collection = mongo.db.todos
    todo_item = request.form.get('add-todo')
    todos_collection.insert_one({'text': todo_item, 'complete': False})
    return redirect(url_for('main.index'))

@app.route('/complete_todo/<oid>')
def complete_todo(oid):
    todos_collection = mongo.db.todos
    todo_item = todos_collection.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    todos_collection.save(todo_item)
    return redirect(url_for('main.index'))

@app.route('/delete_completed')
def delete_completed():
    todos_collection = mongo.db.todos
    todos_collection.delete_many({'complete': True})
    return redirect(url_for('main.index'))

@app.route('/delete_all')
def delete_all():
    todos_collection = mongo.db.todos
    todos_collection.delete_many({})
    return redirect(url_for('main.index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9999))
    app.run(host='0.0.0.0/2', port=port)