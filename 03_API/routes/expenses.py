from flask import Flask, request, Response, Blueprint
import sqlite3
import json
from datetime import date

#define blueprint
expenses_bp = Blueprint("expenses", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"
