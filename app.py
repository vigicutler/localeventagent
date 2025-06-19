
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Neighborhood AI", layout="wide")
st.title("🌆 Neighborhood Engagement Agent")

# Load event data
@st.cache_data
def load_data():
    return pd.read_csv("extended_event_landscape.csv")

data = load_data()
data["Tags"] = data["Tags"].fillna("General")

# Split tabs
tab1, tab2 = st.tabs(["🎉 What Should I Do Today?", "🛠️ What Should I Host?"])

with tab1:
    st.header("🎯 Personalized Event Finder")

    zip_input = st.selectbox("Choose a ZIP Code", sorted(data["ZIP"].dropna().unique()))
    tag_options = sorted(set(tag for tags in data["Tags"] for tag in str(tags).split(",")))
    selected_tags = st.multiselect("Pick your interests", tag_options)
    date_input = st.date_input("Choose a date")

    filtered = data[data["ZIP"] == zip_input]
    if selected_tags:
        filtered = filtered[filtered["Tags"].apply(lambda x: any(tag.strip() in x for tag in selected_tags))]
    filtered = filtered[filtered["Date"] == str(date_input)]

    st.subheader(f"🎯 Top Matches for {zip_input} on {date_input}")
    for _, row in filtered.head(3).iterrows():
        st.markdown(f"### {row['Event Name']}")
        st.markdown(f"🕒 {row['Date']} at {row['Time']}  
📍 {row['Location']}")
        st.markdown(f"**Tags:** {row['Tags']}")
        st.markdown(f"[🔗 More Info]({row['URL']})")
        st.markdown("---")

with tab2:
    st.header("🧠 Producer View: Event Insights & Source Tracking")

    st.subheader("Add Your Event Sources")
    with st.form("producer_form"):
        ig = st.text_input("Instagram Handle")
        email = st.text_input("Newsletter URL")
        website = st.text_input("Website with Events")
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("✅ Source submitted! (This is a placeholder)")

    st.subheader("📊 Upcoming Gaps or Opportunities")
    st.markdown("- No arts events listed this Friday in Inwood")
    st.markdown("- High 311 complaint volume in parks → consider organizing a cleanup")
