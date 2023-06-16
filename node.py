import json
import uuid

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
            # Send request with node connection string to the entry node
            pass

        self.nodes.add(self.node_connection_string())

        self.run()

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
        new_node_string = request.body.read()
        self.nodes.add(new_node_string)
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
        self.blockchain.add_block(insert_block)
        return json.dumps(insert_block.get_dict())

    def consensus(self):
        pass

    def test(self):
        return_message = request.headers.get('message')
        return "{} - {}\n{}:{}".format(self.node_id,
                                       return_message,
                                       self.host,
                                       self.port)


if __name__ == '__main__':
    node = Node('localhost', '8080')

# TODO: Clean this up and add some checks for the input
# Node(str(sys.argv[1]), sys.argv[2], sys.argv[3])


