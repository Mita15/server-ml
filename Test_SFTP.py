import paramiko


host = '34.125.139.205'
port = 22
user = 'sftp_tvx'
password = '<L8m\hEg'
transport = paramiko.Transport((host, port))
transport.connect(username = user, password = password)

sftp = paramiko.SFTPClient.from_transport(transport)

import sys
path = '/var/www/tvextract-skripsi/uploads/tmp/41-61b1b4adda1f7.pdf'    #hard-coded
localpath = '/var/html/server-ml/samples/41-61b1b4adda1f7.pdf'
sftp.put(localpath, path)

sftp.close()
transport.close()
print ('Upload done.')