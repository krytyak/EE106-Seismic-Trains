import sqlite3
import obspy
import numpy as np

def geostats(stream):
    for i in range(len(stream)):
        stream[i].stats.delta = (last_pick-first_pick)
        stream[i].stats.sampling_rate = (len(data_x)/(last_pick-first_pick))
        stream[i].stats.starttime=first_pick    
    return

# Create a SQL connection to our SQLite database
con = sqlite3.connect("geophone.db")

cur = con.cursor()
TimeAndDate=[]
data_x=[]
i=0
# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT datetime FROM geophone;'):
    TimeAndDate.append((row[0]))
for row in cur.execute('SELECT geophone_x FROM geophone;'):
    data_x.append(float(row[0]))
data_y=[]
i=0
for row in cur.execute('SELECT geophone_y FROM geophone;'):
    data_y.append(float(row[0]))
data_z=[]
i=0
for row in cur.execute('SELECT geophone_z FROM geophone;'):
    data_z.append(float(row[0]))
# Be sure to close the connection
con.close()
first_pick = obspy.UTCDateTime(TimeAndDate[0])
last_pick = obspy.UTCDateTime(TimeAndDate[-1])
data_x_np = np.asarray(data_x)
tr1 = obspy.Trace(data=data_x_np)
data_y_np = np.asarray(data_y)
tr2 = obspy.Trace(data=data_y_np)
data_z_np = np.asarray(data_z)
tr3 = obspy.Trace(data=data_z_np)
st = obspy.Stream(traces=[tr1,tr2,tr3])
geostats(st)
