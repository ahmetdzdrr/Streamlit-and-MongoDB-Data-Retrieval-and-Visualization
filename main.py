import ast
import pandas as pd
from pymongo import MongoClient
import streamlit as st
import configparser
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import random
warnings.simplefilter("ignore")

def request():
    config = configparser.ConfigParser()
    config.read('config.ini')

    db_name = config['Database']['db_name']
    collection_name = config['Database']['collection_name']
    user_name = config['Database']['user_name']
    password = config['Database']['password']

    uri = f"mongodb+srv://{user_name}:{password}@cluster0.x5sofsy.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)

    try:
        client.admin.command('ping')

        db = client[db_name]
        collection = db[collection_name]
        data_list = list(collection.find())
        data = pd.DataFrame(data_list)
        dataframe = data.copy()
        dataframe.to_csv("airbnb_data.csv", index=None)

        st.success("Pinged your deployment. You successfully connected to MongoDB!", icon="✅")

    except Exception as e:
        st.exception(e)


def analysis(dataframe):
    dataframe.drop(
        ["reviews_per_month", "_id", "listing_url", "name", "summary", "space", "access", "house_rules",
         "calendar_last_scraped", "description",
         "notes", "transit", "interaction", "neighborhood_overview", "images", "host"], axis=1, inplace=True)

    dataframe['address'] = dataframe['address'].apply(ast.literal_eval)
    dataframe['city'] = dataframe['address'].apply(lambda x: x.get('street').split(',')[0])
    dataframe['country'] = dataframe['address'].apply(lambda x: x.get('country'))

    dataframe["review_scores"] = dataframe["review_scores"].apply(ast.literal_eval)
    dataframe["accuracy"] = dataframe['review_scores'].apply(lambda x: x.get('review_scores_accuracy'))
    dataframe["cleanliness"] = dataframe['review_scores'].apply(lambda x: x.get('review_scores_cleanliness'))
    dataframe["checkin"] = dataframe['review_scores'].apply(lambda x: x.get('review_scores_checkin'))
    dataframe["communication"] = dataframe['review_scores'].apply(lambda x: x.get('review_scores_communication'))
    dataframe["location"] = dataframe['review_scores'].apply(lambda x: x.get('review_scores_location'))
    dataframe["value"] = dataframe['review_scores'].apply(lambda x: x.get('review_scores_value'))
    dataframe["rating"] = dataframe['review_scores'].apply(lambda x: x.get('review_scores_rating'))


    dataframe["total_amenities"] = dataframe["amenities"].apply(lambda x: len(x))

    dataframe.drop(['address', "last_scraped", "amenities", "first_review", "last_review", "review_scores", "reviews", "address",
                    "availability"], axis=1, inplace=True)

    pd.set_option("display.max_columns", 500)
    st.write(dataframe)
    return dataframe

def pie_visualization(dataframe):
    columns = [col for col in dataframe.columns if dataframe[col].nunique() < 6]
    column_option = st.selectbox("Choose a feature for Pie Chart:", ['None'] + columns)
    if column_option != 'None':
        target_counts = dataframe[column_option].value_counts()

        colors = [plt.cm.Paired(random.choice(range(12))) for _ in range(len(target_counts))]

        wedgeprops = {'linewidth': 2, 'edgecolor': 'white'}
        fig, ax = plt.subplots()
        ax.pie(target_counts, labels=target_counts.index, autopct='%1.2f%%',
               startangle=90, wedgeprops=wedgeprops, colors=colors)
        ax.axis('equal')
        ax.set_title(f"{column_option} Pie Chart")
        st.pyplot(fig)


def barplot_visualization(dataframe):
    columns = [col for col in dataframe.columns if dataframe[col].nunique() > 6]
    columns_option = st.selectbox("Choose a feature for Bar Chart:", ["None"] + columns)

    if columns_option != 'None':
        plt.figure(figsize=(12, 6))
        plt.title(f"{columns_option} Bar Plot")
        sns.set(font_scale=1.5)
        sns.countplot(data=dataframe, x=columns_option)
        st.pyplot()