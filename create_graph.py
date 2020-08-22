
# -*- coding: utf-8 -*-

import sqlite3
from contextlib import closing
from pathlib import Path
import datetime
import os
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.models import HoverTool

dbname = 'atmos.db'
current =  str(Path(os.path.abspath(__file__)).parents[0])
dbfile = current + '/' + dbname

time_diff = 9

machine_name = '001'

def get_data():
  with closing(sqlite3.connect(dbfile)) as conn:
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    sql = 'select * from atmospheres order by created_at desc limit 25200;'

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

  # temp_graph setting
  temp_graph = figure(
    title="Temperature",
    plot_width=900,
    plot_height=250,
    x_axis_label='date',
    x_axis_type='datetime',
    y_axis_label='temperature(℃)',
    x_range=[date[-3600], date[-1]]
   )
  #temp_graph.y_range.start = min(temperature) if min(temperature) < 0 else 0
  temp_graph.line(date, temperature, line_width=1, legend_label="temperature", color="limegreen")


  # hum_graph setting
  hum_graph = figure(
    title="Humidity",
    plot_width=900,
    plot_height=300,
    x_axis_label='date',
    x_axis_type='datetime',
    y_axis_label='humidity(%)',
    x_range=temp_graph.x_range,
  )
  hum_graph.line(date, humidity, line_width=1, legend_label="humidity", color="blue")
  #hum_graph.y_range.start = 0
  #hum_graph.y_range.end = 100

  # prs_graph setting
  prs_graph = figure(
    title="Air Pressure",
    plot_width=900,
    plot_height=300,
    x_axis_label='date',
    x_axis_type='datetime',
    y_axis_label='air pressure(hPa)',
    x_range=hum_graph.x_range,
  )
  prs_graph.line(date, air_pressure, line_width=1, legend_label="air pressure", color="red")

  # create graph
  show(gridplot([[temp_graph], [hum_graph], [prs_graph]]))

data = get_data()
create_graph(data)
