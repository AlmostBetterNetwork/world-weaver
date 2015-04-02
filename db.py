import sqlite3

import constants



class DBException(Exception):
    pass


class DBObject(object):

    def __init__(self, conn, id, body=None):
        self.conn = conn
        self.id = id
        self.body = None
        if not body:
            self._fetch()
        else:
            self._save(body)

    @classmethod
    def create(cls, conn, val):
        return cls(conn, val[0], val)

    def _fetch(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM ? WHERE id=? LIMIT 1', (self.table, self.id))
        body = c.fetchone()
        if not body:
            raise DBException('Could not find row')
        return self._save(body)

    def _save(self, body):
        self.body = {}
        for i, sch in self.schema:
            name, _ = sch
            self.body[name] = body[i]
        return self.body

    def refresh(self):
        self.body = None
        self._fetch()

    def get(self, name, default=None):
        return self.body.get(name, default)


class Node(DBObject):
    obj_type = 'node'
    table = 'nodes'
    schema = [
        ('id', 'integer primary key'),
        ('root', 'integer'),
        ('parent', 'integer'),
        ('body', 'text'),
        ('logic_entrance_id', 'integer'),
        ('logic_exit_id', 'integer'),
        ('logic_subnode_id', 'integer'),
    ]

    def get_outbound_edges(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM edges WHERE source_node_id = ?', (self.id, ))
        while 1:
            body = c.fetchone()
            if not body:
                return
            yield Edge.create(body)

    def get_subnodes(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM nodes WHERE parent = ?', (self.id, ))
        while 1:
            body = c.fetchone()
            if not body:
                return
            yield Node.create(self.conn, body)

    def is_root(self):
        return self.body['root'] == 1

    def get_parent(self):
        return Node(self.conn, self.body['parent']) if self.body['parent'] else None

    def get_subnode_logic(self):
        return Logic(self.conn, self.body['logic_subnode_id']) if self.body['logic_subnode_id'] else None

    def get_entrance_logic(self):
        return Logic(self.conn, self.body['logic_entrance_id']) if self.body['logic_entrance_id'] else None

    def get_exit_logic(self):
        return Logic(self.conn, self.body['logic_exit_id']) if self.body['logic_exit_id'] else None


class Edge(DBObject):
    obj_type = 'edge'
    table = 'edges'
    schema = [
        ('id', 'integer primary key'),
        ('body', 'text'),
        ('source_node_id', 'integer'),
        ('destination_node_id', 'integer'),
        ('logic_trigger_id', 'integer'),
    ]

    def get_text(self):
        return self.body['body']

    def get_source_node(self):
        return Node(self.conn, self.body['source_node_id'])

    def get_destination_node(self):
        return Node(self.conn, self.body['destination_node_id'])

    def get_trigger_logic(self):
        return Logic(self.conn, self.body['logic_trigger_id']) if self.body['logic_trigger_id'] else None


class Logic(DBObject):
    obj_type = 'logic'
    table = 'logic'
    schema = [
        ('id', 'integer primary key'),
        ('body', 'text'),
    ]

    def get_content(self):
        return self.body['body']


def get_root_node(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM nodes WHERE root=1 LIMIT 1')
    body = c.fetchone()
    if not body:
        return None

    return Node.create(conn, body)


def setup():
    return sqlite3.connect(constants.DB_PATH)

def teardown(conn):
    if conn:
        conn.close()
