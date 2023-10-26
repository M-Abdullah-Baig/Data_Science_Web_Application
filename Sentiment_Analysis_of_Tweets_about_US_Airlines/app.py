
import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

DATA_URL = ("C:\\Users\\DELL\\Desktop\\Projects\\Coursera\\Data_Science\\Sentiment_Analysis_of_Tweets_about_US_Airlines\\tweets_data.csv")

#@st.cache_data(persist=True)   # If input function does not change, your app use the cache data instead of using data loading over and over again
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])   # To make a standardize format of pandas datetime 
    return data

data = load_data()
   
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))   # add user options

# Every time it gives random tweet when you selected options, as seed is not fixed 
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])  # return only 1 random tweet at a time and its place is 0th row and 0th column

st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox("Visualization type", ["Histogram", "Pie chart"], key='1') # key is used to select the type multiple times and different between one or more widgets
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x = 'Sentiment', y = 'Tweets', color = 'Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = 'Tweets', names = 'Sentiment')
        st.plotly_chart(fig)
        

st.sidebar.subheader("When and where are users tweeting from ?")
hour = st.sidebar.number_input("Hour of day", min_value = 1, max_value = 24)
modified_data = data[data['tweet_created'].dt.hour == hour]             # data for 60 minutes and 1 hour
if not st.sidebar.checkbox("Close", True, key= '2'):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):        # This will update the dataframe with the relevant data
        st.write(modified_data)          

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick airlines", ("US Airways", "United", "American", "Southwest", "Delta"), key = '0')

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]   # This make the new data in which only selected airlines are present
    fig_choice = px.histogram(choice_data, x = 'airline', y = 'airline_sentiment', histfunc = 'count', color = 'airline_sentiment', 
            facet_col = 'airline_sentiment', labels = {'airline_sentiment' : 'tweets'}, height = 600, width = 800)
# facet_col = split the histogram by sentiment so that for each airiline we get three bar plots
    
    st.plotly_chart(fig_choice)
    
 
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display Word Cloud for what sentiment?", ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Close", True, key = '3'):
    st.header("Word Cloud for %s sentiment" % (word_sentiment))
    df = data[data['airline_sentiment'] == word_sentiment]             # subset the data
    words = ' '.join(df['text'])
    
    # Process of words that take only tweets text, eliminate URLs, links from them
    processed_words = ' '.join([word for word in words.split() if 'https' not in word and not word.startswith('@') and word != 'RT'])
    
    # STOPWORDS removing the common words like articles and punctuations that don't factor in and didin't bias our 
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color = 'white', height = 640, width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(plt)
