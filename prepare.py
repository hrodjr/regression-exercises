import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split


def clean_data(df):

#drop duplicates   
    df = df.drop_duplicates()
#replaces empty values with 0
    df = df.replace({'total_charges': ' '}, 0)#total_charges/tenure
#drop redundant columns.
#I dropped after reviewing the initial visualization with the understanding that I would be encoding "types" later in the pipeline.
#Dropped paperless_billing because I felt it did not have an impact on churn.
    df = df.drop(['payment_type_id', 'internet_service_type_id', 'contract_type_id', 'customer_id', 'paperless_billing'], axis = 1)
#change from object to float
    df['total_charges'] = df['total_charges'].astype(float)
#Replaces 'no ... service' with 'No' for encoding. Customer can not have streaming or security services without internet. 
    df = df.replace(to_replace = 'No internet service', value = 'No')
    df = df.replace(to_replace = 'No phone service', value = 'No')

#encode by creating a dummy df.
#get_dummies creates a seperate df of booleans for the identified columns below. Cleaning for the decission tree.
    dummy_df = pd.get_dummies(df[[
    'churn',
    'gender',
    'senior_citizen',
    'partner',
    'dependents',
    'phone_service',
    'multiple_lines',
    'online_security',
    'online_backup',
    'device_protection',
    'tech_support',
    'streaming_tv',
    'streaming_movies']], dummy_na=False, drop_first=[True, True])

#set 'drop_first' to 'False' to encode multiple types of the below listed columns.
    dummy_df_types = pd.get_dummies(df[['payment_type','internet_service_type','contract_type']], dummy_na=False, drop_first=False)
    
#drop encoded columns.   
    df = df.drop(columns=[
    'churn',
    'payment_type',
    'internet_service_type',
    'contract_type',
    'gender',
    'senior_citizen',
    'partner',
    'dependents',
    'phone_service',
    'multiple_lines',
    'online_security',
    'online_backup',
    'device_protection',
    'tech_support',
    'streaming_tv',
    'streaming_movies'])

#...and concatanate the dummies df with the prep's df.
    df = pd.concat([df, dummy_df_types, dummy_df], axis=1)

#rename columns newly encoded columns
    df = df.rename(columns={
    'churn_Yes':'churned',
    'payment_type_Bank transfer (automatic)':'bank_transfer',
    'payment_type_Credit card (automatic)':'credit_card',
    'payment_type_Electronic check':'e_check',
    'payment_type_Mailed check':'check',
    'internet_service_type_DSL':'dsl',
    'internet_service_type_Fiber optic':'fiber',
    'internet_service_type_None':'no_internet',
    'contract_type_Month-to-month':'m2m',
    'contract_type_One year':'one_year_contract',
    'contract_type_Two year':'two_year_contract',
    'senior_citizen':'is_senior',
    'gender_Male':'is_male',
    'partner_Yes':'partner',
    'dependents_Yes':'dependents',
    'phone_service_Yes':'phone_service',
    'multiple_lines_Yes':'multiple_lines',
    'online_security_Yes':'online_security',
    'online_backup_Yes':'online_backup',
    'device_protection_Yes':'device_protection',
    'tech_support_Yes':'tech_support',
    'streaming_tv_Yes':'streaming_tv',
    'streaming_movies_Yes':'streaming_movies'})

#I decided change the following variables into single features.
    df['autopayment'] = df['bank_transfer'] + df['credit_card']

#added 'partner' and 'dependents' together, converted it to boolean then back into int64 as 'not_single'. This column
#will help with the hypothesis of whether or not churn is dependent on singles or not.
    df['partnered']=df['partner'] + df['dependents']
    df['bool'] = df['partnered'].astype('bool')
    df['not_single'] = df['bool'].astype('int64')

#drop original of new features.
#removed total charges. The focus here is on how monthly charges may or may no affect churn rates.
    df = df.drop(columns=['bank_transfer', 'credit_card', 'e_check', 'check', 'one_year_contract', 'two_year_contract', 'no_internet', 'dsl', 'total_charges', 'partner', 'dependents', 'partnered', 'bool'])

#dropped the following columns after running univariate and bivariate statistics
    df = df.drop(columns=['is_male', 'multiple_lines', 'streaming_tv', 'streaming_movies'])
#convert uint8 to int64 for uniformity.
    df = df.astype({
    'fiber':'int64',
    'm2m':'int64',
    'churned':'int64',
    'phone_service':'int64',
    'online_security':'int64',
    'online_backup':'int64',
    'device_protection':'int64',
    'tech_support':'int64',
    'autopayment':'int64'})

    return df


############################### Split Data ##################################

def train_validate_test_split(df, target, seed=123):
    '''
    This function takes in a dataframe, the name of the target variable
    (for stratification purposes), and an integer for a setting a seed
    and splits the data into train, validate and test. 
    Test is 20% of the original dataset, validate is .30*.80= 24% of the 
    original dataset, and train is .70*.80= 56% of the original dataset. 
    The function returns, in this order, train, validate and test dataframes. 
    '''
    
    train_validate, test = train_test_split(df, test_size=0.2, random_state=seed, stratify=df[target])
    train, validate = train_test_split(train_validate, test_size=0.3, random_state=seed, stratify=train_validate[target])
    return train, validate, test