from flask import Flask, jsonify, request

app = Flask(__name__) #create the app

@app.route("/") # this function runs when we run this program
def home():
    return("Hello API")

if __name__ == "__main__":
    app.run(debug=True)