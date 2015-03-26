import sqlite3

import constants
import db


TABLES = [db.Node, db.Edge, db.Logic]

conn = sqlite3.connect(constants.DB_PATH)

c = conn.cursor()

for table in TABLES:
    cols = ', '.join('%s %s' % s for s in table.schema)
    command = 'CREATE TABLE %s (%s)' % (table.table, cols)
    print command
    c.execute('CREATE TABLE %s (%s)' % (table.table, cols))

conn.close()
