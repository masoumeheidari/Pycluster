
import psycopg2
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.optics import optics
from pyclustering.cluster.dbscan import dbscan
from pyclustering.cluster import cluster_visualizer

######################## Preparing Data #############################

conn = psycopg2.connect(database='mytestdb', user='postgres', password='angel9014', host='localhost', port=5432)
cur = conn.cursor()
query = cur.execute('select * from public.points;')
rows = []
rows = cur.fetchmany(100)
data = []
xdata = []
ydata = []
temp = dict()
for i in rows:
    temp = i[5], i[6]
    data.append(temp)
    xdata.clear()
    xdata.append(i[5])
    xdata.append(i[6])
    ydata.append(xdata)


# check that tables exists or not
cur.execute("select * from information_schema.tables where table_name=%s", ('kmeans',))
if bool(cur.rowcount):
    cur.execute("DROP TABLE kmeans;")
    cur.execute("DROP TABLE dbscan;")
    cur.execute("DROP TABLE optics;")
    conn.commit()

cur.execute("CREATE TABLE kmeans (data varchar, id SERIAL PRIMARY KEY);")
cur.execute("CREATE TABLE dbscan (data varchar, id SERIAL PRIMARY KEY);")
cur.execute("CREATE TABLE optics (data varchar, id SERIAL PRIMARY KEY);")
conn.commit()


####################### K-Means Algorithm #############################

start_centers = [ [45.8386509747745, 9.06182105319716], [45.8386094288896, 9.06191748978146] ]
kmeans_instance = kmeans(data, start_centers)
kmeans_instance.process()
clusters = kmeans_instance.get_clusters()
centers = kmeans_instance.get_centers()

visualizer = cluster_visualizer();
visualizer.append_clusters(clusters, data);
visualizer.append_cluster(start_centers, marker = '*', markersize = 20);
visualizer.append_cluster(centers, marker = '*', markersize = 20);
visualizer.show();

with open('out.txt', mode='w') as fp:
    fp.write("######################### K-Means Algorithm Output #########################\n")
    fp.write(str(clusters))
    fp.write('\n\n')
    fp.close()

cur.execute("INSERT INTO kmeans VALUES (%s)", (str(clusters), ))


####################### DB-Scan Algorithm ###########################

dbscan_instance = dbscan(data, 2, 3)
dbscan_instance.process()
clusters = dbscan_instance.get_clusters()

visualizer = cluster_visualizer();
visualizer.append_clusters(clusters, data);
visualizer.append_cluster(start_centers, marker = '*', markersize = 20);
visualizer.show();

with open('out.txt', mode='a') as fp:
    fp.write("######################### DB-Scan Algorithm Output #########################\n")
    fp.write(str(clusters))
    fp.write('\n\n')
    fp.close()

cur.execute("INSERT INTO dbscan VALUES (%s)", (str(clusters), ))


###################### Optics Algorithm ###################

optics_instance = optics(data, 2, 3)
optics_instance.process()
clusters = optics_instance.get_clusters()

visualizer = cluster_visualizer();
visualizer.append_clusters(clusters, data);
visualizer.append_cluster(start_centers, marker = '*', markersize = 20);
visualizer.show();

with open('out.txt', mode='a') as fp:
    fp.write("######################### Optics Algorithm Output #########################\n")
    fp.write(str(clusters))
    fp.write('\n\n')
    fp.close()

cur.execute("INSERT INTO optics VALUES (%s)", (str(clusters), ))
conn.commit()

cur.close()
conn.close()
