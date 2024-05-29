import os.path
import time
from ftplib import FTP
import socket

from back_progress.utils.config import *


class FTPClient:
    def __init__(self, host, username, password, port=21, use_ipv6=False, timeout=10):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.use_ipv6 = use_ipv6
        self.timeout = timeout
        self.ftp = None
        self.directory = ftp_directory

    def connect(self):
        try:
            # 获取适当的地址信息
            addr_info = socket.getaddrinfo(self.host, self.port, socket.AF_INET6 if self.use_ipv6 else socket.AF_INET,
                                           socket.SOCK_STREAM)
            for res in addr_info:
                af, socktype, proto, canonname, sa = res
                try:
                    print(f"Trying to connect to {sa}")
                    self.sock = socket.socket(af, socktype, proto)
                    self.sock.settimeout(self.timeout)
                    self.sock.connect(sa)
                    self.ftp = FTP()
                    self.ftp.sock = self.sock
                    self.ftp.set_pasv(True)
                    self.ftp.connect(self.host, self.port)
                    print(f"Connected to {sa}")
                    break
                except Exception as e:
                    print(f"Connection attempt to {sa} failed: {e}")
                    if self.sock:
                        self.sock.close()
                    self.ftp = None
                    continue
            if self.ftp is None:
                raise Exception("Could not open socket")
            self.ftp.login(self.username, self.password)
            print(f"Logged in to {self.host}")

        except socket.gaierror as e:
            print(f"Error resolving host: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def disconnect(self):
        try:
            if self.ftp is not None:
                self.ftp.quit()
                print("Disconnected from the FTP server")
        except Exception as e:
            print(f"An error occurred during disconnect: {e}")

    def upload_file(self, local_file, timeStr):
        try:
            self.check_and_reconnect()

            self.create_folder(timeStr)
            directory = os.path.join(self.directory, timeStr)
            remote_file = os.path.basename(local_file)
            remote_file = str(time.time()) + "nas_time" + remote_file  # 防止重名
            with open(local_file, 'rb') as file:
                remote_file = remote_file.replace("\\", "/")
                self.ftp.storbinary(f'STOR {os.path.join(directory, remote_file)}', file)
            print(f"Uploaded {local_file} to {remote_file}")
            return remote_file
        except Exception as e:
            print(f"An error occurred during upload: {e}")
        return None

    def download_file(self, remote_file, local_file):
        try:
            with open(local_file, 'wb') as file:
                self.ftp.retrbinary(f'RETR {remote_file}', file.write)
            print(f"Downloaded {remote_file} to {local_file}")
        except Exception as e:
            print(f"An error occurred during download: {e}")

    def list_files(self, directory="."):
        try:
            files = self.ftp.nlst(directory)
            print(f"Files in {directory}:")
            for file in files:
                print(file)
            return files
        except Exception as e:
            print(f"An error occurred while listing files: {e}")

    def check_connection(self):
        try:
            self.ftp.voidcmd("NOOP")
            return True
        except Exception as e:
            print(f"An error occurred while checking connection: {e}")
        return False

    def reconnect(self):
        self.disconnect()
        self.connect()

    def check_and_reconnect(self):
        if not self.check_connection():
            self.reconnect()

    def check_file_exists(self, remote_file, directory):
        try:
            directory = os.path.join(self.directory, directory)
            files = self.ftp.nlst(directory)
            for file in files:
                if file.endswith(remote_file):
                    return True
            return False
        except Exception as e:
            print(f"An error occurred while listing files: {e}")
            return False

    def check_dir_exists(self, remote_dir):
        try:
            parent_dir = os.path.dirname(remote_dir)
            files = self.ftp.nlst(parent_dir)
            for file in files:
                if os.path.basename(file) == os.path.basename(remote_dir):
                    return True
            return False
        except Exception as e:
            print(f"An error occurred while listing files: {e}")
            return False

    def create_folder(self, timeStr):
        try:
            folder_path = os.path.join(self.directory, timeStr)
            # 检查文件夹是否存在
            if not self.check_dir_exists(folder_path):
                # 创建文件夹
                timeStrs = timeStr.split("/")
                timeStrs = [path for path in timeStrs if path != ""]
                print(timeStrs)
                for i in range(1, len(timeStrs) + 1):
                    dirPath = "/".join(timeStrs[:i])
                    dirPath = os.path.join(self.directory, dirPath)
                    print("check  folder  " + dirPath)
                    if not self.check_dir_exists(dirPath):
                        print(f"Creating folder {dirPath}")
                        self.ftp.mkd(dirPath)
                print(f"Folder {folder_path} created.")
            else:
                print(f"Folder {folder_path} already exists.")
        except Exception as e:
            print(f"An error occurred while creating folder {folder_path}: {e}")

    def delete_file(self, file_path, directory):
        try:
            self.check_file_exists(file_path, directory)
            self.ftp.delete(os.path.join(self.directory, file_path))
            print(f"File {file_path} deleted.")
        except Exception as e:
            print(f"An error occurred while deleting file {file_path}: {e}")


def get_def_ftp_client():
    ftp_client = FTPClient(ftp_host, ftp_user, ftp_pws, use_ipv6=False)
    return ftp_client


# 使用示例
if __name__ == "__main__":
    pass
