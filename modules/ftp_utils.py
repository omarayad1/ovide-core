import os
from ftplib import FTP
import ftplib


def download_file_to_tmp(filename):
    host = os.environ["FTP_HOST"]
    username = os.environ["FTP_USERNAME"]
    password = os.environ["FTP_PASSWORD"]
    ftp = FTP(host, username, password)
    ftp.cwd("ovide-static")
    ftp.retrbinary("RETR %s" % filename, open('./tmp/%s' % filename, 'wb').write)
    ftp.close()


def upload_file_from_tmp(filename):
    host = os.environ["FTP_HOST"]
    username = os.environ["FTP_USERNAME"]
    password = os.environ["FTP_PASSWORD"]
    ftp = FTP(host, username, password)
    ftp.cwd("ovide-static")
    ftp.storlines("STOR %s" % filename, open('./tmp/%s' % filename, 'r'))
    ftp.close()