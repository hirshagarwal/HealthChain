import uuid

import requests as requests
from requests import Response

from blockchain import Block
from clienthelper import ClientHelper
from user import User


class HealthChainClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.helper = ClientHelper(host, port)

    def add_block(self, new_block: Block):
        request_response = requests.post("http://{}:{}/add_block".format(self.host, self.port),
                                 data=new_block.get_json())
        return request_response.json()

    def get_blockchain(self) -> Response:
        return requests.get("http://{}:{}/get_blockchain"
                            .format(self.host, self.port)).json()


if __name__ == '__main__':
    client = HealthChainClient('localhost', '8080')
    user = User(uuid.uuid4())
    block = client.helper.build_user_block('Hirsh', 'Agarwal', '16/08/1997', user)
    response = client.add_block(block)
    print(response)
    # decrypted_block = UserData.decrypt_user_data_block(block.data, user.private_key)
    # print(client.get_blockchain())
