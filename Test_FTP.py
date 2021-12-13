from ftplib import FTP

host = '34.125.139.205'
user = 'sftp_tvx'
password = '<L8m\hEg'

def jalanin_ini():
    with FTP(host) as ftp:
        ftp.login(user=user, passwd=password)
        print('Login success')
        ftp.cwd('/var/www/tvextract-skripsi/uploads/tmp/')
        print('Change directory success')
        file_name = '41-61b1b4adda1f7.pdf'
        filepath = open('/var/html/server-ml/samples/41-61b1b4adda1f7.pdf', 'rb')
        print('Opening File')
        ftp.storbinary('STOR ' + file_name   , filepath)
        print('Transfer is successful')
        ftp.quit()

jalanin_ini()