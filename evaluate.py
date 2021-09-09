import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from seaborn.regression import residplot
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import f_regression 
from math import sqrt

#gets the baseline
def get_baseline(df, x, y):
    df['yhat_baseline'] = y.mean()
    model = LinearRegression().fit(x, y)
    df['yhat'] = model.predict(x)
    return df

#gets residuals
def get_residuals(df, y):
    df['residual'] = df['yhat'] - y
    df['residual_baseline'] = df['yhat_baseline'] - y
    return df

#creates a residual plot
def plot_residual(df, x, y):
    sns.residplot(x, y)
    plt.show()

#returns regression errors
def regression_errors(df, y, yhat):
    MSE2 = mean_squared_error(y, yhat)
    SSE2 = MSE2 * len(df)
    ESS = sum((yhat - y.mean())**2)
    TSS = ESS + SSE2
    RMSE2 = mean_squared_error(y, yhat, squared = False)
    return (MSE2, SSE2, ESS, TSS, RMSE2)

#computes the SSE, MSE, and RMSE for the baseline model
def baseline_mean_errors(df, y, yhat_baseline):
    MSE2_baseline = mean_squared_error(y, yhat_baseline)
    SSE2_baseline = MSE2_baseline * len(df)
    RMSE2_baseline = mean_squared_error(y, yhat_baseline, squared=False)
    
    return MSE2_baseline, SSE2_baseline, RMSE2_baseline

#returns true if your model performs better than the baseline, otherwise false
def better_than_baseline(regression_errors = True, baseline_mean_errors = True):
    
    if regression_errors - baseline_mean_errors <  regression_errors:
        print('The model is better then the baseline.')
    else:
        print('The model is not better then the baseline.')
