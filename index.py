import redis
import sys
import json
import os
from flask import Flask, render_template, request, jsonify

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
REDIS_PORT = os.environ['REDIS_PORT']

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/add")
def add():
	try:
		item = request.get_json()
		r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
		r.rpush('items', json.dumps(item))	
		return jsonify({"error": 0, "result": "OK"})
	except Exception as e:	
		if hasattr(e, 'message'):
			print("Error  inesperado: " + e.message)
			return jsonify({"error": 1, "result": "Unexpected error: " + e.message}), 500
		else:
			print("Error inesperado: " + e)
			return jsonify({"error": 1, "result": "Unexpected error: " + e}), 500

@app.route("/addall")
def addAll():
	try:
		items = request.get_json()					
		
		r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
		for item in items:
			r.rpush('items', json.dumps(item))				
		
		return jsonify({"error": 0, "result": "OK"})
	except Exception as e:	
		if hasattr(e, 'message'):
			print("Error  inesperado: " + e.message)
			return jsonify({"error": 1, "result": "Unexpected error: " + e.message}), 500
		else:
			print("Error inesperado: " + e)
			return jsonify({"error": 1, "result": "Unexpected error: " + e}), 500

@app.route("/items")
def items():
	try:		
		r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
		items = r.lrange('items', 0, -1)
		itemsJson = []
		for item in items:
			itemsJson.append(json.loads(item))
		return jsonify(itemsJson)
	except Exception as e:	
		if hasattr(e, 'message'):
			print("Error  inesperado: " + e.message)
			return jsonify({"error": 1, "result": "Unexpected error: " + e.message}), 500
		else:
			print("Error inesperado: " + e)
			return jsonify({"error": 1, "result": "Unexpected error: " + e}), 500


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
