import clustering 
from scipy.stats import entropy
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans

class entropy_cal:
    def k_means_clust(self,n_clust,data):
        km = KMeans(n_clusters = n_clust, init='k-means++',
            n_init=10, max_iter=300,
                tol=1e-04, random_state=0)
        
        km_predict = km.fit_predict(data)
        return(km_predict)
    
    def entropy_calculation(self,option,categorical,df):

        data = df[option].to_numpy()
        clust = clustering.clustering()
        k_val = range(2,8)
        elbow = clust.elbow_method(k_val,data)
        temp= self.k_means_clust(elbow[0].knee,data)

        temp = temp + 1
        en = []

        for i in categorical:
            y = df[i].to_numpy().astype(int)
            y = y + 1
            en.append((i,entropy(temp,y)))

        en = sorted(en, key = lambda x: x[1])
        df2 = pd.DataFrame(en,columns =['field','Entropy'])
        return df2



        