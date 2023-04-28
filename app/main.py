import streamlit as st
from pre_process import pre_process
from clustering import clustering
from entropy import entropy_cal
from feature_eng import feature_eng
import pandas as pd
import numpy as np
import plotly.express as px
from feature import feature_matrix


st.title("JNB Clustering")
pp = pre_process()
clust = clustering()
fm = feature_matrix()
fe = feature_eng()
en = entropy_cal()
file = st.file_uploader("Upload the dataset", type = ['csv'])
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df)
    df = fe.Label(df)
    st.dataframe(df)
    cat_th = st.slider("Categorical Features' Threshold",min_value = 1, step = 1)
    X,Y = pp.cat_threshold(cat_th,df)
    col1,col2 = st.columns(2)

    with col1:
       st.dataframe(df[X])
    with col2:
       st.dataframe(df[Y])

    data = df[X].to_numpy()
   

   # KneeLocator parameters
    k = st.slider("k-value Threshold",min_value = 2, step = 1, max_value = 10)
    k_val = range(2,k)
    k_val_arr = np.array(k_val)

    kl,s_score = clust.elbow_method(k_val,data)
    all_knees = st.checkbox("Show all knees/elbows")

    # plot the figure
    st.write(clust.plot_figure(k_val_arr, s_score, kl, all_knees))

    sj = clust.jnb_clustering(data, X)

    jnb_sil = pd.DataFrame(sj, columns = ['features','JNB sil_score'])
    fig = px.bar(jnb_sil, x = 'features', y = 'JNB sil_score', color='JNB sil_score')
    st.plotly_chart(fig, use_container_width=True)

    #threshold
    S = st.number_input(label = 'Select the percentange of data to be taken into consideration (based on Silhoette Score)', min_value=25, max_value=100, step=5)

    threshold = (100 - S)  * len(X)// 100
   
    X = []

    for i in range(len(sj)-1, threshold-1,-1):
         X.append(sj[i][0])

    st.text('Selected Features:')
    st.write(X)

    r = fm.printPowerSet(X)
    sj = clust.allPossibleSubsets(r,df)

    #Feature Matrix 
    st.text('Feature Matrix')
    fig = px.imshow(fm.matrix(X,sj), text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    #Entropy 
    highest = pp.sort(sj[1:]) 
    options = st.multiselect('Choose the desired features:',X,highest[0])
    result = en.entropy_calculation(options,Y,df)
    fig = px.bar_polar(result, r="Entropy", theta="field",
                   color="Entropy",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
    st.plotly_chart(fig,use_container_width=True)


    









    






    




