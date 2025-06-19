import streamlit as st
import pandas as pd

st.set_page_config(page_title="Local Event Agent", layout="wide")

st.title("🌆 Local Event Agent")
st.subheader("Discover events tailored to your neighborhood and interests")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vigicutler/localeventagent/main/extended_event_landscape.csv"
    df = pd.read_csv(url)

    # Rename for consistency
    df = df.rename(columns={
        "Location": "Neighborhood",
        "Event Name": "Event Name",
        "Description": "Description",
        "URL": "URL",
        "Date": "Date",
        "Time": "Time",
        "Tags": "Tags"
    })

    # Ensure Tags column exists and has no NaNs
    if "Tags" not in df.columns:
        df["Tags"] = ""
    else:
        df["Tags"] = df["Tags"].fillna("")

    return df

# 🔽 Load data first
df = load_data()

# ✅ Check columns after loading
required_cols = {"Neighborhood", "Date", "Tags"}
if required_cols.issubset(df.columns):
    neighborhood = st.selectbox("Select your neighborhood:", sorted(df["Neighborhood"].dropna().unique()))
    day = st.selectbox("Select a day:", sorted(df["Date"].dropna().unique()))
    tag_filter = st.multiselect("Filter by tag:", sorted(set(tag.strip() for tags in df["Tags"].dropna() for tag in tags.split(","))))

    # Filter
    filtered_df = df[(df["Neighborhood"] == neighborhood) & (df["Date"] == day)]
    if tag_filter:
        filtered_df = filtered_df[filtered_df["Tags"].apply(lambda x: any(tag.strip() in x.split(",") for tag in tag_filter))]

    # Render event cards
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
