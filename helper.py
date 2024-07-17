#helper.py
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    num_of_messages = df.shape[0]
    words = [word for message in df["message"] for word in message.split()]
    num_of_media = df[df["message"] == "<Media omitted>\n"].shape[0]
    delete_messages = df[df["message"] == "This message was deleted\n"].shape[0]
    num_of_links = [link for message in df["message"] for link in extract.find_urls(message)]

    return num_of_messages, len(words), num_of_media, delete_messages, len(num_of_links)


def most_busy_user(df):
    df = df[df["user"] != "group_notification"]
    x = df['user'].value_counts().head()
    df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={ "count": "percentage"})
    return x,df


def create_wordcloud(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    df = df[(df["user"] != "group_notification") & (df["message"] != "<Media omitted>\n")]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="black")
    df_wc = wc.generate(df["message"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    df = df[(df["user"] != "group_notification") & (df["message"] != "<Media omitted>\n")]
    words = [word for message in df['message'] for word in message.split()]
    most_common_words = Counter(words).most_common(20)
    most_common_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency']).reset_index(drop=True)
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    emoji_list = [c for message in df['message'] for c in message if c in emoji.EMOJI_DATA]
    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))

    # Debugging: Print the structure and head of emoji_df
    print("Emoji DataFrame structure:", emoji_df.head())

    return emoji_df



def monthly_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()

    time = [f"{row['month']}-{row['year']}" for _, row in timeline.iterrows()]
    timeline["time"] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    daily_timeline=df.groupby("only_date").count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    return df["day_name"].value_counts()

def Month_activity_map(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]
    return df["month"].value_counts()

def heat_map(selected_user, df):
    if selected_user != "overall":
        df = df[df["user"] == selected_user]

    heat_map=df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)
    return heat_map