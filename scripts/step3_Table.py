# Below codestring is used to display the grid table that consists of cost of basic ammenities.

import pandas as pd
import json
from io import StringIO


def getLogger():
    import logging
    logging.basicConfig(filename="UIACLogger.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger


logger = getLogger()


def file_read(blob_name):
    #reading the file from azure blob storage container
    logger.info(f"Read dataset file: {blob_name}")
    try:
        from azure.storage.blob import BlockBlobService
        sas_token = '?sv=2021-04-10&st=2022-12-22T08%3A12%3A47Z&se=2023-12-30T08%3A12%3A00Z&sr=c&sp=racwl&sig=fMeYkXsCvwK%2F0qVrCmj2j3NiMricQjOPWOkAEXekIPA%3D'
        account_name = 'willbedeletedsoon'
        container_name = 'codx-pede-s02'
        #blob_name = 'cost-of-living_v2_I0869' fiile_read("cost-of-living_v2_I0869")
        def get_data_from_blob(sas_token, account_name, container_name, blob_name):
            block_blob_service = BlockBlobService(account_name=account_name, sas_token= sas_token)
            from_blob = block_blob_service.get_blob_to_text(container_name = container_name, blob_name=blob_name)
            return pd.read_csv(StringIO(from_blob.content))
        input_df=get_data_from_blob(sas_token, account_name, container_name, blob_name)
        #filtering out empty columns
        input_df = input_df[input_df.x2.notnull()]
        input_df = input_df[input_df.x8.notnull()]
        input_df = input_df[input_df.x33.notnull()]
        input_df = input_df[input_df.x54.notnull()]
        input_df = input_df[input_df.x48.notnull()]
        input_df = input_df[input_df.x37.notnull()]
        input_df = input_df[input_df.x36.notnull()]
        data_good = input_df[input_df["data_quality"] == 1]
        
        #print(data_good)
        return(data_good)
    except Exception as error_msg:
        logger.info(f"Exception occured while reading the dataset: {blob_name}"
                    f"Error Info is  {error_msg}")


def get_filter_table(dframe, selected_filters):
    logger.info("Applying screen filters on the grid table dframe.")
    select_df = dframe.copy()
    for item in list(selected_filters):
        if isinstance(selected_filters[item], list):
            if 'All' not in selected_filters[item] and selected_filters[item]:
                select_df = select_df[select_df[item].isin(
                    selected_filters[item])]
        else:
            if selected_filters[item] != 'All':
                select_df = select_df[select_df[item]
                                      == selected_filters[item]]
    logger.info("Successfully applied screen filters on the grid table dframe.")
    return select_df


def generate_dynamic_table(dframe, name='Sales', grid_options={"tableSize": "small", "tableMaxHeight": "80vh", "quickSearch":True}, group_headers=[], grid="auto"):
    logger.info("Generate dynamic Grid table json from dframe")
    table_dict = {}
    table_props = {}
    table_dict.update({"grid": grid, "type": "tabularForm",
                      "noGutterBottom": True, 'name': name})
    values_dict = dframe.dropna(axis=1).to_dict("records")
    table_dict.update({"value": values_dict})
    col_def_list = []
    for col in list(dframe.columns):
        col_def_dict = {}
        col_def_dict.update({"headerName": col, "field": col})
        col_def_list.append(col_def_dict)
    table_props["groupHeaders"] = group_headers
    table_props["coldef"] = col_def_list
    table_props["gridOptions"] = grid_options
    table_dict.update({"tableprops": table_props})
    logger.info("Successfully generated dynamic Grid table json from dframe")
    return table_dict


def build_grid_table_json():
    logger.info("Preparing grid table json for Colour Screen")
    form_config = {}
    dframe = file_read("cost-of-living_v2_I0869.csv")
    dframe=dframe[['country','city','x48', 'x41', 'x36', 'x8']] #--here281222 --5 columns
    dframe.columns = dframe.columns.str.replace('x48', 'Apartment')
    dframe.columns = dframe.columns.str.replace('x41', 'Movie Ticket')
    dframe.columns = dframe.columns.str.replace('x36', 'Basic cost')
    dframe.columns = dframe.columns.str.replace('x8', 'Water')
    
    selected_filters = {"country": ['India','United States']}
    
    dframe2 = get_filter_table(dframe, selected_filters)
    form_config['fields'] = [generate_dynamic_table(dframe2)]
    grid_table_json = {}
    grid_table_json['form_config'] = form_config
    logger.info("Successfully prepared grid table json for Colour Screen")
    return grid_table_json


grid_table_json = build_grid_table_json()
dynamic_outputs = json.dumps(grid_table_json)