
import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from datetime import date
import requests

st.set_page_config(page_title="Community Agent", layout="wide")

st.title("🌿 Community Agent")
st.subheader("How can I help today?")

# Load and cache the cleaned volunteer data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vigicutler/localeventagent/main/volunteer_opportunities_clean_with_address.csv"
    df = pd.read_csv(url)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    df["Tags"] = df["Tags"].fillna("")
    return df

df = load_data()

# Optional: fetch weather for a given ZIP code using OpenWeatherMap
def get_weather(zip_code, api_key="YOUR_API_KEY"):
    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},US&appid={api_key}&units=imperial"
        response = requests.get(weather_url)
        data = response.json()
        if "main" in data:
            return f"{data['weather'][0]['description'].title()}, {data['main']['temp']}°F"
    except:
        return None

# User input
user_prompt = st.text_input("💬 What kind of cause or vibe are you looking to help with?", "nature, community, youth")
zip_input = st.text_input("📍 Enter your ZIP code", "10040")
weather_info = get_weather(zip_input)

if weather_info:
    st.markdown(f"**Current Weather:** {weather_info}")

# Filter and fuzzy match
def fuzzy_match(row, prompt):
    tags = row["Tags"]
    return fuzz.partial_ratio(prompt.lower(), tags.lower())

df["Score"] = df.apply(lambda row: fuzzy_match(row, user_prompt), axis=1)
top_matches = df[df["Score"] > 50].sort_values(by="Score", ascending=False)

# Show top matches
st.markdown("## Top Opportunities")
if not top_matches.empty:
    for _, row in top_matches.iterrows():
        st.markdown(f"""
---
### {row['Title']}
Date: {row['Date']}  
Location: {row['Location']}  
Tags: _{row['Tags']}_  
Description: {row['Description']}  
[More Info]({row['URL'] if 'URL' in row else '#'})
        """)
        col1, col2 = st.columns(2)
        with col1:
            st.button("Add to Calendar", key=f"cal_{row['Title']}")
        with col2:
            st.button("Share", key=f"share_{row['Title']}")
else:
    st.info("No strong matches found. Try a different vibe or tag!")
