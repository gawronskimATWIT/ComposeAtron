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
    key = paramiko.RSAKey(filename="/home/user/vastKey.pem")
    sftpClient.connect("192.168.1.8", username="foo",password="pass")

    collections = db.list_collection_names()

    for collection in collections:

        documents = db[collection].find({"priority": {"$exists": "true"}})

        if len(list(documents.clone())) == 0:
            continue


        for doc in documents:

            try:
                if isNone(doc['wavPath']):
                    continue
            except KeyError:
                    continue


            sendFile(doc['wavPath'],sftpClient)
            
            fileName = doc['wavPath'].split('/')[-1]

            waitForFiles(fileName,sftpClient)

    #        recieveFile(doc['_id'],sftpClient)




def sendFile(path,sftpClient):
    with sftpClient.open_sftp() as sftp:
        artist_name = path.split('/')[-2]  # Get the artist's name
        file_name = path.split('/')[-1]    # Get the file name
        encoded_artist_name = artist_name.replace(' ', '_') # Replace spaces with underscores
        remote_file_name = f"{encoded_artist_name}_{file_name}"
        remoteFilePath = "/upload/" + remote_file_name
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