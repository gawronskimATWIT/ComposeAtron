import paramiko
from pymongo import MongoClient
from sftp import getClient
import time


def isNone(path):
     return path.split('/')[-1] == 'None'

def processAudioFiles():
    #connect to DB
    client = MongoClient("mongodb://root:rootpassword@76.152.217.55:27017/")
    db = client["Songs"]
    #connect to remote server
    sftpClient = getClient()
    sftpClient.connect("76.152.217.55", username="user",password="H@ppykid60")

    collections = db.list_collection_names()

    for collection in collections:

        documents = db[collection].find({"priority": {"$exists": "true"}})

        if len(list(documents.clone())) == 0:
            continue


        for doc in documents:

            if isNone(doc['wavPath']):
                continue

            sendFile(doc['wavPath'],sftpClient)
            
            fileName = doc['wavPath'].split('/')[-1]

            waitForFiles(fileName,sftpClient)

    #        recieveFile(doc['_id'],sftpClient)




def sendFile(path,sftpClient):

    with sftpClient.open_sftp() as sftp:
        remoteFilePath = "/songs/" + path.split('/')[-1]
        sftp.put(path, remoteFilePath)

#def processFile(id):



#def recieveFile(id): 

def waitForFiles(fileName, sftp, timeout=10000):
    startTime = time.time()
    stemTypes = ['bass', 'drums', 'instrum', 'instrum2', 'other', 'vocals']

    for stem in stemTypes:
        remotePath = f"{fileName}_{stem}.wav"
        fileReceived = False

        while time.time() - startTime < timeout and not fileReceived:
            try:
                sftp.stat(remotePath)
                fileReceived = True
                print(f"Recieved : {remotePath}")
            except FileNotFoundError:
                time.sleep(5)
        if not fileReceived:
            print(f"Timed out waiting for: {remotePath}")
            return False
        
    return True




if __name__ == '__main__':
    processAudioFiles()