#!/usr/bin/env python
# coding: utf-8

# In[54]:


from sqlalchemy import create_engine
import sqlite3

from IPython.display import HTML
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import iplot

plotly.offline.init_notebook_mode(
    connected=True
)
pio.renderers.default = "jupyterlab"
# pio.renderers.default = "iframe"
# pio.renderers.default = "plotly_mimetype"


# In[2]:


# https://plotly.com/python/bar-charts/
# https://plotly.com/python/hover-text-and-formatting/
# https://plotly.com/python/figure-labels/
# https://plotly.com/python/styling-plotly-express/


# In[3]:


books = [
    "book1",
    "book2",
    "book3",
    "book4",
    "book5"
]

time = [
    6.7,
    14.5,
    10.2,
    8.0,
    8.9
]

df = pd.DataFrame({"book_name":books, "time":time})


# In[4]:


fig = go.Figure(
    [go.Bar(
        x=books,
        y=time
    )]
)

fig.show()


# In[5]:


fig = px.bar(
    df.sort_values(by="time", ascending=False),
    x="book_name",
    y="time",
    text_auto=True
)

fig.update_layout(
    # title="Plot Title",
    # xaxis_title="X Axis Title",
    # yaxis_title="Y Axis Title",
    # legend_title="Legend Title",
    font=dict(
        # family="Courier New, monospace",
        # family="Open Sans",
        size=18,
        color="limegreen"
    )
)

fig.update_traces(
    marker_color="yellow"
)

# fig.show()
# iplot(fig)
HTML(fig.to_html())


# ## Pre-processing raw data

# In[14]:


toggl_time_entries_df = pd.read_csv(
    filepath_or_buffer="Toggl_time_entries_2022-01-01_to_2022-12-23.csv"
)

toggl_time_entries_df["start_datetime"] = pd.to_datetime(
    toggl_time_entries_df["Start date"] + " " + toggl_time_entries_df["Start time"]
)
toggl_time_entries_df["end_datetime"] = pd.to_datetime(
    toggl_time_entries_df["End date"] + " " + toggl_time_entries_df["End time"]
)

toggl_time_entries_df["duration_secs"] = (toggl_time_entries_df["end_datetime"] - toggl_time_entries_df["start_datetime"]).astype("timedelta64[s]")
toggl_time_entries_df["duration_mins"] = toggl_time_entries_df["duration_secs"]/60
toggl_time_entries_df["duration_hours"] = toggl_time_entries_df["duration_secs"]/3600

toggl_time_entries_df["Start date"] = pd.to_datetime(toggl_time_entries_df["Start date"])
toggl_time_entries_df["year"] = toggl_time_entries_df["Start date"].dt.year


# In[15]:


toggl_time_entries_df.head()


# In[8]:


toggl_time_entries_df.info()


# ## Push raw data to sqlite db

# In[59]:


disk_engine = create_engine("sqlite:///test.db")
# price.to_sql('stock_price', disk_engine, if_exists='append')
toggl_time_entries_df.to_sql(
    name="toggl_raw",
    con=disk_engine,
    if_exists="replace",
    index=False
)


# ## Total time by year

# In[82]:


# Using sql
toggl_year_agg_sql = """
    SELECT
        year,
        SUM(duration_hours) AS duration_hours
    FROM
        toggl_raw
    GROUP BY
        year;
"""
toggl_year_agg_df = pd.read_sql(
    sql=toggl_year_agg_sql,
    con=disk_engine
)


# In[83]:


## Using pandas
# toggl_year_agg_df = toggl_time_entries_df.groupby(
#     ["year"]
# ).agg(
#     {"duration_secs": "sum"}
# ).reset_index()

# toggl_year_agg_df["duration_hours"] = (toggl_year_agg_df["duration_secs"]/3600).round(1)


# In[84]:


toggl_year_agg_df
# toggl_year_agg_df.duration_hours.to_list()[0]


# In[85]:


ind_val = toggl_year_agg_df.duration_hours.to_list()[0]
year_val = str(toggl_year_agg_df.year.to_list()[0])

year_ind_fig = go.Figure(
    go.Indicator(
        mode="number",
        value=ind_val,
        number = {
            "suffix": " hours"
        }
    )
)

year_ind_fig.update_layout(
    template = {
        "data" : {
            "indicator": [
                {
                    "title": {
                        "text": "Total Time Spent"
                    },
                    "mode" : "number+delta+gauge",
                    "delta" : {
                        "reference": 90
                    }
                }
            ]
                         
        }
    }
)

year_ind_fig.show()


# ## Number of books read

# In[86]:


# Using sql
# Note: this doesn't take into account if a book was actually finished
toggl_book_count_sql = """
    SELECT
        COUNT(DISTINCT Description) AS book_count
    FROM
        toggl_raw;
"""
toggl_book_count_df = pd.read_sql(
    sql=toggl_book_count_sql,
    con=disk_engine
)


# In[87]:


book_count_val = toggl_book_count_df.book_count.to_list()[0]

book_count_fig = go.Figure(
    go.Indicator(
        mode="number",
        value=book_count_val,
        # number = {
        #     "suffix": " books"
        # }
    )
)

book_count_fig.update_layout(
    template = {
        "data" : {
            "indicator": [
                {
                    "title": {
                        "text": "Total Books Read"
                    },
                    "mode" : "number+delta+gauge",
                    "delta" : {
                        "reference": 90
                    }
                }
            ]
                         
        }
    }
)

book_count_fig.show()


# ## Time by month

# In[102]:


# Using sql
toggl_month_agg_sql = """
    SELECT
        strftime('%Y%m', DATETIME("Start date")) AS yearmonth,
        SUM(duration_hours) AS duration_hours
    FROM
        toggl_raw
    GROUP BY
        strftime('%Y%m', "Start date");
"""

toggl_month_agg_df = pd.read_sql(
    sql=toggl_month_agg_sql,
    con=disk_engine
)

toggl_month_agg_df


# In[109]:


month_duration_fig = px.bar(
    toggl_month_agg_df.sort_values(by="yearmonth", ascending=True),
    x="yearmonth",
    y="duration_hours",
    text_auto=True,
    # orientation="h",
    hover_name="yearmonth",
    hover_data={
        # "yearmonth":False
    },
    labels={
        "duration_hours": "Duration (hrs)",
        "yearmonth": "Year Month"
    }
)

month_duration_fig.update_layout(
    title="Time Spent Per Month",
    # xaxis_title="X Axis Title",
    # yaxis_title="Y Axis Title",
    # legend_title="Legend Title",
    font={
        # family="Courier New, monospace",
        # family="Open Sans",
        # size=18,
        # color="limegreen"
    }
)

month_duration_fig.update_traces(
    textfont_size=12,
    textangle=0,
    textposition="outside",
    cliponaxis=False,
    # marker_color="green",
    marker_color="#3ba37c"
)

HTML(month_duration_fig.to_html())


# ## Time by book

# In[88]:


# Using sql
toggl_book_agg_sql = """
    SELECT
        Description,
        SUM(duration_hours) AS duration_hours
    FROM
        toggl_raw
    GROUP BY
        Description;
"""
toggl_book_agg_df = pd.read_sql(
    sql=toggl_book_agg_sql,
    con=disk_engine
)
toggl_book_agg_df["description_trunc"] = toggl_book_agg_df["Description"].str.slice(0, 20)

# d.loc[d.sales == 12, 'sales'] = 99
toggl_book_agg_df.loc[toggl_book_agg_df["description_trunc"].str.len() > 19, "description_trunc"] = toggl_book_agg_df["description_trunc"] + "..."


# In[89]:


# # Using pandas
# toggl_book_agg_df = toggl_time_entries_df.groupby(
#     ["Description"]
# ).agg(
#     {"duration_secs": "sum"}
# ).reset_index()

# toggl_book_agg_df["duration_hours"] = (toggl_book_agg_df["duration_secs"]/3600).round(1)
# toggl_book_agg_df["description_trunc"] = toggl_book_agg_df["Description"].str.slice(0, 20)

# # d.loc[d.sales == 12, 'sales'] = 99
# toggl_book_agg_df.loc[toggl_book_agg_df["description_trunc"].str.len() > 19, "description_trunc"] = toggl_book_agg_df["description_trunc"] + "..."


# In[90]:


fig = px.bar(
    toggl_book_agg_df.sort_values(by="duration_hours", ascending=True),
    x="duration_hours",
    y="description_trunc",
    text_auto=True,
    orientation="h",
    hover_name="Description",
    hover_data={
        "description_trunc":False
    },
    labels={
        "duration_hours": "Duration (hrs)",
        "description_trunc": "Book Name"
    }
)

fig.update_layout(
    # title="Plot Title",
    # xaxis_title="X Axis Title",
    # yaxis_title="Y Axis Title",
    # legend_title="Legend Title",
    font=dict(
        # family="Courier New, monospace",
        # family="Open Sans",
        # size=18,
        # color="limegreen"
    )
)

fig.update_traces(
    textfont_size=12,
    textangle=0,
    textposition="outside",
    cliponaxis=False,
    # marker_color="green",
    marker_color="#3ba37c"
)

HTML(fig.to_html())


# In[97]:


# sql = "select datetime(strftime('%Y-%m-%dT%H:00:00', 'now'));"
sql = "select strftime('%Y%m', 'now');"
# sql = "select 
pd.read_sql(
    sql=sql,
    con=disk_engine
)


# In[ ]:




