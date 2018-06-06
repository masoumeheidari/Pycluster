
import psycopg2
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.optics import optics
from pyclustering.cluster.dbscan import dbscan
from pyclustering.cluster import cluster_visualizer


class pycluster():
    def __init__(self):
        ######################## Preparing Data #############################
        self.conn = psycopg2.connect(database='mytestdb', user='postgres', password='angel9014', host='localhost', port=5432)
        self.cur = self.conn.cursor()
        query = self.cur.execute('select * from public.points;')
        rows = []
        rows = self.cur.fetchmany(1000)
        self.data = []
        xdata = []
        ydata = []
        temp = dict()
        for i in rows:
            temp = i[5], i[6]
            self.data.append(temp)
            xdata.clear()
            xdata.append(i[5])
            xdata.append(i[6])
            ydata.append(xdata)


        # check that tables exists or not
        self.cur.execute("select * from information_schema.tables where table_name=%s", ('kmeans',))
        if bool(self.cur.rowcount):
            self.cur.execute("DROP TABLE kmeans;")
            self.cur.execute("DROP TABLE dbscan;")
            self.cur.execute("DROP TABLE optics;")
            self.conn.commit()

        self.cur.execute("CREATE TABLE kmeans (data varchar, id SERIAL PRIMARY KEY);")
        self.cur.execute("CREATE TABLE dbscan (data varchar, id SERIAL PRIMARY KEY);")
        self.cur.execute("CREATE TABLE optics (data varchar, id SERIAL PRIMARY KEY);")
        self.conn.commit()


    def kmeans_func(self):
        ####################### K-Means Algorithm #############################

        start_centers = [ [45.8386509747745, 9.06182105319716], [45.8386094288896, 9.06191748978146] ]
        kmeans_instance = kmeans(self.data, start_centers)
        kmeans_instance.process()
        clusters = kmeans_instance.get_clusters()
        centers = kmeans_instance.get_centers()

        ########## Ploting data
        # visualizer = cluster_visualizer();
        # visualizer.append_clusters(clusters, data);
        # visualizer.append_cluster(start_centers, marker = '*', markersize = 5);
        # visualizer.append_cluster(centers, marker = '*', markersize = 5);
        # visualizer.show();

        w = 0
        for i in range(len(clusters)):
            if len(clusters[i]) > w:
                w = len(clusters[i])

        h = len(clusters)

        output = [[0 for x in range(w)] for y in range(h)]
        for i in range(len(clusters)):
            for j in range(len(clusters[i])):
                output[i][j] = self.data[clusters[i][j]]

        ########## Writing data to file
        # with open('out.txt', mode='w') as fp:
        #     fp.write("######################### K-Means Algorithm Output #########################\n")
        #     fp.write(str(output))
        #     fp.write('\n\n')
        #     fp.close()

        self.cur.execute("INSERT INTO kmeans VALUES (%s)", (str(output), ))


    def dbscan_func(self):
        ####################### DB-Scan Algorithm ###########################

        dbscan_instance = dbscan(self.data, 2, 3)
        dbscan_instance.process()
        clusters = dbscan_instance.get_clusters()

        ########## Ploting data
        # visualizer = cluster_visualizer();
        # visualizer.append_clusters(clusters, data);
        # visualizer.append_cluster(start_centers, marker = '*', markersize = 5);
        # visualizer.show();

        w = 0
        for i in range(len(clusters)):
            if len(clusters[i]) > w:
                w = len(clusters[i])

        h = len(clusters)

        output = [[0 for x in range(w)] for y in range(h)]
        for i in range(len(clusters)):
            for j in range(len(clusters[i])):
                output[i][j] = self.data[clusters[i][j]]

        ########## Writing data to file
        # with open('out.txt', mode='a') as fp:
        #     fp.write("######################### DB-Scan Algorithm Output #########################\n")
        #     fp.write(str(clusters))
        #     fp.write('\n\n')
        #     fp.close()

        self.cur.execute("INSERT INTO dbscan VALUES (%s)", (str(output), ))


    def optics_func(self):
        ###################### Optics Algorithm ###################

        optics_instance = optics(self.data, 2, 3)
        optics_instance.process()
        clusters = optics_instance.get_clusters()

        ########## Ploting data
        # visualizer = cluster_visualizer();
        # visualizer.append_clusters(clusters, data);
        # visualizer.append_cluster(start_centers, marker = '*', markersize = 5);
        # visualizer.show();

        w = 0
        for i in range(len(clusters)):
            if len(clusters[i]) > w:
                w = len(clusters[i])

        h = len(clusters)

        output = [[0 for x in range(w)] for y in range(h)]
        for i in range(len(clusters)):
            for j in range(len(clusters[i])):
                output[i][j] = self.data[clusters[i][j]]

        ########## Writing data to file
        # with open('out.txt', mode='w') as fp:
        #     fp.write("######################### Optics Algorithm Output #########################\n")
        #     fp.write(str(output))
        #     fp.write('\n\n')
        #     fp.close()

        self.cur.execute("INSERT INTO optics VALUES (%s)", (str(output), ))
        self.conn.commit()

        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    pycl = pycluster()
    pycl.kmeans_func()
    pycl.dbscan_func()
    pycl.optics_func()
