import json
import sys
import uuid

import requests
from bottle import Bottle, request, response

from blockchain import Chain, Block


class Node(Bottle):
    def __init__(self, host, port, entry_node=None):
        super(Node, self).__init__()
        self.node_id = uuid.uuid4()
        self.nodes = set()
        self.host = host
        self.port = port
        self.name = "Node"
        self.blockchain = Chain()

        # API Paths
        self.get('/test', callback=self.test)
        self.get('/list_nodes', callback=self.list_nodes)
        self.get('/get_blockchain', callback=self.get_blockchain)
        self.get('/get_tail_block', callback=self.get_tail_block)

        self.post('/register_node', callback=self.register_node)
        self.post('/add_block', callback=self.add_block)

        if entry_node is not None:
            print("Registering node to: {}".format(entry_node))
            register_node_response = requests.post("http://{}/register_node".format(entry_node),
                                                   data=self.node_connection_string()
                                                   )
            self.nodes.add(json.dumps(register_node_response.json()))
            target_blockchain = requests.get("http://{}:{}/get_blockchain".format(
                entry_node.split(':')[0], entry_node.split(':')[1]
            )).json()
            self.build_from_target(target_blockchain)

        self.nodes.add(self.node_connection_string())
        print("Nodes: ")
        for _node in self.nodes:
            print(_node)

        self.run()

    def build_from_target(self, target_json):
        self.blockchain.blockchain = []
        chain = target_json['blockchain']
        for _block in chain:
            block = Block.from_json(_block)
            self.blockchain.blockchain.append(block)

    def node_connection_string(self):
        connection_dict = {
            'node_id': str(self.node_id),
            'host': self.host,
            'port': self.port}
        return json.dumps(connection_dict)

    def run(self, **kwargs):
        super().run(host=self.host, port=self.port, debug=True)

    def list_nodes(self):
        node_list = []
        for node_item in self.nodes:
            node_item_json = json.loads(node_item)
            node_list.append({
                'node_id': str(node_item_json['node_id']),
                'host': node_item_json['host'],
                'port': node_item_json['port']
            })
        return json.dumps(node_list)

    def register_node(self):
        new_node_string = request.body.read().decode('utf-8')
        new_node_object = json.loads(new_node_string)
        for _node in self.nodes:
            _node_object = json.loads(_node)
            if (_node_object['host'] == new_node_object['host']
                    and _node_object['port'] == new_node_object['port']):
                self.nodes.discard(_node)
                break

        self.nodes.add(new_node_string)
        print("New node registered: {} \nCurrent node list: ".format(new_node_string))
        for _node in self.nodes:
            if _node == self.node_connection_string():
                print("(SELF)" + _node)
                continue
            print(_node)
        return self.node_connection_string()

    def get_blockchain(self):
        response.content_type = 'application/json'
        json_chain = self.blockchain.get_json()
        object_chain = {
            "blockchain_length": len(self.blockchain.blockchain),
            "blockchain": json.loads(json_chain)
        }
        return json.dumps(object_chain)

    def get_tail_block(self):
        response.content_type = 'application/json'
        return self.blockchain.read_tail_block().get_json()

    def add_block(self):
        response.content_type = 'application/json'
        add_block_string = request.body.read()
        add_block_json = json.loads(add_block_string)
        insert_block = Block.from_json(add_block_json)

        # Make sure our chain is up to date
        for node in self.nodes:
            if node == self.node_connection_string():
                continue
            node_dict = json.loads(node)
            tail_block = requests.get("http://{}:{}/get_tail_block"
                                      .format(node_dict['host'], node_dict['port'])).json()
            if tail_block['hash'] == self.get_tail_block()['hash']:
                print("Current chain up to date. Proceed to add block")
                pass

        self.blockchain.add_block(insert_block)
        return json.dumps(insert_block.get_dict())

    def test(self):
        return_message = request.headers.get('message')
        return "{} - {}\n{}:{}".format(self.node_id,
                                       return_message,
                                       self.host,
                                       self.port)


if __name__ == '__main__':
    _host = "localhost"
    _port = "8080"
    _target = None
    try:
        _host = str(sys.argv[1])
        _port = str(sys.argv[2])
        _target = str(sys.argv[3])
    except IndexError as ex:
        print("No target supplied: {}".format(ex))
    if _target is not None:
        print("Running on {}:{} targeting {}".format(
            _host,
            _port,
            _target
        ))
        node = Node(_host, _port, _target)
    else:
        print("Running on {}:{}".format(
            _host,
            _port
        ))
        node = Node(_host, _port)


