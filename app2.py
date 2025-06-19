
import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

st.set_page_config(page_title="🤝 Community Agent", layout="wide")

# Title
st.title("🤝 Community Agent")
st.subheader("Ask: 'How can I help?' — Get real, local ways to show up.")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vigicutler/localeventagent/main/extended_event_landscape.csv"
    df = pd.read_csv(url)
    df = df.rename(columns={"Location": "Neighborhood", "Event Name": "Event Name", "Description": "Description",
                            "URL": "URL", "Date": "Date", "Time": "Time", "Tags": "Tags"})
    df["Tags"] = df["Tags"].fillna("")
    return df

df = load_data()

# User Prompt
user_input = st.text_input("Type your intention or question (e.g., 'How can I help with nature this weekend?')")

def score_match(row, query):
    tags = row["Tags"].split(",") if row["Tags"] else []
    return max([fuzz.partial_ratio(tag.strip().lower(), query.lower()) for tag in tags] or [0])

if user_input:
    df["score"] = df.apply(lambda row: score_match(row, user_input), axis=1)
    top_events = df[df["score"] > 50].sort_values("score", ascending=False).head(5)
    other_events = df[~df.index.isin(top_events.index)].sort_values("Date").head(5)

    st.markdown("### 🌟 Your Top Matches")
    for _, row in top_events.iterrows():
        st.markdown(f'''
**{row["Event Name"]}**  
🕒 {row["Date"]} at {row["Time"]}  
📍 {row["Neighborhood"]}  
📝 {row["Description"]}  
🏷️ _{row["Tags"]}_  
🔗 [More Info]({row["URL"]})
''')

    st.markdown("---")
    st.markdown("### 📍 Other Events Happening Nearby")
    for _, row in other_events.iterrows():
        st.markdown(f'''
**{row["Event Name"]}**  
🕒 {row["Date"]} at {row["Time"]}  
📍 {row["Neighborhood"]}  
🏷️ _{row["Tags"]}_  
🔗 [More Info]({row["URL"]})
''')
else:
    st.info("Type something above to get started — e.g., 'How can I help with seniors this week?'")
