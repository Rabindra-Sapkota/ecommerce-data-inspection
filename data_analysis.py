import pandas as pd

pd.set_option('display.max_columns', None)

# Lets analyse data by calender week now. Impact of fiscal week can be done similarly
sales_calender_week_df = pd.read_csv('SalesData.csv', parse_dates=['Day'], index_col='Day',
                       usecols=['SeasonDesc', 'Day', 'Dayofweek', 'ClassDesc', 'SalesUnits',
                                'SalesDollars'])

print(sales_calender_week_df.head())

# Since whole data is for year 2016 lets modify value of season desc accordingly
sales_calender_week_df['SeasonDesc'] = sales_calender_week_df.SeasonDesc.apply(lambda x: 'Spring' if x == 'Spring 2016' else 'Fall')
print(sales_calender_week_df.head())

# Lets see if sales is influenced by day of week
sales_calender_week_df.groupby(['Dayofweek'])[['SalesUnits','SalesDollars']].sum().plot(kind='bar', subplots=True, rot=0)

# Company has relatives higher sales in terms of unit and amount on saturday and friday
# Sales is lower on monday. So company can make decision on stock of product
# Account can make decision relatively with this insight
# For stock we can drill down if any particular product has higher sell or only all products

# Lets view series with daily total sales
sales_calender_week_df.SalesDollars.resample('D').sum().plot()

# Graph is irregular with spikes at regular interval.
# This indicates sales on particular day of month is higher than other month
# Lets visualize it too
sales_calender_week_df.SalesDollars.resample('W').sum().plot(title='Trend of total Sales Per Week')
sales_calender_week_df.SalesDollars.resample('M').sum().plot(title='Trend of total Sales Per Month')
sales_calender_week_df.groupby(sales_calender_week_df.index.day)['SalesDollars'].sum().plot(grid=True, title='Sales Vs Day of month')
# Plot indicated that sales is at peak around 24th. It gets to start around 21 and settles around 26

# Graph indicates monthly sales has been increased in month from januaury to march
# For january we only had partial data. For it is actually increased in greater amount from february
# Knowing reason of boost that cause rise in sales can be implemented later to increase sales

sales_calender_week_df.groupby(['SeasonDesc'])['SalesUnits', 'SalesDollars'].sum().plot(kind='bar', subplots=True, rot=0)
# Higher sales on spring than fall. Can drill down to see if it is actually due to some season specific products

# Find Seasonal and overgreen products
seasonal_analysis_df = sales_calender_week_df.pivot_table(index=['ClassDesc'], columns=['SeasonDesc'], values=['SalesUnits'], aggfunc='sum', fill_value=0)
seasonal_analysis_df.columns = ['_'.join(col) for col in seasonal_analysis_df.columns]
seasonal_analysis_df['SalesDiff'] = abs(seasonal_analysis_df.SalesUnits_Fall - seasonal_analysis_df.SalesUnits_Spring)
seasonal_analysis_df['SalesDiffPer'] = seasonal_analysis_df.SalesDiff / (seasonal_analysis_df.SalesUnits_Fall + seasonal_analysis_df.SalesUnits_Spring) * 100

print('Evergreen Products')
print(seasonal_analysis_df[seasonal_analysis_df.SalesDiffPer <= 40])

print('Seasonal Products')
print(seasonal_analysis_df[seasonal_analysis_df.SalesDiffPer > 40])

# Based on result we have to make stock of product accordingly
# Get top 10 product for each month
sales_month = sales_calender_week_df.groupby([sales_calender_week_df.index.month, 'ClassDesc'])[['SalesDollars']].sum().sort_values(['Day','SalesDollars'], ascending=[True, False])
top_for_product = sales_month.groupby('Day').head(30).reset_index()

top_for_product['Day'] = pd.to_datetime(top_for_product.Day, format='%m').dt.month_name()
print(top_for_product)
