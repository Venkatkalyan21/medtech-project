from pymongo import MongoClient

MONGO_URI = "mongodb+srv://rahulrrk2807_db_user:axnU93xoK3bkFCnm@medtech.8rnmzbj.mongodb.net/?appName=medtech"

client = MongoClient(MONGO_URI)

db = client["medtech_db"]

reports_collection = db["reports"]
