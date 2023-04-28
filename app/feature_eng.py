from sklearn import preprocessing

class feature_eng:
    def __init__(self) -> None:
        pass
    def Label(self, df):
        label_encoder = preprocessing.LabelEncoder()
        df = df.dropna() # drop nan values
        for col in df.columns:
            if(df[col].dtype == object):
                # Encode labels in column 
                df[col]= label_encoder.fit_transform(df[col])

        return(df)


