import numpy as np
import pandas as pd


def create_incidents(M, N, filename):

    df = pd.DataFrame({'feature1':np.random.randint(M, size=(N,)),

                     'feature2':np.random.randint(M, size=(N,)),

                     'time':np.random.rand(N)

                     })
    try:
        df.to_csv(filename, index_label='id')
    except IOError:
        print('Could not write file:', filename)
        return

def create_incidents2(M, N, filename):

    df = pd.DataFrame({'feature1':np.random.randint(M, size=(N,)),

                     'feature2':np.random.randint(M, size=(N,)),

                     'time':0.0#np.random.rand(N)

                     })
    try:
        df.to_csv(filename, index_label='id')
    except IOError:
        print('Could not write file:', filename)
        return
