#code string to plot a multitrace graps based on dropdown

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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

def fiile_read(blob_name):
    #reading the file from azure blob storage container
    logger.info(f"Read dataset file: {blob_name}")
    try:
        from azure.storage.blob import BlockBlobService
        sas_token = '?sv=2021-04-10&st=2022-12-22T08%3A12%3A47Z&se=2023-12-30T08%3A12%3A00Z&sr=c&sp=racwl&sig=fMeYkXsCvwK%2F0qVrCmj2j3NiMricQjOPWOkAEXekIPA%3D'
        account_name = 'willbedeletedsoon'
        container_name = 'codx-pede-s02'
        #blob_name = 'cost-of-living_v2_I0869'
        def get_data_from_blob(sas_token, account_name, container_name, blob_name):
            block_blob_service = BlockBlobService(account_name=account_name, sas_token= sas_token)
            from_blob = block_blob_service.get_blob_to_text(container_name = container_name, blob_name=blob_name)
            return pd.read_csv(StringIO(from_blob.content))
        input_df=get_data_from_blob(sas_token, account_name, container_name, blob_name)
        #filtering out empty columns
        input_df = input_df[input_df.x2.notnull()]
        input_df = input_df[input_df.x23.notnull()]
        input_df = input_df[input_df.x33.notnull()]
        input_df = input_df[input_df.x54.notnull()]
        data_good = input_df[input_df["data_quality"] == 1]
        
        ##print(data_good)
        return(input_df)
    except Exception as error_msg:
        logger.info(f"Exception occured while reading the dataset: {blob_name}"
                    f"Error Info is  {error_msg}")

def getGraph():
    logger.info(
        "Preparing scatter plot json to understand relation between x and y values")
    # load dataset
    #df = pd.DataFrame(np.random.randint(0,100,size=(100, 2)), columns=list('XY'))
    #df = df.assign(Y = lambda x: (x['X']**2))
    #df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv")
    input_df=fiile_read("cost-of-living_v2_I0869.csv")
        #filtering out empty columns
    df = input_df[input_df["data_quality"] == 1].groupby(['city'])
    df = input_df[input_df["country"] == 'India']
    #print(df)
    # create figure
    fig = go.Figure()

    # Add surface trace
    fig.add_trace(go.Surface(  x=df.city,y=df.x54, colorscale="Viridis"))

    # Update plot sizing
    # fig.update_layout(
    #     width=800,
    #     height=900,
    #     autosize=False,
    #     margin=dict(t=0, b=0, l=0, r=0),
    #     template="plotly_white",
    # )

    # Update 3D scene options
    # fig.update_scenes(
    #     aspectratio=dict(x=1, y=1, z=0.7),
    #     aspectmode="manual"
    # )

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["type", "bar"],
                        label="bar",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "scatter"],
                        label="scatter",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "violin"],
                        label="violin",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "column"],
                        label="column",
                        method="restyle"
                    ),
                    dict(
                        args=["type", "box"],
                        label="box",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="Trace type:", showarrow=False,
            x=0, y=1.085, yref="paper", align="left")
        ]
    )

    fig.show()
    return io.to_json(fig)

dynamic_outputs = getGraph()