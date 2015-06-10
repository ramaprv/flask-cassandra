# flask-cassandra

Python Flask Cassandra Simple Shop CRUD
==================

This is a collection of simple and illustrative Cassandra Shop application. The purpose of this collection is to help new Cassandra users better understand Cassandra and to present illustrative use cases. 

Getting started
---------------

If you don't have access to a Cassandra cluster, you can get started by installing with HomeBrew for Mac.

Getting started
---------------

If you already have access to a Cassandra cluster, you should be able to start running this example application right away. All you have to do is set an environment variable on your client indicating where your cluster is located:

```bash
   $ export BACKEND_STORAGE_IP='mycluster_ip'
```

However, if you don't have access to a Cassandra cluster, you can get started by installing [Ferry](http://ferry.opencore.io). Ferry is an open-source tool that helps developers provision virtual clusters on a local machine. Ferry supports Cassandra (and other "big data" tools) and doesn't require that you actually know how to configure Cassandra to get started. 

Assuming that you are using Ferry, you should run all these commands in a Cassandra client. The first thing to do is install all the prerequisite packages. They can be found in `requirements.txt`. Here's a simple way to do it from the command line using `pip`.

```bash
   $ pip install -r requirements.txt
```

Afterwards, you'll want to set up the Cassandra keyspace and table for our application.

```bash
   $ cqlsh -f createtable.cql
```

After creating the table, you should be able to start the web server by typing:

```bash
   $ python rest.py &
```

Afterwards, insert some data into Cassandra by typing:

```bash
   $ python client.py post 
```

Finally, let's see what data got inserted.

```bash
   $ python client.py fetch  
```
