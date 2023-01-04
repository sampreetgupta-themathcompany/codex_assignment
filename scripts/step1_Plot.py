# Below codestring is used to create a plot to show basic ammenities cost across countries.
import plotly.express as px
import pandas as pd
import json
from io import StringIO
import plotly.io as io


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


def getGraph(dframe, filters):
    logger.info(
        "Preparing bar graph json to understand basic_expenditure across all countries")
    column_names = ['x48', 'x38', 'x37', 'x36', 'x33', 'x8', 'x29']
    #print(dframe['country'])
    data_good = dframe[dframe["data_quality"] == 1]
    data_good['basic_expenditure']= data_good[column_names].sum(axis=1)
    for item in filters:
        if 'All' in filters[item]:
            continue
        elif isinstance(filters[item], list):
            data_good = data_good[data_good[item].isin(filters[item])]
        else:
            data_good = data_good[data_good[item] == filters[item]]
    fig = px.bar(data_good, x='x48', y='country', color='basic_expenditure')
    #fig.show()
    logger.info(
        "Successfully prepared bar graph json to understand basic_expenditure across all countries")
    return io.to_json(fig)


selected_filters = {"country": ['India','China','Russia']}
dframe = fiile_read("cost-of-living_v2_I0869.csv")
#dframe = dframe.groupby(['country'])
dynamic_outputs = getGraph(dframe, selected_filters)#here11