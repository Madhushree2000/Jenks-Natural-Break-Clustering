import pandas as pd

class pre_process:
    def cat_threshold(self, th, df:pd.DataFrame):
        X =[]
        Y =[]
        for i in df.columns:
            z = df[i].unique()
            if(len(z) > th):
                X.append(i)
            else:
                Y.append(i)

        return(X,Y)
    
    def sort(self, arr):
        h = [0,0]
        for i in arr:
            if(h[1]<i[1]):
                h = i
        return h

    
