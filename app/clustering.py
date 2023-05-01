from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from jenkspy import JenksNaturalBreaks
from kneed import KneeLocator
from plotly import graph_objects as go
import pandas as pd


class clustering:
    def __init__(self) -> None:
        pass

    #k-means

    def k_means_clust(self,n_clust,data):
        km = KMeans(n_clusters = n_clust, init='k-means++',
            n_init=10, max_iter=300,
                tol=1e-04, random_state=0)
        
        km.fit_predict(data)
        s_score = silhouette_score(data, km.labels_, metric = 'euclidean')
        return(s_score)
    
    #plot

    def plot_figure(self,x, y, kl, all_knees):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines+markers",
                line=dict(color="#2600f7", width=2),
                name="input data",
            
            )
        )
        if all_knees:
            fig.add_trace(
                go.Scatter(
                    x=sorted(list(kl.all_knees)),
                    y=list(kl.all_knees_y),
                    mode="markers",
                    marker=dict(
                        color="orange",
                        size=8,
                        line=dict(width=1, color="DarkSlateGrey"),
                    ),
                    marker_symbol="diamond",
                    name="potential knee",
                )
            )
        fig.add_trace(
            go.Scatter(
                x=[kl.knee],
                y=[kl.knee_y],
                mode="markers",
                marker=dict(
                    color="orangered",
                    size=12,
                    line=dict(width=1, color="DarkSlateGrey"),
                ),
                marker_symbol="x",
                name="knee point",
            )
        )
        fig.add_trace(
            go.Scatter(
            x=[kl.knee, kl.knee],
            y=[min(y), max(y)],
            mode="lines",
            line=dict(color="green", width=2, dash="dash"),
            name="knee line"
        )
    )
        fig.update_layout(
            title="Knee/Elbow(s) in Your Data",
            title_x=0.5,
            xaxis_title="k-value",
            yaxis_title="Silhoette Score",
        )
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="rgb(204, 204, 204)",
                linewidth=1,
                ticks="outside",
                tickfont=dict(
                    family="Arial",
                    size=12,
                    
                ),
            ),
            yaxis=dict(
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor="rgb(204, 204, 204)",
                linewidth=1,
                ticks="outside",
                tickfont=dict(
                    family="Arial",
                    size=12,
                    
                ),
            ),
            showlegend=True,
            #plot_bgcolor="yellow",
        )
        return fig

    
    #Elbow Method

    def elbow_method(self, k, data):
        ss = []
        for i in k:
            s = self.k_means_clust(i,data)
            ss.append(s)
        kneedle = KneeLocator(
            k, ss, 
            S = 1, 
            curve = 'concave', 
            direction = 'increasing', 
            interp_method = 'interp1d'
            )  
        return(kneedle,ss)
    
    #JNB

    def jnb_clustering(self, data, X):
        jnb = JenksNaturalBreaks()
        s = dict()
        for i in range(0,len(X)):

            #fit the model
            jnb.fit(data[:,i])
            
            # Silhouette Score
            s_score = silhouette_score(data, jnb.labels_, metric = 'euclidean')
            s[X[i]] = s_score
        
        
        return(sorted(s.items(), key=lambda kv: (kv[1], kv[0])))
    
    # all possible subsets
    def allPossibleSubsets(self, r, df:pd.DataFrame):

        sj =[(1,1)]
        for X in r:
            data = df[X].to_numpy()
            s = -1
            for i in range(2,8):
                sk = self.k_means_clust(i,data)
                if sk > s:
                    s = sk
            
            sj.append((X,s))
        return sj
    
