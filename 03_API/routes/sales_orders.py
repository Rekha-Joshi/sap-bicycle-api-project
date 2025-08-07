from flask import Flask, jsonify, request, Response, Blueprint
import sqlite3
import json

#defining blueprint
sales_order_bp = Blueprint("sales_order", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"