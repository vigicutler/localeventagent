import streamlit as st
import pandas as pd

st.set_page_config(page_title="Local Event Agent", layout="wide")

st.title("🌆 Local Event Agent")
st.subheader("Discover events tailored to your neighborhood and interests")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vigicutler/localeventagent/main/extended_event_landscape.csv"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error("❌ Failed to load event data. Check if the CSV exists and the repo is public.")
        st.stop()

df = load_data()

# Filter options
if "Neighborhood" in df.columns and "Date" in df.columns and "Tags" in df.columns:
    neighborhood = st.selectbox("Select your neighborhood:", sorted(df["Neighborhood"].dropna().unique()))
    day = st.selectbox("Select a day:", sorted(df["Date"].dropna().unique()))
    tag_filter = st.multiselect("Filter by tag:", sorted(set(tag for tags in df["Tags"].dropna() for tag in tags.split(","))))

    # Filter data
    filtered_df = df[(df["Neighborhood"] == neighborhood) & (df["Date"] == day)]
    if tag_filter:
        filtered_df = filtered_df[filtered_df["Tags"].apply(lambda x: any(tag in x.split(",") for tag in tag_filter))]

    # Show results
    st.markdown("### 🎟️ Top Events")
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
---
### {row['Event Name']}
🕒 {row['Date']} at {row['Time']}
📍 {row['Neighborhood']}
📝 {row['Description']}
🏷️ {row['Tags']}
🔗 [More Info]({row['URL']})
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.button("📅 Add to Calendar", key=f"cal_{row['Event Name']}")
        with col2:
            st.button("🔗 Share", key=f"share_{row['Event Name']}")
else:
    st.error("❌ Expected columns not found in CSV. Please ensure columns like 'Neighborhood', 'Date', and 'Tags' exist.")

