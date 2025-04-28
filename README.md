# IMDB
IMDB 2024 Data scrapping and Visualizations:
An end-to-end data pipeline project that scrapes movie data from IMDB for the year 2024, processes and stores it in a cloud-based SQL database, and presents interactive insights using Streamlit.

The project aims at the following:
1) scrapping the movie data from IMDB for the year 2024 using selinium.
2) clean it using python pandas.
3) store the dataframe in a SQL database (TiDb cloud).
4) Using streamlit,display a dashboard to provide several insights and visualizations of the dataset.

Tools Used:
1) Python
2) selinium
3) MySQL
4) TiDb
5) Streamlit

Project workflow:

1) Using selinium, data from IMDB website was scrapped for the year 2024 across different genres and the scrapped data from each genre was stored as seperste csv files.
2) With the help of Pandas these csv files were merged into sinle csv and coverted into a dataframe. This acts as the final dataset to work on.
3) The data set is further went through cleaning process for effective analyzation.
4) The cleaned dataset is then stored in TiDB cloud (An SQL database).
5) The dataset is accesed from TiDB cloud, using streamlit various visualizaion and insights are developed.
6) User is also allowed to experience dynamic filtering techniques for customized insights.

Folder Structure:

IMDB
│
├── imdb_data_scrapping.ipynb # Selenium scraping scripts
├── merged_data_final.csv     # Final cleaned dataset
├── imdb_sql_connection.ipynb # TiDB DB connection script             
├── IMDB.py                   # Streamlit dashboard   
└── README.md                 
