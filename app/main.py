import streamlit as st
from pre_process import pre_process
from clustering import clustering
from entropy import entropy_cal
from feature_eng import feature_eng
import pandas as pd
import numpy as np
import plotly.express as px
from feature import feature_matrix
# Use the full page instead of a narrow central column
#st.set_page_config(layout="wide")
st.title(':blue[JENK-]:red[RED]:')
st.subheader('_Jenks-Natural-Break Reduction for Efficient Dimensionality_')


pp = pre_process()
clust = clustering()
fm = feature_matrix()
fe = feature_eng()
en = entropy_cal()
file = st.file_uploader("Upload the dataset", type = ['csv'])
if file is not None:
    df = pd.read_csv(file,index_col=0)
    st.dataframe(df)
    df = fe.Label(df)
    st.divider()
    
    title_text = 'Pre-processing'
    st.markdown(f"<h2 style='text-align: left;'><b>{title_text}</b></h2>", unsafe_allow_html=True)

    cat_th = st.slider("Categorical Features' Threshold",min_value = 1, step = 1)
    X,Y = pp.cat_threshold(cat_th,df)
    col1,col2 = st.columns(2)

    with col1:
       st.dataframe(df[X])
    with col2:
       st.dataframe(df[Y])

    data = df[X].to_numpy()
   
    st.divider()
    
    title_text = 'Clustering'
    st.markdown(f"<h2 style='text-align: left;'><b>{title_text}</b></h2>", unsafe_allow_html=True)

   # KneeLocator parameters
    k = st.slider("k-value Threshold",min_value = 4, step = 1, max_value = 10)
    k_val = range(2,k)
    k_val_arr = np.array(k_val)

    kl,s_score = clust.elbow_method(k_val,data)
    all_knees = st.checkbox("Show all knees/elbows")

    # plot the k-means elbow chart
    st.plotly_chart(clust.plot_figure(k_val_arr, s_score, kl, all_knees), use_container_width=True)

    #JNB Clustering

    sj = clust.jnb_clustering(data, X)

    title_text = 'JNB Clustering'
    st.markdown(f"<h3 style='text-align: left;'><b>{title_text}</b></h3>", unsafe_allow_html=True)
    jnb_sil = pd.DataFrame(sj, columns = ['features','JNB silhoette score'])
    fig = px.bar(jnb_sil, x = 'features', y = 'JNB silhoette score', color='JNB silhoette score',color_continuous_scale = 'plasma' )
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
    title_text = 'Feature Matrix'
    st.markdown(f"<h3 style='text-align: left;'><b>{title_text}</b></h3>", unsafe_allow_html=True)
    st.markdown(f"<p> All potential combinations from the chosen attributes are calculated and placed into a feature matrix for easy comparison. This allows us to understand and compare various multi-dimensional features in a single table-like format, through which we can understand the trade-off between the High dimensional features with a low silhouette score and low-dimensional features with a high silhouette score.</p>", unsafe_allow_html=True)   
    fig = px.imshow(fm.matrix(X,sj), text_auto=True, color_continuous_scale = 'plasma')
    st.plotly_chart(fig, use_container_width=True)

    #Entropy 
    title_text = 'Categorical Feature Ranking'
    st.markdown(f"<h3 style='text-align: left;'><b>{title_text}</b></h3>", unsafe_allow_html=True)
    st.markdown(f"<p> Based on entropy, the user can select features that will most likely match their numerical features. As entropy is a measurement of disorders, one can use it to represent similarity by checking entropy between two clusters. If the clusters are similar they will generate less entropy compared to dissimilar clusters.</p>", unsafe_allow_html=True)
    #st.text('Based on entropy, the user can select features that will most likely match their numerical features. As entropy is a measurement of disorders, one can use it to represent similarity by checking entropy between two clusters. If the clusters are similar they will generate less entropy compared to dissimilar clusters.')
    highest = pp.sort(sj[1:]) 
    options = st.multiselect('Choose the desired features:',X,highest[0])
    result = en.entropy_calculation(options,Y,df)
    fig = px.bar_polar(result, r="Entropy", theta="field",
                   color="Entropy",
                   color_discrete_sequence= px.colors.sequential.Plasma_r,
                   color_continuous_scale = 'plasma')
    st.plotly_chart(fig,use_container_width=True)


    









    






    




