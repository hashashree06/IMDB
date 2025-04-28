import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import mysql.connector

# Establishing SQL connection to TiDB
connection=mysql.connector.connect(host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",           
                              user="4TuZQhevixrKXDn.root",              
                              password="plut8plTY5XHB5ei",      
                              database="IMDB2",
                                ) 

cursor=connection.cursor()
cursor.execute("select MOVIE_NAME,RATING,VOTING_COUNT,DURATION,GENRE from movie_details")
results = cursor.fetchall()
columns = [i[0] for i in cursor.description]
df=pd.DataFrame(results,columns=columns)
df.rename(columns={'VOTING_COUNT': 'VOTING COUNT'}, inplace=True)
df.rename(columns={'MOVIE_NAME': 'MOVIE NAME'}, inplace=True)
# st.write(df.head(10))

# # reading the dataframe using pandas
# df=pd.read_csv("E:\merged_data_final.csv")


# sidebar for choosing between visualization and filtering option
var1=st.sidebar.selectbox("select an option",['Home','Interactive Visualization','Interactive Filtering Functionality'])

if var1== 'Home':
    # to display the title
    st.title('IMDB 2024 DATA SCRAPPING AND VISUALIZATION')
    # giving description
    st.write('Extracting and analysing movie data from IMDB for the year 2024')
    st.markdown("[clich here to proceed to IMDB SITE](https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31)")
    # to insert image
    st.image("https://cdn.prod.website-files.com/626fae216404de74c2539b98/633558f4ed4b31fead1f3382_8.png")

if var1== 'Interactive Visualization':
    option=st.sidebar.radio("choose an option",
                 ['Top 10 movies by Highest Rating and significant voting count',
                  'Genre Distribution',
                  'Average Duration of movies in each Genre',
                  'Voting Trends by genre',
                  'Rating Distribution',
                  'Genre-based Rating Leaders',
                  'Most popular generes by voting',
                  'Duration Extremes',
                  'Ratings by Genre',
                  'Correlation Analysis'])
     
    if option == 'Top 10 movies by Highest Rating and significant voting count':
        votes=50000
        df_voting_filtered=df[df['VOTING COUNT']>votes]
        # st.write(df_voting_filtered)
        rating = df_voting_filtered.sort_values(by=['RATING','VOTING COUNT'], ascending=[False,False]).head(10)
        st.write(rating)

        # rating=9
        # df_rating_filtered=df[df['RATING']>rating]
        # voting=df_rating_filtered.sort_values(by=['RATING','VOTING COUNT'],ascending=[False,False]).head(10)
        # st.write(voting)

    if option == 'Genre Distribution':
        #barchart showing count of movies in each genre
        fig,ax=plt.subplots()
        ax.set_title(f"Bar Chart:Genre Distribution")
        genre = df['GENRE'].value_counts()
        ax.bar(genre.index,genre.values, color='orchid')
        ax.set_xlabel("Genre")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    
    if option == 'Average Duration of movies in each Genre':
        genre_group=df.groupby('GENRE')['DURATION'].mean()
        st.write(genre_group)
        fig,ax=plt.subplots()
        ax.set_title(f"Horizontal Bar Chart:Average duration of movie in each genre")
        #genre = df['GENRE'].value_counts()
        ax.barh(genre_group.index,genre_group.values, color='green')
        ax.set_ylabel("Genre")
        ax.set_xlabel("Duration")
        st.pyplot(fig)

    if option =='Voting Trends by genre':
        genre_group=df.groupby('GENRE')['VOTING COUNT'].mean()
        st.write(genre_group)
        fig,ax=plt.subplots()
        ax.set_title(f"Horizontal bar Chart:Average voting across each genre")
        #genre = df['GENRE'].value_counts()
        ax.barh(genre_group.index,genre_group.values, color='red')
        ax.set_ylabel("Genre")
        ax.set_xlabel("Voting count")
        st.pyplot(fig)

    
    if option == 'Rating Distribution':
        fig,ax=plt.subplots()
        ax.set_title(f"histogram of movie rating")
        ax.hist(df['RATING'])
        ax.set_xlabel("rating")
        ax.set_ylabel("count")
        st.pyplot(fig)

    if option == 'Genre-based Rating Leaders':
        rating=9
        df_rating_filtered=df[df['RATING']>rating] #filtering dataframe by rating>9
        index_pulling=df_rating_filtered.groupby('GENRE')['RATING'].idxmax() #grouping according to genre and getting the index of the max rated movie
        movie_name_extraction=df.loc[index_pulling,['GENRE', 'MOVIE NAME', 'RATING']] #from the index(row) we are extracting genre,movie name,rating
        st.write(movie_name_extraction)
      
    
    if option == 'Most popular generes by voting':
        # max_vc = df.loc[df['VOTING COUNT'].idxmax(), ['GENRE', 'MOVIE NAME', 'VOTING COUNT']]
        # max_vc_df = pd.DataFrame([max_vc])
        # st.write(max_vc_df)
        genre_group = df.groupby('GENRE')['VOTING COUNT'].sum().reset_index()
        st.write(genre_group)
        fig= px.pie(genre_group, names='GENRE', values='VOTING COUNT')
        st.plotly_chart(fig)



    if option == 'Duration Extremes':
        min_dur=df.loc[df['DURATION'].idxmin(),['GENRE', 'MOVIE NAME','DURATION']]
        max_dur=df.loc[df['DURATION'].idxmax(),['GENRE', 'MOVIE NAME','DURATION']]
        st.write('shortest movie',min_dur)
        st.write('Longest movie',max_dur)

    if option == 'Ratings by Genre':
        avg_rating=df.groupby('GENRE')['RATING'].mean().reset_index() #if not given reset index , then avg rating will be series of data and not a dataframe
        #st.write(avg_rating)
        heatmap=avg_rating.pivot_table(index='GENRE',values='RATING') #pivot can be applied to a DF alone
        fig, ax = plt.subplots()
        sns.heatmap(heatmap, annot=True, cmap='coolwarm',ax=ax)
        st.pyplot(fig)

    if option == 'Correlation Analysis':
        fig,ax=plt.subplots()
        ax.set_title(f"Scatter  plot :relationship between rating and voting count")
        df.plot(kind = 'scatter', x = 'RATING', y = 'VOTING COUNT',ax=ax)
        st.pyplot(fig)

        
if var1=='Interactive Filtering Functionality':
    st.write("The Dashboard will visualize the inetractive fitering functionality in IMDB dataset")
    st.write("User can apply multiple filters simultaneously for customized insights")
    
    # Genre Filter
    genres = df['GENRE'].unique()
    selected_genres = st.sidebar.multiselect("Select Genre(s):", genres,)

    # Rating Filter
    min_rating, max_rating = st.sidebar.slider("Select Rating Range:", 0.0, 10.0, (8.0,10.0),0.1)
    filtered_df = df[(df['RATING'] >= min_rating) & (df['RATING'] <= max_rating)]
    # st.write(filtered_df.reset_index(drop=True))
   
    # Duration Filter
    min_dur=st.sidebar.selectbox("Select min duration :",sorted(df['DURATION'].unique()))
    max_dur=st.sidebar.selectbox("Select max duration :",sorted(df['DURATION'].unique()))
    filtered_df = df[(df['DURATION'] >= min_dur) & (df['RATING'] <= max_dur)]

        # def min_to_hr(df):
        #     for i, row in df.iterrows():
        #         hr = row['DURATION'] // 60
        #         min = row['DURATION'] % 60
        #         # Update the 'DURATION' column with the formatted string
        #         df.at[i, 'DURATION'] = f"{hr}h {min}m"
        #     return df
    
    
    # df['DURATION'] = (df['DURATION'] // 60).astype(str) + 'h ' + (df['DURATION'] % 60).astype(str) + 'm'
    # df['DURATION'] = (df['DURATION']//60+'h'+df['DURATION']%60+'m')
    # df['DURATION'] = df['DURATION']//60+'h'
    # min_to_hr(df)
    # st.sidebar.multiselect("Select duration :",df['DURATION'].unique())
    # filtered_df = df[(df['DURATION'] >= min_dur) & (df['DURATION'] <= max_dur)]
    # st.write(filtered_df.reset_index(drop=True))


    # voting count
    min_votes, max_votes = st.sidebar.slider("Select the voting range:",int(df['VOTING COUNT'].min()),int(df['VOTING COUNT'].max()),(int(df['VOTING COUNT'].min()), int(df['VOTING COUNT'].max())),100000)
    filtered_df = df[(df['VOTING COUNT'] >= min_votes) & (df['VOTING COUNT'] <= max_votes)]

    # Apply filters
    filtered_df = df[
        (df['GENRE'].isin(selected_genres)) &
        (df['RATING'] >= min_rating) &
        (df['RATING'] <= max_rating) &
        (df['DURATION'] >= min_dur) &
        (df['DURATION'] <= max_dur)&
        (df['VOTING COUNT'] >= min_votes) &
        (df['VOTING COUNT'] <= max_votes)
        ]

    # Display the filtered DataFrame
    st.write("Filtered Results:")
    st.dataframe(filtered_df)
