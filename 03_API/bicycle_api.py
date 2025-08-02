import sys
import os
#this tells python to look at the parent folder of this file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from routes import customers_bp, vendors_bp

app = Flask(__name__) #create the app
app.register_blueprint(customers_bp)
app.register_blueprint(vendors_bp)

#Default route
@app.route("/") # this function runs when we run this program
def home():
    return("Hello API")


if __name__ == "__main__":
    app.run(debug=True)