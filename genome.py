from typing import List, Tuple, Dict
from random import random, choice
from copy import deepcopy

from genes import Node, Connection, NodeType as NT
from innovation import Innovation, InnovationDB, InnovationType as IT


class Genome:
    '''
    Genome class
    '''

    def __init__(self, genome_id: int,
                connections: List[Connection],
                innovations: InnovationDB,
                mutation_rate: float,
                loop_rate: float) -> None:
        '''
        Parameters
        ----------
        genome_id: genome idenitication number
        connections: connection gene list
        innovations: innovation database
        mutation_rate: mutation rate
        loop_rate: chance that a new connection is a loop
        '''
        self.id = genome_id
        self.connections = dict()
        self._set_connections(connections)
        self._set_nodes(connections)
        self.innovations = innovations
        self.fitness = None


    def _add_connection(self, c: Connection) -> None:
        self.connections[(c.in_node, c.out_node)] = c


    def _add_node(self, node: Node) -> None:
        self.nodes[node.id] = node


    def _set_connections(self, connections: List[Connection]) -> None:
        for c in connections:
            self._add_connection(c)


    def _set_nodes(self, connections: List[Connection]) -> None:
        for c in connections:
            self._add_node(connection.in_node)
            self._add_node(connection.out_node)


    def crossover(self, other) -> object:
        pass


    def add_connection(self) -> bool:
        '''
        Add connection gene mutation

        Returns
        -------
        whether a new connection is successfully created
        '''
        if random() > self.mutation_rate:
            return False
        
        in_node = None
        out_node = None
        recurrent = False

        if random() < self.loop_rate:
            node_pool = list(self.nodes.values())

            while node_pool:
                node = choice(node_pool)
                if node.recurrent or node.type == NT.BIAS or node.type == NT.INPUT:
                    node_pool.remove(node)
                    assert node not in node_pool, 'Remove failed!'
                else:
                    in_node = out_node = node
                    recurrent = True
                    break
        else:
            in_node_pool = list(self.nodes.values())
            out_node_pool = list(self.nodes.values())

            def _connection_existed(in_node__: int, out_node__: int) -> bool:
                return self.connections[(in_node__, out_node__)] is not None

            while in_node_pool:
                in_node_ = choice(in_node_pool)
                out_node_pool_ = deepcopy(out_node_pool).remove(in_node_)

                while out_node_pool_:
                    out_node_ = choice(out_node_pool_)

                    if _connection_existed(in_node_, out_node_) or 
                            out_node_.type == NT.BIAS or out_node_.type == NT.INPUT:
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

            self.create_connection(in_node.id, out_node.id, recurrent)
            return True


    def add_node(self) -> bool:
        '''
        Add node gene mutation

        Returns
        -------
        whether a new node is successfully created
        '''
        if random() > self.mutation_rate:
            return False

        connection_pool = list(self.connections.values())

        while connection_pool:
            connection = choice(connection_pool)

            if connection.recurrent or not connection.enabled \
                    or self.nodes[connection.in_node].type == NT.BIAS:
                connection_pool.remove(connection)
            else:
                node = self.create_node(connection.in_node, connection.out_node)
                self.create_connection(connection.in_node, node.id, False)
                self.create_connection(node.id, connection.out_node, False)
                return True
        return False


    def create_connection(self, in_node: int, out_node: int, recurrent: bool) -> Connection:
        '''
        
        '''
        innovation_id, _  = self.innovations.create(IT.NEW_CONNECTION, in_node, out_node)
        weight = self._random_clamp()
        connection = Connection(in_node, out_node, weight, True, recurrent, innovation_id)
        self._add_connection(connection)
        return connection


    def create_node(self, in_node: int, out_node: int) -> Node:
        '''
        
        '''
        _, node_id = self.innovations.create(IT.NEW_NODE, in_node, out_node)
        x = (self.nodes[in_node].x + self.nodes[out_node].x) / 2
        y = (self.nodes[in_node].y + self.nodes[out_node].y) / 2;
        node = Node(node_id, NT.HIDDEN, x, y)
        self._add_node(node)
        return node


        



    def _random_clamp(self) -> float:
        return random() * 2 - 1


