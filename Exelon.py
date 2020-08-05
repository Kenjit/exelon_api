from datetime import date, timedelta, datetime
import requests
import pandas as pd
from io import StringIO
    
    
        
    
def gen_url(api_key, report,start_date = '',end_date = '',period = '*', rtype = 0):
        server = 'https://api.bmreports.com/BMRS/'
        service = '&ServiceType=csv'
        api = '/V1?APIKey=' + api_key
        if rtype == 0:
            fdate = "&FromDate="
            tdate = "&ToDate="
            try: 
                start_date = start_date.strftime('%Y-%m-%d')
                end_date = end_date.strftime('%Y-%m-%d')
                url = server+report+api+fdate+start_date+tdate+end_date+service
            except:
                print('Date range not provided. Default data for yesterday and today ({} to {})'\
                      .format(date.today() - timedelta(days=1),date.today()))
                url = server+report+api+service
        elif rtype == 1:
            sdate = '&SettlementDate='
            speriod = '&Period='
            try: 
    	        start_date = start_date.strftime('%Y-%m-%d')
    	        url = server+report+api+sdate+start_date+speriod+period+service
            except:
                print('Date range not provided. Default data for latest period({} p {})'\
                      .format(date.today(), datetime.now().hour*2\
                      + int(datetime.now().minute/30)-1))
                url = server+report+api+service
        elif rtype == 2:
            fdate = "&FromSettlementDate="
            tdate = "&ToSettlementDate="
            speriod = '&Period='
            try: 
                start_date = start_date.strftime('%Y-%m-%d')
                end_date = end_date.strftime('%Y-%m-%d')
                url = server+report+api+fdate+start_date+tdate\
                		+end_date+speriod+period+service
            except:
                print('Date range not provided. Default data for yesterday and today ({} to {})'\
                      .format(date.today() - timedelta(days=1),date.today()))
                url = server+report+api+service
        elif rtype == 3:
            year = "&Year=" + str(start_date)
            try: 
                url = server+report+api+year+service
            except:
                print('Year not provided. Default data current year ({})'\
                      .format(date.today().year))
                url = server+report+api+service
        elif rtype == 4:
            sdate = '&SettlementDate='
            speriod = '&SettlementPeriod='
            try: 
                start_date = start_date.strftime('%Y-%m-%d')
                url = server+report+api+sdate+start_date+speriod+period+service
            except:
                print('Date range not provided. Default data for latest period({} p {})'\
                      .format(date.today(), datetime.now().hour*2\
                      + int(datetime.now().minute/30)-1))
                url = server+report+api+service
        return url
        
def get_generation_by_fuel(api_key, start_date='',end_date=''):
        rtype = 0
        report = 'FUELHH'
        names = ['Record Type', 'Settlement Date', 'Settlement Period',\
        		'CCGT', 'OIL', 'COAL', 'NUCLEAR', 'WIND', 'PS', 'NPSHYD',\
        		'OCGT', 'OTHER', 'INTFR', 'INTIRL', 'INTNED', 'INTEW',\
        		'BIOMASS', 'INTNEM']
        KEY = api_key
        url = gen_url(KEY, report,start_date,\
        				end_date, rtype = rtype)
        r = requests.get(url)
        data = pd.read_csv(StringIO(r.text), header=None,\
        					names = names, skiprows=1)
       
        solar = get_solar(start_date, end_date )
        # Format data
        data = data.iloc[:-1]

        data['Time'] = data['Settlement Period'].apply(lambda x:\
        								pd.Timedelta(str((x-1)*30)+' min'))

        data.index = pd.to_datetime(data['Settlement Date'],format = '%Y%m%d')

        data.drop(['Record Type', 'Time'], axis = 1, inplace = True)
        data['SOLAR'] = solar['SOLAR']
        return data
    
    
def get_solar(start_date = '', end_date = ''):
        sdate = start_date.strftime('%Y-%m-%dT%H:%M:%S')
        edate = end_date.strftime('%Y-%m-%dT%H:%M:%S')
        names = ['PES ID', 'DATETIME', 'SOLAR']
        url = 'https://api0.solar.sheffield.ac.uk/pvlive/v2?start='\
                + sdate +'&end=' + edate + '&data_format=csv'
        r = requests.get(url)
        data = pd.read_csv(StringIO(r.text), names = names, skiprows = 1)
        data.index = pd.to_datetime(data['DATETIME'])
        data.drop(['PES ID', 'DATETIME'], axis = 1, inplace = True)
        data['SOLAR'] = data['SOLAR']
        return data
    
    
