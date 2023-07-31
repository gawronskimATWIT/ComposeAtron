import paramiko
import os
from sftp import getClient

def recieveFile(id,sftp,remotePath):
    with sftp.open_sftp() as sftp:
        localPath = f"./recieved/{id}.wav"
        sftp.get(remotePath,localPath)

def processFile(filePath):
  try:
    # Code to process the file goes here
    print(f"Processing {filePath}")
    home = os.getcwd() + "/MVSEP-MDX23-music-separation-model"
    os.chdir(home)


    os.system(f'python inference.py --input_audio {filePath}.wav --output_folder /upload')



    return True  # Return True if processing is successful
  except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")
            return False  # Return False if an error occurs  






def get_unprocessed_files(directory, stemTypes):
    files = os.listdir(directory)
    return [f for f in files if f.endswith('.wav') and not any(f.endswith(f'_{stem}.wav') for stem in stemTypes)]



def sendFile(id):


if __name__ == '__main__' :
    sftpClient = getClient()
    
    sftpClient.connect("76.152.217.55", username="user",password="H@ppykid60")
    
    stemTypes = ['bass', 'drums', 'instrum', 'instrum2', 'other', 'vocals']
    directory = '/upload/'

    while True:
        wav_files = get_unprocessed_files(directory, stemTypes)
       

        for wav_file in wav_files:
            file_path = os.path.join(directory, wav_file)
            success = processFile(file_path)

            if success:
                print(f"Successfully processed {file_path}")

                sendFile(ith sftp.open_sftp() as sftp:
            localPath = f"./recieved/{id}.wav"
        sftp.get(remotePath,localPath)
)


                
            else:
                print(f"Failed to process {file_path}")

        import time
        time.sleep(20)


    
    
    


