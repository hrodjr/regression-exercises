import pandas as pd
import env

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

#zillow db
zillow_sql = "SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips\
    FROM properties_2017\
        JOIN propertylandusetype USING (propertylandusetypeid)\
            WHERE propertylandusetype.propertylandusetypeid LIKE '261';"

def get_zillow_data():
    return pd.read_sql(zillow_sql,get_connection('zillow'))

#Wrangle zillow dataset
def wrangle_zillow():
    ''' Brief description of wrangle function'''
    
    return df