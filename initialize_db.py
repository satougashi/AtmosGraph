# -*- coding: utf-8 -*-

import sqlite3
from contextlib import closing

dbname = 'atmos.db'

with closing(sqlite3.connect(dbname)) as conn:
  c = conn.cursor()

  # db上はUTCとして扱う
  create_table = '''
    create table atmospheres (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      machime_name TEXT,
      temperature REAL,
      humidity REAL,
      air_pressure REAL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP CHECK(
        created_at like '____-__-__ __:__:__'
      )
    )'''

  c.execute(create_table)

  conn.commit()
