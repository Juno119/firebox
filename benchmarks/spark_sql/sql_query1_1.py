# SELECT pageURL, pageRank FROM rankings WHERE pageRank > X

import sys,os

assert len(sys.argv) == 2

from pyspark import SparkContext
sc = SparkContext(appName="PythonKMeans")

# sc is an existing SparkContext.
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load a text file and convert each line to a dictionary.
#lines = sc.textFile("/data/joao/rankings.txt")
lines = sc.textFile("/nscratch/joao/rankings.txt")
#lines = sc.textFile("/nscratch/joao/1node-text/1node/rankings/rankings.txt")

#lines.cache()

parts = lines.map(lambda l: l.split(","))
rankings = parts.map(lambda p: {"pageURL": p[0], "pageRank": int(p[1]), "avgDuration":int(p[2])})

# Infer the schema, and register the SchemaRDD as a table.
# In future versions of PySpark we would like to add support for registering RDDs with other
# datatypes as tables
schemaRanking = sqlContext.inferSchema(rankings)
schemaRanking.registerAsTable("rankings")

# SQL can be run over SchemaRDDs that have been registered as a table.
#teenagers = sqlContext.sql("SELECT name FROM people WHERE age >= 13 AND age <= 19")

print "Running query: ", sys.argv[1]
num_query = int(sys.argv[1])
#num_query = sys.argv[1]

print "Num_query: " + str(num_query) + "\n"

if num_query == 1:
    urls = sqlContext.sql("SELECT pageURL, pageRank FROM rankings WHERE pageRank > 10")
elif num_query == 2:
    urls = sqlContext.sql("SELECT pageURL, pageRank FROM rankings WHERE pageRank > 100")
elif num_query == 3:
    urls = sqlContext.sql("SELECT pageURL, pageRank FROM rankings WHERE pageRank > 1000")
elif num_query == 4:
    urls = sqlContext.sql("SEECT pageURL, pageRank FROM ranks WERE pageRank > 1000")
else: assert 0

# The results of SQL queries are RDDs and support all the normal RDD operations.
#teenNames = teenagers.map(lambda p: "Name: " + p.name)
#for url in urls.collect():
#    print url
urls.collect()
