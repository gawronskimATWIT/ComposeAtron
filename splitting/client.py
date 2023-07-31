import paramiko
import os
from sftp import getClient

def recieveFile(id,sftp,remotePath):
    with sftp.open_sftp() as sftp:
        localPath = f"./recieved/{id}.wav"
        sftp.get(remotePath,localPath)

def processFile(id):
    os.system(f'python inference.py --input_audio {id}.wav --output_folder ./results/')


def sendFile(id):


if __name__ == '__main__' :
    sftpClient = getClient()

    
    recieveFile()
    processFile()
    sendFile()