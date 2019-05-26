from pytrends.request import TrendReq

pytrend = TrendReq(hl='en-US', tz=360)

kw_list = ["Sumsung"] 

pytrend.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='', gprop='')

# Interest Over Time
interest_over_time_df = pytrend.interest_over_time()
print(interest_over_time_df.tail())

tt = pytrend.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)

print(tt)

# Interest by Region
#interest_by_region_df = pytrend.interest_by_region()
#print(interest_by_region_df.tail())

# Related Queries, returns a dictionary of dataframes
#related_queries_dict = pytrend.related_queries()
#print(related_queries_dict)

# Get Google Hot Trends data
#trending_searches_df = pytrend.trending_searches()
#print(trending_searches_df.head())

# Get Google Top Charts
#top_charts_df = pytrend.top_charts(cid='actors', date=201611)
#print(top_charts_df.head())

# Get Google Keyword Suggestions
#suggestions_dict = pytrend.suggestions(keyword='sumsung')
#print(suggestions_dict)

