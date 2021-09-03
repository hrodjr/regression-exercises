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
def wrangle_zillow(df):
    ''' cleans and prepares zillow data'''
    df = df.drop_duplicates()
#replaces nulls with bedroomcnt mode
    df['bedroomcnt'] = df.bedroomcnt.fillna(value = 3)
#replaces nulls with bathroomcnt mode
    df['bathroomcnt'] = df.bathroomcnt.fillna(value = 2)
#replaces nulls with calculatedfinishedsquarefeet mean
    df['calculatedfinishedsquarefeet'] = df.calculatedfinishedsquarefeet.fillna(value = df['calculatedfinishedsquarefeet'].mean())
#replaces nulls with taxvaluedollarcnt mode
    df['taxvaluedollarcnt'] = df.taxvaluedollarcnt.fillna(value = 45000)
#replaces nulls with yearbuilt mode
    df['yearbuilt'] = df.yearbuilt.fillna(value = 1960)
 #replaces nulls with taxamount mean   
    df['taxamount'] = df.taxamount.fillna(value = df['taxamount'].mean())
#converts data type to int64 from float64
    df = df.astype('int64')
#rename columns
    df = df.rename(columns={"bedroomcnt": "bedrooms", "bathroomcnt": "bathrooms", "calculatedfinishedsquarefeet":"square_feet",
                  "taxvaluedollarcnt":"tax_value", "yearbuilt":"year", "taxamount":"tax_amount", "fips":"county_codes"})

    return df