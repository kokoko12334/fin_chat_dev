from sshtunnel import SSHTunnelForwarder
from settings import *
import os

class SSHConnection:
    def __init__(self):
        self.ssh_host : str = settings.SSH_HOST
        self.ssh_port : int = settings.SSH_PORT
        self.ssh_user : str = settings.SSH_USER
        self.ssh_password: str = settings.SSH_PASSWORD
        self.remote_host = settings.DATABASE_HOST
        self.remote_port = settings.DATABASE_PORT
        self.tunnel = None
        
    def connect(self):
        self.tunnel = SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_user,
            ssh_password=self.ssh_password,
            remote_bind_address=(self.remote_host, self.remote_port)
        )
        self.tunnel.start()

    def disconnect(self):
        if self.tunnel:
            self.tunnel.stop()
            
ssh = SSHConnection()