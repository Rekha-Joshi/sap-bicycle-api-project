from flask import Flask, jsonify, request, Response, Blueprint
import sqlite3
import json

#defining blueprint
production_orders_bp = Blueprint("production_orders", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

