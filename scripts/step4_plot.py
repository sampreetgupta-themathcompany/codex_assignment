# code string to showw a plot of y=x^2
import numpy as np
import pandas as pd
import plotly.express as px
import pandas as pd
import json
from io import StringIO
import plotly.io as io
from plotly.io import to_json




def getLogger():
    import logging
    logging.basicConfig(filename="UIACLogger.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger


logger = getLogger()



def getGraph():
    logger.info(
        "Preparing scatter plot json to understand relation between x and y values")
    df = pd.DataFrame(np.random.randint(0,100,size=(100, 1)), columns=list('X'))
    df = df.assign(Y = lambda x: (x['X']**2))
    fig = px.scatter(df, y='Y', x='X')
    fig.show()
    return io.to_json(fig)
dynamic_outputs = getGraph()
#print(df)