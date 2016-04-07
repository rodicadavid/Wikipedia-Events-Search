import os
import wiki_pages_update
from flask import Flask, jsonify, redirect, url_for, request, render_template, Response, json
import urllib
from pymongo import MongoClient
import time

app = Flask(__name__)


client = MongoClient(os.environ['WIKIEVENTS_DB_1_PORT_27017_TCP_ADDR'], 27017)
db = client.eventdb  
db.events_collection.create_index([("title", "text")])
db.events_collection.create_index([("day", 1 )])
db.events_collection.create_index([("year", 1 )])
db.events_collection.create_index([("category", 1 )])

@app.route('/')
def wiki_events():
    day = request.args['day'].replace("_", " ") if 'day' in request.args else ""
    year = request.args['year'] if 'year' in request.args else ""
    category = request.args['category'] if 'category' in request.args else ""
    keyword = request.args['keyword'] if 'keyword' in request.args else ""     
    query = {}
    if day != "":
        query["day"] = day.lower()
    if category != "":
        query["category"] = category.lower()
    if year != "":
        query["year"] = year.lower()        
    if keyword != "":    
        query["$text"] = { "$search" : keyword }
    _items = db.events_collection.find(query, { '_id' : 0 })
    items = [item for item in _items]
    data = {
        'results'  : items
    }
    js = json.dumps(data)
    return Response(js, status=200, mimetype='application/json')

if __name__ == "__main__":
    update = wiki_pages_update.UpdateWikipediaPagesData(db)
    update.start()
    app.run(host='0.0.0.0', debug = True)
