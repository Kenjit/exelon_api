
import Exelon
import yaml,fnmatch
import pandas as pd
from datetime import timedelta, datetime



def get_config():
    a_yaml_file = open("credentials.yaml")
    parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    return parsed_yaml_file["exelon_config"].get("api_key"), pd.to_datetime(parsed_yaml_file["exelon_config"].get("start_date"))

def scraper(): 
    api_key,begin= get_config()
    begin = pd.to_datetime(begin)
    end = datetime.today()- timedelta(days=1)
    months = int((end - begin)/pd.Timedelta(1, 'd'))
    print(end,begin)

    gen_data = pd.DataFrame()


    for i in range(months):
        start_date = begin 
        end_date = end
        temp = Exelon.get_generation_by_fuel(api_key,start_date,end_date)
        gen_data = pd.concat([gen_data, temp], sort = False)
    gen_data['INT'] = gen_data[fnmatch.filter(gen_data.columns, 'INT*')].sum(axis = 1)
    gen_data['HYDRO'] = gen_data[['NPSHYD', 'PS']].sum(axis = 1)
    gen_data['TOT'] = gen_data[['CCGT','OIL','COAL','NUCLEAR','WIND','HYDRO','BIOMASS','INT', 'SOLAR']].sum(axis = 1)
    gen_data = gen_data.resample('d', label='left').sum()
    
    return gen_data
       

        
    