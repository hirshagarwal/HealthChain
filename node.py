import uuid
from bottle import Bottle, request


class Node(Bottle):
    def __init__(self, host, port, entry_node=None):
        super(Node, self).__init__()
        self.node_id = uuid.uuid4()
        self.nodes = set()
        self.host = host
        self.port = port
        self.name = "Node"

        # API Paths
        self.get('/test', callback=self.test)

        if entry_node is not None:
            print("Registering node to: {}".format(entry_node))
            # Send request with node connection string to the entry node
            pass

        self.run()

    def node_connection_string(self):
        return "{}:{}:{}".format(
            self.node_id,
            self.host,
            self.port
        )

    def run(self, **kwargs):
        super().run(host=self.host, port=self.port, debug=True)

    def register_node(self):
        new_node_string = request.headers.get('node_connection_string')

    def test(self):
        return_message = request.headers.get('message')
        return "{} - {}\n{}:{}".format(self.node_id,
                                       return_message,
                                       self.host,
                                       self.port)


if __name__ == '__main__':
    node = Node('localhost', 8080)
    # node.run(host=node.host, port=8080, debug=True)

# TODO: Clean this up and add some checks for the input
#node = Node(str(sys.argv[1]), sys.argv[2], sys.argv[3])
#node.run()
#route('/test')(node.test)


