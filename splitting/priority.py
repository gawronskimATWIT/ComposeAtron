from pymongo import MongoClient
import os

def updateDoc(collection):
    collection.update_many(
        {},
        {"$set": {"priority": True}}
        ) 

test = os.getcwd() + "\\splitting\\important.txt"
with open(test, "r") as file:
    artistNames = [line.strip() for line in file.readlines()]

client = MongoClient("mongodb://root:rootpassword@76.152.217.55:27017/")
db = client["Songs"]


for artist in artistNames:
    artistName = artist.strip()
    collection = db[artistName]
    updateDoc(collection)
    print(f"priority added: {artistName}")

client.close()