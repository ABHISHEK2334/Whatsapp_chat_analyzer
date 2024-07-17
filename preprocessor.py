#preprocessor.py
import re
import pandas as pd
import base64
import streamlit as st
from textblob import TextBlob

def preprocess(data):

    # Regular expression pattern for date and time with optional space
    pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s?\u202F?[ap]m\s-'

    # Debugging: Print data to verify content
    # print("Raw data:", data[:1000])  # Print first 1000 characters of data for verification

    # Extract dates and messages
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Debugging: Check extracted dates and messages
    print("Extracted dates:", dates[:5])  # Print first 5 dates
    print("Extracted messages:", messages[:5])  # Print first 5 messages

    if len(dates) != len(messages):
        print("Mismatch between number of dates and messages")

    # Create DataFrame
    df = pd.DataFrame({'date': dates, 'user_message': messages})

    if df.empty:
        print("DataFrame is empty after creation")
    else:
        print("DataFrame created successfully")

    # Convert 'date' to string before using .str.strip()
    df['date'] = df['date'].astype(str).str.strip()

    # Attempt to convert to datetime, handling errors gracefully
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p -', errors='coerce')

    # Debugging: Check for any NaT values
    if df['date'].isna().sum() > 0:
        print("Conversion to datetime failed for some entries.")
        print(df[df['date'].isna()])

    user = []
    message_text = []

    for message in df['user_message']:
        entry = re.split(r"([\w\W]+?):\s", message, 1)  # Limit split to 1 to capture only first username
        if len(entry) > 1:
            user.append(entry[1])
            message_text.append(entry[2])
        else:
            user.append('group_notification')
            message_text.append(entry[0])

    df['user'] = user
    df['message'] = message_text
    df.drop(columns=['user_message'], inplace=True)
    df["only_date"]=df["date"].dt.date
    df['month'] = df['date'].dt.month_name()
    df["month_num"]=df["date"].dt.month
    df['year'] = df['date'].dt.year
    df['day'] = df['date'].dt.day
    df["day_name"]=df["date"].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period=[]
    for hour in df[["day_name","hour"]]["hour"]:
        if hour == 23:
            period.append(str(hour)+"-"+str("00"))
        elif hour == 0:
            period.append(str("00")+"-"+str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period']=period


    df['polarity'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment'] = df['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))



    return df
""""this is a generating a data frame of chating"""

