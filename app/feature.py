import pandas as pd
import numpy as np

class feature_matrix:
    def __init__(self) -> None:
        pass

    def printPowerSet(self, arr):
        x = []
        y = []
        n = len(arr)
        # Function to find all subsets of given set.
        # Any repeated subset is considered only
        # once in the output
        _list = []
    
        # Run counter i from 000..0 to 111..1
        for i in range(2**n):
            subset = ""
    
            # consider each element in the set
            for j in range(n):
    
                # Check if jth bit in the i is set.
                # If the bit is set, we consider
                # jth element from set
                if (i & (1 << j)) != 0:
                    subset += str(arr[j]) + "|"
    
            # if subset is encountered for the first time
            # If we use set<string>, we can directly insert
            if subset not in _list and len(subset) > 0:
                _list.append(subset)
    
        # consider every subset
        for subset in _list:
    
            # split the subset and print its elements
            arr = subset.split('|')
            for string in arr:
                
                x.append(string)
            
            y.append(x[:-1])
            x = []
        return y

    def list_convertor(self, l):
        output =[]
        s = ""
        for i in l:
            s = ""
            for j in i:
                s = s+j+"-"
            output.append(s[:-1])
            
        return(output)
    
    def matrix(self, X, sj):
        feature_matrix=[]

        # finding number of rows and columns in the feature matrix
        num = len(X)
        if num%2!=0: #if odd number of features
            c = (num+1)//2
            r = (num-1)//2

        else: # else even number of features
            c = num//2
            r = num//2

        num_col = int(2**c)
        num_row = int(2**r)

        col_list = [['1']]
        col_list = col_list+ (self.printPowerSet(X[0:c]))

        row_list = [['1']]
        row_list = row_list+ (self.printPowerSet(X[c:num]))

        col_list = self.list_convertor(col_list)
        row_list = self.list_convertor(row_list)



        f=0
        for i in range(0,num_row):
            row = []
            for j in range(0,num_col):
                huss =sj[f]
                row.append(huss[1])
                f+=1
            feature_matrix.append(row)

        feature_matrix = np.array(feature_matrix)
        data = pd.DataFrame(data = feature_matrix, 
                  index = row_list, 
                  columns = col_list)
        return data




