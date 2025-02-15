from flask import jsonify
from app import app

@app.route("/")
def home():
    infos = [
        {"Nome": "Marcelo Henrique Colombo",
         "E-mail": "marcelo.h.colombo@gmail.com",
         "Linkedin": "https://www.linkedin.com/in/marcelo-colombo-65766a82/" 
    }]
    return jsonify(infos)