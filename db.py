import sqlite3

import constants


conn = None


class DBObject(object):

    def __init__(self, id):
        self.id = id
        self._fetch()

    def _fetch(self):
        pass


class Node(DBObject):
    obj_type = 'node'

    def get_outbound_edges(self):
        pass

    def get_subnodes(self):
        pass

    def get_subnode_logic(self):
        pass

    def get_entrance_logic(self):
        pass

    def get_exit_logic(self):
        pass


class Edge(DBObject):
    obj_type = 'edge'

    def get_text(self):
        pass

    def get_destination_node_id(self):
        pass

    def get_trigger_logic(self):
        pass


class Logic(DBObject):
    obj_type = 'logic'

    def get_code(self):
        pass


def get_root_node():
    pass

def get_node(id):
    pass


def setup():
    conn = sqlite3.connect(constants.DB_PATH)


def teardown():
    if conn:
        conn.close()
