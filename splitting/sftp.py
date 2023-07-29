import paramiko

def getClient():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    client.connect("76.152.217.55", username="user",password="H@ppykid60")

    return client