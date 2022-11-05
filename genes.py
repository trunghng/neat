from abc import ABC
from enum import Enum


class Gene(ABC):
    '''
    Gene abstract class
    '''


class NodeType(Enum):

    INPUT = 'input'
    HIDDEN = 'hidden'
    BIAS = 'bias'
    OUTPUT = 'output'
    NONE = None # denotes Connection


class Node(Gene):
    '''
    Node gene class
    '''

    def __init__(self, node_id: int,
                node_type: NodeType,
                x: float, y: float) -> None:
        '''
        Parameters
        ----------
        node_id: identification number of the node
        node_type: node type
        x: x-coordinate of the node
        y: y-coordinate of the node
        '''
        self.id = node_id
        self.type = node_type
        self.x = x
        self.y = y


class Connection(Gene):
    '''
    Connection gene class
    '''

    def __init__(self, in_node: int,
                out_node: int,
                weight: float,
                enabled: bool,
                innovation_id: int) -> None:
        '''
        Parameters
        ----------
        in_node: in-coming node ID
        out_node: out-going node ID
        weight: weight of the connection
        enabled: whether the connection is expressed
        recurrent: whether the connection is recurrent
        innovation_id: innovation ID
        '''
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.recurrent = recurrent
        self.innovation_id = innovation_id
