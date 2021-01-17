import pandas as pd

sales_df = pd.read_csv('SalesData.csv')

# Display full information without truncation of columns
pd.set_option('display.max_columns', None)

# Inspect top 5 rows
print(sales_df.head())

# Inspect data type, null values and number of unique values for potential feature
print(sales_df.info())
print(sales_df.nunique())

# There are no null values so handling of null values part can be skipped.
#    Imputation could be done if there were null values

# From above results, Location, Locdesc and fiscal year has only one value.So, they can be used as meta data for
#    information rather than in analysis.

# Fiscal Season and SeasonDesc represents same data in different format. So one of them can be deleted

# Class desc has less unique values than Class. So, we can conclude that multiple classes have same descriptions
#    If case was opposite we could argue same class has multiple description which could also be due to typo
#    For now lets drop Class and use ClassDesc only since it has more unique values and data won't be lost

# Fiscal week and Day are date data values and loading them as date will help on using time related analysis
# Data can be treated as time-series data representing daily transactions. So, loading day as index helps in analysis

# Lets reload data considering above facts
sales_df = pd.read_csv('SalesData.csv', parse_dates=['Fiscal Week', 'Day'], index_col='Day',
                       usecols=['SeasonDesc', 'Fiscal Week', 'Day', 'Dayofweek', 'ClassDesc', 'SalesUnits',
                                'SalesDollars'])

# Lets find unique values of Season
print(sales_df.SeasonDesc.unique())

# Check if day and fiscal week represent same feature but with different time offset
print(set(sales_df.index - sales_df['Fiscal Week']))

# It had more unique values. So, daily or monthly transaction can depend on calender year or fiscal year

sales_fiscal_week_df = sales_df.reset_index(drop=True).set_index('Fiscal Week')
sales_fiscal_week_df.index.name = 'FiscalWeek'
print('Head data in fiscal week wise data')
print(sales_fiscal_week_df.head())

print('\nHead data in calender week wise data')
sales_calender_week_df = sales_df.drop(columns=['Fiscal Week'])
print(sales_calender_week_df.head())
