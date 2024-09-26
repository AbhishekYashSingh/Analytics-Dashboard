import pandas as pd
import streamlit as st
import plotly.express as px

df_original=pd.read_csv("correct_twitter_201904.tsv",sep='\t',low_memory=False)
df=pd.DataFrame()

df['date'] = pd.to_datetime(df_original[' ts2'], errors='coerce')
#df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
df['like_count'] = pd.to_numeric(df_original['like_count'], errors='coerce')

# Convert 'time' to datetime time format
df['time'] = pd.to_datetime(df_original[' ts2'], format='%H:%M', errors='coerce').dt.time
df['id']=df_original['id']
df['place_id']=df_original['place_id']
df['text']=df_original['text']

st.title('Tweet Analysis Dashboard')

# Search box
search_term = st.text_input("Search for a keyword in tweets:", "")

# Filter DataFrame based on the search term
filtered_df = df[df['text'].str.contains(search_term, case=False)]
print(filtered_df.columns)
# Display some stats and results
if not filtered_df.empty:

    # Graph 1: Number of tweets per day
    tweets_per_day = filtered_df.groupby(filtered_df['date'].dt.date).size().reset_index(name='Tweet Count')
    st.subheader(f"Number of Tweets containing '{search_term}' per day")
    fig1 = px.line(tweets_per_day, x='date', y='Tweet Count', title="Tweets Over Time")
    st.plotly_chart(fig1)

    # Graph 2: Unique users posting tweets
    unique_users = filtered_df.groupby('date')['id'].nunique().reset_index(name='Unique Users')
    st.subheader(f"Number of Unique Users posting '{search_term}' per day")
    fig2 = px.bar(unique_users, x='date', y='Unique Users', title="Unique Users Per Day")
    st.plotly_chart(fig2)

    # Graph 3: Average likes per tweet
    avg_likes = filtered_df.groupby('date')['like_count'].mean().reset_index(name='Average Likes')
    st.subheader(f"Average Likes for Tweets containing '{search_term}' per day")
    fig3 = px.line(avg_likes, x='date', y='Average Likes', title="Average Likes Over Time")
    st.plotly_chart(fig3)

    # Graph 4: Tweets by place
    place_tweets = filtered_df.groupby('place_id').size().reset_index(name='Tweet Count')
    st.subheader(f"Tweets containing '{search_term}' by Place")
    fig4 = px.bar(place_tweets, x='place_id', y='Tweet Count', title="Tweets by Place")
    st.plotly_chart(fig4)

    # Graph 5: Tweets by time of day
    filtered_df['time'] = pd.to_datetime(filtered_df['time'], format='%H:%M').dt.hour
    tweets_by_time = filtered_df.groupby('time').size().reset_index(name='Tweet Count')
    st.subheader(f"Tweets containing '{search_term}' by Time of Day")
    fig5 = px.line(tweets_by_time, x='time', y='Tweet Count', title="Tweets by Time of Day")
    st.plotly_chart(fig5)

    # Find the user who posted the most tweets
    top_user = filtered_df['id'].value_counts().idxmax()
    st.subheader(f"The user who posted the most tweets containing '{search_term}' is: {top_user}")

else:
    st.write("No tweets found containing the search term.")

