#app.py
import streamlit as st    ##1E364A
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_img_as_base64("pexels-goumbik-590022.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-color: white;
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}} 

[data-testid="stHeader"]{{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: margin-top;
    background-repeat: no-repeat;
}}
[data-testid=stSidebar]{{
   background-color: #ADD8E6;
}}
[data-testid=stFileUploaderDropzone]{{
   background-color: #ADD8E6;
}}

[data-testid=baseButton-secondary]{{
        background-color: #4CAF50; 
        color: white; 
        border: 2px solid #4CAF50;
        border-radius: 4px; 
        padding: 10px; 
        background-color: #45a049; 
        border: 2px solid #45a049;
}}
</style>
"""
gtm_script = """
<head>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-5JLDQDFN');</script>
<!-- End Google Tag Manager -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5JLDQDFN"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
</head>
"""

st.markdown(f"""
    {page_bg_img}
    {gtm_script}
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-top: -40px;">
        <h1 style="font-size: 65px; font-weight: bold; color:black;">WhatsApp Chat Analyzer</h1>
    </div>
""", unsafe_allow_html=True)





st.sidebar.title("WhatsApp Chat Analyzer")
upload_file = st.sidebar.file_uploader("Choose a file")

if upload_file is not None:
    byte_data = upload_file.getvalue()
    data = byte_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    st.dataframe(df)

    list_of_user = df["user"].unique().tolist()
    list_of_user.remove("group_notification")
    list_of_user.sort()
    list_of_user.insert(0, "overall")
    selected_user = st.sidebar.selectbox("Show the analysis with respect to", list_of_user)

    if st.sidebar.button("Show Analysis"):
        num_of_messages, words, num_of_media, delete_messages, num_of_links = helper.fetch_stats(selected_user, df)



        st.markdown(f"<p style='font-size:30px; font-weight:bold; color: #10304A;'>Messages: {num_of_messages}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:30px; font-weight:bold; color: #10304A;'>Total words: {words}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:30px; font-weight:bold; color: #10304A;'>Media: {num_of_media}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:30px; font-weight:bold; color: #10304A;'>Deleted Messages: {delete_messages}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:30px; font-weight:bold; color: #10304A;'>Links: {num_of_links}</p>", unsafe_allow_html=True)

        st.markdown("""
            <div style="text-align: center; margin-top: -40px;">
                <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Monthly Timeline</h1>
            </div>
        """, unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("""
                 <div style="text-align: center; margin-top: -40px;">
                    <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Daily Timeline</h1>
                </div>
                """, unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["message"])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("""
                <div style="text-align: center; margin-top: -40px;">
                    <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Activity Map</h1>
                </div>
                """, unsafe_allow_html=True)
        col1,col2=st.columns(2)

        with col1:
            st.markdown("""
                <div>
                    <h1 style="font-size: 30px; font-weight: bold; color:#10304A;">Most Busy Day</h1>
                </div>
                """, unsafe_allow_html=True)
            busy_day=helper.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.markdown("""
                <div>
                    <h1 style="font-size: 30px; font-weight: bold; color:#10304A;">Most Busy Month</h1>
                </div>
                """, unsafe_allow_html=True)
            busy_Month = helper.Month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_Month.index, busy_Month.values,color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)




        if selected_user == "overall":
            st.markdown("""
                <div style="text-align: center; margin-top: -40px;">
                    <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Most Busy User</h1>
                </div>
                """, unsafe_allow_html=True)
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            plt.xticks(rotation="vertical")
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color="red")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.markdown("""
            <div style="text-align: center; margin-top: -40px;">
                <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Word Cloud</h1>
            </div>
            """, unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.markdown("""
            <div style="text-align: center; margin-top: -40px;">
                <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Most Common Words</h1>
            </div>
            """, unsafe_allow_html=True)
        most_common_word = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_word["Word"], most_common_word["Frequency"])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("""
            <div style="text-align: center; margin-top: -40px;">
                <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Emoji Analyzer</h1>
            </div>
            """, unsafe_allow_html=True)
        emoji_df = helper.emoji_helper(selected_user, df)

        # Debugging: Check the content of emoji_df

        if not emoji_df.empty and emoji_df.shape[1] >= 2:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1], labels=emoji_df[0])  # , autopct="%0.2f"
                st.pyplot(fig)
        else:
            st.markdown("""
                <div>
                    <h1 style="font-size: 30px; font-weight: bold; color:#10304A;">Emoji Not Available</h1>
                </div>
                """, unsafe_allow_html=True)


        st.markdown("""
        <div style="text-align: center; margin-top: -40px;">
            <h1 style = "font-size:40px; font-weight:bold; color:#10304A;">Heat Map</h1>
        </div>    
        """,unsafe_allow_html=True)
        heat_map = helper.heat_map(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(heat_map)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.markdown("""
                    <div style="text-align: center; margin-top: -40px;">
                        <h1 style="font-size: 40px; font-weight: bold; color:#10304A;">Sentiment Analysis</h1>
                    </div>
                """, unsafe_allow_html=True)
        if selected_user != "overall":
            df = df[df["user"] == selected_user]
        sentiment_counts = df['sentiment'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140,
               colors=['#28a745', '#dc3545', '#ffc107'])
        ax.axis('equal')
        st.pyplot(fig)
