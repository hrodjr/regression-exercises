import matplotlib.pyplot as plt
import seaborn as sns
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


#Distributions. Gets histographs of acquired continuous variables (non-categorical - object)
def get_hist(df):
    ''' Gets histographs of acquired continuous variables'''
    
    plt.figure(figsize=(16, 3))

    # List of columns
    cols = [col for col in df.columns if col not in ['county_codes', 'year']]

    for i, col in enumerate(cols):

        # i starts at 0, but plot nos should start at 1
        plot_number = i + 1 

        # Create subplot.
        plt.subplot(1, len(cols), plot_number)

        # Title with column name.
        plt.title(col)

        # Display histogram for column.
        df[col].hist(bins=5)

        # Hide gridlines.
        plt.grid(False)

        # turn off scientific notation
        plt.ticklabel_format(useOffset=False)

        plt.tight_layout()

    plt.show()

#Gets box plots of acquired continuous variables (non-categorical - object)
def get_box(df):
    ''' Gets boxplots of acquired continuous variables'''
    
    # List of columns
    cols = ['bedrooms', 'bathrooms', 'square_feet', 'tax_value']

    plt.figure(figsize=(16, 3))

    for i, col in enumerate(cols):

        # i starts at 0, but plot should start at 1
        plot_number = i + 1 

        # Create subplot.
        plt.subplot(1, len(cols), plot_number)

        # Title with column name.
        plt.title(col)

        # Display boxplot for column.
        sns.boxplot(data=df[[col]])

        # Hide gridlines.
        plt.grid(False)

        # sets proper spacing between plots
        plt.tight_layout()

    plt.show()   

#removes identified outliers 
def remove_outliers(df, k , col_list):
    ''' remove outliers from a list of columns in a dataframe 
        and return that dataframe. Much like the word “software”, John Tukey is responsible for creating this “rule” called the 
        Inter-Quartile Range rule. In the absence of a domain knowledge reason for removing certain outliers, this is a pretty 
        robust tool for removing the most extreme outliers (with Zillow data, we can feel confident using this, since Zillow markets 
        to the majority of the bell curve and not folks w/ $20mil properties). the value for k is a constant that sets the threshold.
        Usually, you’ll see k start at 1.5, or 3 or less, depending on how many outliers you want to keep. The higher the k, the more 
        outliers you keep. Recommend not going beneath 1.5, but this is worth using, especially with data w/ extreme high/low values.'''
    
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df

#Wrangle zillow dataset
def prepare_zillow(df):
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
#converts year built and fips 'county_codes' to object as they are categories
    convert_dict = {'yearbuilt': object, 'fips': object}
    df = df.astype(convert_dict)
#rename columns
    df = df.rename(columns={"bedroomcnt": "bedrooms", "bathroomcnt": "bathrooms", "calculatedfinishedsquarefeet":"square_feet",
                  "taxvaluedollarcnt":"tax_value", "yearbuilt":"year", "taxamount":"tax_amount", "fips":"county_codes"})

# drop taxamount
    df = df.drop(columns = 'tax_amount')

#removes outliers with k values and column features
    df = remove_outliers(df, 1.5, ['bedrooms', 'bathrooms', 'tax_value', 'square_feet'])

#gets graphs
    get_hist(df)
    get_box(df)
##For later
#train[['year']] = imputer.transform(train[['year']])
#validate[['year']] = imputer.transform(validate[['year']])
#test[['year']] = imputer.transform(test[['year']])      

    df.head()
    

    return df

##########Final wrangle function################
def wrangle_zillow():
    prepared_zillow_data = prepare_zillow(get_zillow_data())

    return prepared_zillow_data
