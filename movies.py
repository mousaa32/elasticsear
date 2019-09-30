from flask import Flask, render_template, request, flash, redirect
from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

app = Flask(__name__)
es = Elasticsearch()


@app.route('/')
def home():
    res = es.search(
        index="movies2",
        size=4849,
        body={
            "query": {
                "match_all": {}
            }
        }
    )
    val = res['hits']['hits']
    total = []
    grand = []
    valeur_anne = []
    ACTEURS = []
    val_acteur = []
    for i in val:
        total.append(i['_source']['fields'])
    for j in total:
        try:
            genres = j['genres']
            genre = ""
            for k in genres:
                # print(k)
                genre = genre+","+k
            acteur = j['actors']
            acteurs = ""
            for l in acteur:
                ACTEURS.append({'nom_acteur': l})
                acteurs = acteurs+","+l
            grand.append({'dierectors': j['directors'][0], 'date de sortie': j['release_date'],
                          'evaluation': j['rating'], 'genres': genre[1:], 'titre': j['title'], 'rang': j['rank'], 'duree de film': j['running_time_secs'],
                          'acteur': acteurs[1:], 'annee': j['year']})
        except:
            continue
    df = pd.DataFrame(data=grand)
    annee = df.groupby('annee')['annee'].count().nlargest(23, keep='all')
    for i in annee:
        valeur_anne.append(i)
    nom_annee = annee.index.tolist()
    df1 = pd.DataFrame(data=ACTEURS)
    actor = df1.groupby('nom_acteur')['nom_acteur'].count().nlargest(23)
    for i in actor:
        val_acteur.append(i)
    nom_acteur = actor.index.tolist()
    evaluation = df.groupby('annee')['evaluation'].mean()
    nom_evaluation = evaluation.index.tolist()
    tab0 = []
    for i in evaluation:
        tab0.append(i)
    a = sum(tab0[0:10])/len(tab0[0:10])
    b = sum(tab0[10:20])/len(tab0[10:20])
    c = sum(tab0[20:30])/len(tab0[20:30])
    d = sum(tab0[30:40])/len(tab0[20:30])
    e = sum(tab0[40:50])/len(tab0[20:30])
    f = sum(tab0[50:60])/len(tab0[20:30])
    g = sum(tab0[60:70])/len(tab0[20:30])
    h = sum(tab0[70:80])/len(tab0[20:30])
    i = sum(tab0[80:len(tab0)])/len(tab0[80:len(tab0)])
    moyenne = []
    moyenne.append([a, b, c, d, e, f, g, h, i])

    j = nom_evaluation[0:10]
    k = nom_evaluation[10:20]
    l = nom_evaluation[20:30]
    m = nom_evaluation[30:40]
    n = nom_evaluation[40:50]
    o = nom_evaluation[50:60]
    p = nom_evaluation[60:70]
    q = nom_evaluation[70:80]
    r = nom_evaluation[80:len(nom_evaluation)]
    tab1 = []
    tab1.append([str(j[0])+"-"+str(j[9]), str(k[0])+"-"+str(k[9]), str(l[0])+"-"+str(l[9]), str(m[0])+"-"+str(m[9]), str(n[0])+"-"+str(n[9]),
                 str(o[0])+"-"+str(o[9]), str(p[0])+"-"+str(p[9]), str(q[0])+"-"+str(q[9]), str(r[0])+"-"+str(r[6])])

    # # print(tab1)
    # data = []
    # a={}
    # for i, j in zip(tab1[0], moyenne[0]):
    #     a = {i,j}
    #     # print(a)
    #     data.append(a)
    # print(data)
    # checkins=tab1[0]
    # labels=tab1[0]
    # checkins = df.groupby('evaluation')['evaluation'].count().nlargest(23)
    # print(mat)
    # def checkins_bar_chart(checkins,labels):
    
    #   colors=['red','green','yellow','blue','cyan','gold','teal','orangered','magenta','skyblue']
    #   ax = checkins.plot(kind='bar', color = colors, fontsize=12)
    #   # print(ax)
    #   ax.set_title("Hotels Checkins Within 10KM\n", fontsize=20)
    #   y_pos = np.arange(len(labels))
    #   # print(labels)
    #   plt.xticks(y_pos, labels)
    #   ax.set_xlabel("Hotels", fontsize=20)
    #   ax.set_ylabel("Checkins", fontsize=20)
    #   plt.show()
    
    
    # print("\nAanalysis\n",pd.DataFrame(np.array(checkins),index=labels))
    # checkins_bar_chart(checkins,labels)

    return render_template('movies.html', valeur_anne=valeur_anne, nom_annee=nom_annee, minium=min(nom_annee), maximum=max(nom_annee),
                           nom_acteur=nom_acteur, val_acteur=val_acteur, moyenne=moyenne[0], tab1=tab1[0])


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
