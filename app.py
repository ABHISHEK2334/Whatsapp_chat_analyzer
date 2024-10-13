import streamlit as st
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
[data-testid="stApp"] {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}} 

[data-testid="stHeader"] {{
    background:transparent;
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



# Embed background style and GTM script
st.markdown(f"""
    {page_bg_img}
    
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
        ax.plot(timeline["time"], timeline["message"], color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
