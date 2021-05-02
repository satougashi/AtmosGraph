
# -*- coding: utf-8 -*-

import sqlite3
from contextlib import closing
from pathlib import Path
import datetime
import os
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.models import HoverTool

dbname = 'atmos.db'
current = str(Path(os.path.abspath(__file__)).parents[0])
dbfile = current + '/' + dbname

time_diff = 9

machine_name = '001'

lang = 'JP'
label = {
  'temperature': {
    'EN': 'Temperature',
    'JP': '気温',
  },
  'humidity': {
    'EN': 'Humidity',
    'JP': '湿度',
  },
  'air_pressure': {
    'EN': 'Air Pressure',
    'JP': '気圧',
  },
}


def get_data():
  with closing(sqlite3.connect(dbfile)) as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    sql = 'select * from atmospheres order by created_at desc limit 3600;'

    c.execute(sql)

    return c.fetchall()

def create_graph(data):
  output_file(current + "/templates/" + 'graph.html')

  #prepare data
  temperature = []
  humidity = []
  air_pressure = []
  date = []
  for row in reversed(data):
    temperature.append(row['temperature'])
    air_pressure.append(row['humidity'])
    humidity.append(row['air_pressure'])
    time = datetime.datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
    time += datetime.timedelta(hours=time_diff)
    date.append(time)

  mindate = date[-3600] if len(date) > 3600 else date[-1 * (len(date))]
  # temp_graph setting
  temp_graph = figure(
    title=label["temperature"][lang],
    plot_width=900,
    plot_height=300,
    x_axis_label='date',
    x_axis_type='datetime',
    y_axis_label=label["temperature"][lang] + '(℃)',
    x_range=[mindate, date[-1]],
    tooltips=[(label["temperature"][lang], "$y")],
   )
  #temp_graph.y_range.start = min(temperature) if min(temperature) < 0 else 0
  temp_graph.line(date, temperature, line_width=1, color="limegreen")
  #temp_graph.line(date, temperature, line_width=1, legend_label=label["temperature"][lang], color="limegreen")


  # hum_graph setting
  hum_graph = figure(
    title=label["humidity"][lang],
    plot_width=900,
    plot_height=300,
    x_axis_label='date',
    x_axis_type='datetime',
    y_axis_label=label["humidity"][lang] + '(%)',
    x_range=temp_graph.x_range,
    tooltips=[(label["humidity"][lang], "$y")],
  )
  hum_graph.line(date, humidity, line_width=1, color="blue")
  #hum_graph.line(date, humidity, line_width=1, legend_label=label["humidity"][lang], color="blue")
  #hum_graph.y_range.start = 0
  #hum_graph.y_range.end = 100

  # prs_graph setting
  prs_graph = figure(
    title=label["air_pressure"][lang],
    plot_width=900,
    plot_height=300,
    x_axis_label='date',
    x_axis_type='datetime',
    y_axis_label=label["air_pressure"][lang] + '(hPa)',
    x_range=hum_graph.x_range,
    tooltips=[(label["air_pressure"][lang], "$y")],
  )
  prs_graph.line(date, air_pressure, line_width=1, color="red")
  #prs_graph.line(date, air_pressure, line_width=1, legend_label=label["air_pressure"][lang], color="red")

  # create graph
  show(gridplot([[temp_graph], [hum_graph], [prs_graph]]))

data = get_data()
create_graph(data)
