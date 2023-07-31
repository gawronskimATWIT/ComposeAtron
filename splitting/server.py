import paramiko
from pymongo import MongoClient
from sftp import getClient


def isNone(path):
     return path.split('/')[-1] == 'None'

def processAudioFiles():
    #connect to DB
    client = MongoClient("mongodb://root:rootpassword@76.152.217.55:27017/")
    db = client["Songs"]
    #connect to remote server
    sftpClient = getClient()

    collections = db.list_collection_names()

    for collection in collections:

        documents = db[collection].find({"priority": {"$exists": "true"}})

        if len(list(documents.clone())) == 0:
            continue


        for doc in documents:

            if isNone(doc['wavPath']):
                continue

            sendFile(doc['wavPath'],sftpClient)

          #   processFile(doc['_id'])

    #        recieveFile(doc['_id'],sftpClient)




def sendFile(path,sftpClient):

    with sftpClient.open_sftp() as sftp:
        remoteFilePath = "/songs/" + path.split('/')[-1]
        sftp.put(path, remoteFilePath)

# def processFile(id):



#def recieveFile(id): 




if __name__ == '__main__':
    processAudioFiles()