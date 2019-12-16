import os
from flask import Flask, request, render_template
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'first_database'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)


@app.route('/')
def home_page():
    return "Home page"


@app.route('/create')
def create():

    document = {"name": "Kevin",
                "nb_of_movies": "20"}

    mongo.db.actors.insert_one(document)

    return "A record has been created"



@app.route('/read')
def read():

    actors = mongo.db.actors.find()

    return render_template('read.html', actors=actors)


@app.route('/update')
def update():

    query = {'name': 'Leonardo'}

    actor_to_update = mongo.db.actors.find_one(query)

    id_ = actor_to_update["_id"]
    what_doc = {'_id': ObjectId(id_)}

    doc_content = {'name': "Leonardo",
                   'number_of_movies': "456"}

    mongo.db.actors.update(what_doc, doc_content)

    return render_template('index.html')


@app.route('/delete')
def delete():
    query = {'name': 'Kevin'}

    actor_to_update = mongo.db.actors.find_one(query)

    id_ = actor_to_update["_id"]

    mongo.db.actors.remove({'_id': ObjectId(id_)})
    return "A record has been deleted"


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5000')),
            debug=True)
