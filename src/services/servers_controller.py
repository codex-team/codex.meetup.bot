import logging
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
        logging.info(f"Setup password for instance with ip: {server_ip}")
        ssh_client = None
        for x in range(15):
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=server_ip, username="ubuntu", pkey=private_key)
                logging.info(f"Connected to instance with ip: {server_ip}")
                break
            except Exception as e:
                logging.info(f"Error while setup password (attempt {x})")
                logging.error(e)
                sleep(5)

        stdin, stdout, stderr = ssh_client.exec_command('sudo su')
        sleep(2)
        stdin.write('echo -e "' + password + '\n' + password + '" | passwd\n')
        sleep(2)
        stdin.write('echo "PasswordAuthentication yes" | sudo tee -a /etc/ssh/sshd_config\n')
        sleep(2)
        stdin.write('echo "PermitRootLogin yes" | sudo tee -a /etc/ssh/sshd_config\n')
        sleep(2)
        stdin.write('sudo service ssh restart')
        sleep(2)
        logging.info(f"Finished setting password for instance with ip: {server_ip}")

    def generate_password(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def create_server(self, user_id, server_name):
        logging.info(f'create {server_name}')
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
