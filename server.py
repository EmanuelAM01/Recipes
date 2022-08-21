from flask_app import app

#Importando Controlador
from flask_app.controllers import users
from flask_app.controllers import recipes
#Pasos a seguir:
#pipenv install flask pymysql
#pipenv shell
#python server.py -> python3, py o python

if __name__=="__main__":
    app.run(debug=True)