import os
import random
import string
from time import sleep

from src.services.database import database
from src.services.yandex_cloud import create_instance, delete_instance
import paramiko

script_dir = os.path.dirname(__file__)
rel_path = "../../keys/key"
abs_file_path = os.path.join(script_dir, rel_path)

private_key = paramiko.RSAKey.from_private_key_file(abs_file_path)


class ServerController:
    def __enable_password_auth(self, server_ip, password):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for x in range(5):
            try:
                ssh_client.connect(hostname=server_ip, username="ubuntu", pkey=private_key)
                break
            except Exception as e:
                print(e)
                sleep(5)

        stdin, stdout, stderr = ssh_client.exec_command('sudo su')
        stdin.write('echo -e "' + password + '\n' + password + '" | passwd\n')
        stdin.write('echo "PasswordAuthentication yes" | sudo tee -a /etc/ssh/sshd_config\n')
        stdin.write('echo "PermitRootLogin yes" | sudo tee -a /etc/ssh/sshd_config\n')
        stdin.write('sudo service ssh restart')

    def generate_password(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def create_server(self, user_id, server_name):
        print(f'create {server_name}')
        server_data = create_instance(server_name)
        ip_address = server_data['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']

        password = self.generate_password(8)

        self.__enable_password_auth(ip_address, password)
        server_data['userId'] = user_id
        server_data['password'] = password
        database.servers.insert_one(server_data)

        return server_data

    def delete_server_by_id(self, server_id):
        try:
            delete_instance(server_id)
        except Exception:
            pass
        finally:
            database.servers.remove({'id': server_id})

    def delete_server_by_user_id(self, user_id):
        server = database.servers.find_one({'userId': user_id})

        try:
            delete_instance(server['id'])
        except Exception:
            pass
        finally:
            database.servers.remove({'id': server['id']})


servers_controller = ServerController()
