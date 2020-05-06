# -*- coding: utf-8 -*-

import sqlite3
from contextlib import closing

dbname = 'atmos.db'

with closing(sqlite3.connect(dbname)) as conn:
  c = conn.cursor()

  select_sql = 'select * from atmospheres'
  for row in c.execute(select_sql):
      print(row)
