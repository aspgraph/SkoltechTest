import numpy as np
import pandas as pd


def create_incidents(M, N, filename):
    """
    Создать файл "инцидентов"
    :arg M: Число возможных значений вариаций "feature1" и "feature2"
    :arg N: Число "инцидентов"
    :arg filename: Файл для сохранения "инцидентов"
    :type M: int
    :type N: int
    :type filename: str
    """
    df = pd.DataFrame({'feature1':np.random.randint(M, size=(N,)),

                     'feature2':np.random.randint(M, size=(N,)),

                     'time':np.random.rand(N)

                     })
    try:
        df.to_csv(filename, index_label='id')
    except IOError:
        print('Could not write file:', filename)
        return
