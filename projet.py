import psycopg2
from psycopg2.extras import RealDictCursor
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ['localhost'],
    port=9200
)

#pour supprimer un index
es.indices.delete(index='sante', ignore=[400, 404])


con =psycopg2.connect(
    host="localhost",
    database="apirest",
    user="postgres",
    password="Diop1957+",
    port=5432
)
cur =con.cursor(cursor_factory=RealDictCursor)
cur.execute(''' select * from data_region''')
a=cur.fetchall()
for i in a:
    # print(i)
    es.index(index='sante', doc_type='test',body=i) 


#******************************************les reponses**********************************
#les 5 taux:http://localhost:9200/sante/_search?_source=region&sort=tesp:desc&size=5
#recherche_all:http://localhost:9200/sante/test/_search?
#recherche/region:http://localhost:9200/sante/test/_search?q=region:nom_region
#pour une region une caracteristique:http://localhost:9200/sante/_search?q=region:nom_region&_source=region,le taux 
#update :http://localhost:9200/sante/test/id_generee methode put
#post:http://localhost:9200/sante/test/