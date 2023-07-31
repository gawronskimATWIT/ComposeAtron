import paramiko
import os
from sftp import getClient
import time


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



def sendFile(path, sftpClient):
     with sftpClient.open_sftp() as sftp:
        # Split the remote file name into artist name and file name
        remote_file_name = path.split('/')[-1]
        encoded_artist_name, file_name = remote_file_name.split('_', 1)
        file_name = file_name.split('_', 1)[-1]
        # Decode the artist's name by replacing underscores with spaces
        artist_name = encoded_artist_name.replace('_', ' ')
        
        # Construct the local path using the artist's name
        remotePath = f"/songs/{artist_name}/{file_name}"
        
        # Get the file from the remote server
        sftp.put(path, remotePath)


if __name__ == '__main__' :
    sftpClient = getClient()
    
    sftpClient.connect("76.152.217.55", username="user",password="H@ppykid60")
    
    stemTypes = ['bass', 'drums', 'instrum', 'instrum2', 'other', 'vocals']
    directory = '/upload/'

    while True:
        
        wav_files = get_unprocessed_files(directory, stemTypes)

        if not wav_files:
            print("No unprocessed files found. Waiting...")
            time.sleep(10)  # Wait for 10 seconds before checking again
            continue

        for wav_file in wav_files:
            file_path = os.path.join(directory, wav_file)
            success = processFile(file_path)

            if success:
                print(f"Successfully processed {file_path}")

                sendFile(file_path, sftpClient)


                
            else:
                print(f"Failed to process {file_path}")

        time.sleep(20)


    
    
    


