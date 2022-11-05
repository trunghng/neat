from typing import List, Tuple, Dict
import random as rand
from copy import deepcopy

from genes import Node, Connection, NodeType as NT
from innovation import InnovationType, Innovation, InnovationDB


class Genome:
    '''
    Genome class
    '''

    def __init__(self, genome_id: int,
                connections: List[Connection],
                innovations: InnovationDB) -> None:
        '''
        Parameters
        ----------
        genome_id: genome idenitication number
        connections: connection gene list
        innovations: innovation database
        '''
        self.id = genome_id
        self.connections = dict()
        self.connections = self._get_connections()
        self.inputs, self.hiddens, self.biases, \
            self.outputs, self.node_count = self._get_nodes()
        self.innovations = innovations
        self.fitness = None


    def _get_connections(self) -> Dict[int, Dict[int, Connection]]:
        for c in self.connections:
            self._add_connection(c)
        return self.connections


    def _add_connection(self, c: Connection) -> None:
        if c.in_node in self.connections:
            self.connections[c.in_node][c.out_node] = c
        else:
            self.connections[c.in_node] = dict()


    def _get_nodes(self) -> Tuple[List[Node], List[Node], \
            List[Node], List[Node], int]:
        inputs, hiddens, biases, outputs = [], [], [], []
        node_count = 0

        def __add_node(node: Node, node_type: NT, nodes: List[Node]) -> None:
            if node.type == node_type and node not in nodes:
                nodes.append(node)
                node_count += 1

        for connection in connections:
            in_node = connection.in_node
            out_node = connection.out_node

            __add_node(in_node, NT.INPUT, inputs)
            __add_node(in_node, NT.HIDDEN, hiddens)
            __add_node(in_node, NT.BIAS, biases)
            __add_node(out_node, NT.HIDDEN, hiddens)
            __add_node(out_node, NT.OUTPUT, outputs)

        return inputs, hiddens, biases, outputs, node_count


    def crossover(self, other) -> object:
        pass


    def add_connection(self, mutation_rate: float,
                        loop_rate: float) -> bool:
        '''
        Add a connection to the genome

        Parameters
        ----------
        mutation_rate: mutation rate
        loop_rate: chance that a new connection is a loop

        Returns
        -------
        whether a new connection is successfully created
        '''
        if rand.uniform(0, 1) > mutation_rate:
            return False
        
        in_node = None
        out_node = None
        recurrent = False

        if random.uniform(0, 1) < loop_rate:
            node_pool = deepcopy(self.hiddens + self.outputs)

            while not node_pool:
                node = rand.choice(node_pool)
                if node.recurrent:
                    node_pool.remove(node)
                    assert node not in node_pool, 'Remove failed!'
                else:
                    in_node = out_node = node
                    recurrent = True
                    break
        else:
            in_node_pool = deepcopy(self.inputs + self.hiddens + \
                    self.biases + self.outputs)
            out_node_pool = deepcopy(self.hiddens + self.outputs)

            def _connection_existed(in_node__: int, out_node__: int) -> bool:
                return self.connections[in_node__][out_node__] is not None

            while not in_node_pool:
                in_node_ = rand.choice(in_node_pool)
                out_node_pool_ = deepcopy(out_node_pool).remove(in_node_)

                while not out_node_pool_:
                    out_node_ = rand.choice(out_node_pool_)

                    if _connection_existed(in_node_, out_node_):
                        out_node_pool_.remove(out_node_)
                        assert out_node_ not in out_node_pool_, 'Remove failed!'
                    else:
                        in_node = in_node_
                        out_node = out_node_
                        break
                if in_node is None:
                    in_node_pool.remove(in_node_)
                else:
                    break
            if in_node is None:
                return False
            else:
                if in_node.y > out_node.y:
                    recurrent = True

            _, innovation_id = self.innovations.create(
                InnovationType.NEW_CONNECTION, in_node.id, out_node.id)
            weight = None # TODO
            connection = Connection(in_node.id, out_node.id, weight, True, recurrent, innovation_id)
            self._add_connection(connection)
            return True


    def add_node(self, mutation_rate: float,
                innovations: List[Innovation]) -> bool:
        if rand.uniform(0, 1) < mutation_rate:
            return False
        pass


