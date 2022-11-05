from typing import List
from enum import Enum
from genes import NodeType

class InnovationType(Enum):

    NEW_NODE = 'new node'
    NEW_CONNECTION = 'new connection'


class Innovation:
    '''
    Innovation class
    '''

    def __init__(self, innovation_id: int,
            innovation_type: InnovationType,
            in_node: int,
            out_node: int,
            node_id: int,
            node_type: NodeType) -> None:
        '''
        Parameters
        ----------
        innovation_id: innovation ID
        innovation_type: innovation type
        in_node: in-coming node ID
        out_node: out-going node ID
        node_id: node ID, -1 if connection
        node_type: node type
        '''
        self.id = innovation_id
        self.type = innovation_type
        self.in_node = in_node
        self.out_node = out_node
        self.node_id = node_id
        self.node_type = node_type


class InnovationDB:
    '''
    Innovation database
    '''

    def __init__(self) -> None:
        self.db = dict
        self.global_innovation_id = 0
        self.current_node_id = 0
        self.current_connection_id = 0


    def next_innovation(self) -> int:
        self.global_innovation_id += 1
        return self.global_innovation_id


    def next_node(self) -> int:
        self.current_node_id += 1
        return self.current_node_id


    def nex_connection(self) -> int:
        self.current_connection_id += 1
        return self.current_connection_id


    def create(self, 
            innovation_type: InnovationType,
            node_type: NodeType=NodeType.NONE,
            in_node: int=None,
            out_node: int=None) -> int:
        '''
        Create new innovation and add to the DB

        Parameters
        ----------
        innovation_type: innovation type
        node_type: node type
        in_node: in-coming node ID
        out_node: out-going node ID

        Returns
        -------
        node_id: current node/connection ID
        innovation_id: ID of the new created innovation, 
            or an old ID if it already exists
        '''
        if node_type == NodeType.INPUT or node_type == NodeType.OUTPUT:
            in_node = out_node = -1
            innovation_id = self.next_innovation()
        else:
            innovation_id = self.contains(innovation_type, in_node, out_node)

            if innovation_id == -1:
                innovation_id = self.next_innovation()

        if innovation_type == InnovationType.NEW_NODE:
            node_id = self.next_node()
        else:
            node_id = self.next_connection()

        if innovation_id != -1:
            innovation = Innovation(innovation_id, innovation_type, 
                in_node, out_node, node_id, node_type)
            self.add(innovation)

        return node_id, innovation_id


    def add(self, innovation: Innovation) -> None:
        '''
        Add an innovation to the DB
        '''
        inv_type, inn, outn = innovation.innovation_type, innovation.in_node, innovation.out_node
        if inv_type not in self.db:
            self.db[inv_type] = dict()
        if inn not in self.db[inv_type]:
            self.db[inv_type][inn] = dict()
        if outn not in self.db[inv_type][inn]:
            self.db[inv_type][inn][outn] = dict()
        self.db[inv_type][inn][outn][node_id] = innovation


    def contains(self,
                innovation_type: InnovationType,
                in_node: int,
                out_node: int) -> int:
        '''
        Whether the DB contains the innovation

        Parameters
        ----------
        innovation_type: innovation type
        in_node: in-coming node ID
        out_node: out-going node ID

        Returns
        -------
            ID of the innovation if it is in the DB, otherwise return -1
        '''
        innovation = self.db[innovation_type][in_node][out_node]
        if innovation:
            return innovation.id
        return -1

