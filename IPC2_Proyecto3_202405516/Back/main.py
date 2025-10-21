from flask import Flask 
from flask_cors import CORS
from controller.app_controller import app_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(app_bp)

if __name__ == '__main__':
	app.run(debug=True)