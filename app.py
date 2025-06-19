import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Local Event Agent", layout="wide")

# Title and subtitle
st.title("🌆 Local Event Agent")
st.subheader("Discover events tailored to your neighborhood and interests")

# Load data from GitHub (raw CSV link)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vigicutler/local-event-agent/main/extended_event_landscape.csv"
    df = pd.read_csv(url)
    return df

# Load the data
df = load_data()

# --- User Filters ---
# Neighborhood dropdown
neighborhoods = sorted(df["Neighborhood"].dropna().unique())
selected_neighborhood = st.selectbox("Select your neighborhood:", neighborhoods)

# Date dropdown
dates = sorted(df["Date"].dropna().unique())
selected_date = st.selectbox("Select a day:", dates)

# Tag filter
all_tags = sorted(set(tag.strip() for tags in df["Tags"].dropna() for tag in tags.split(",")))
selected_tags = st.multiselect("Filter by tag:", all_tags)

# --- Filter Data ---
filtered_df = df[
    (df["Neighborhood"] == selected_neighborhood) &
    (df["Date"] == selected_date)
]

# Tag filtering (if tags selected)
if selected_tags:
    filtered_df = filtered_df[filtered_df["Tags"].apply(
        lambda x: any(tag.strip() in x.split(",") for tag in selected_tags)
    )]

# --- Display Results ---
st.markdown("### 🎟️ Top Events")

if filtered_df.empty:
    st.info("No events match your filters. Try adjusting the tags or date.")
else:
    for _, row in filtered_df.iterrows():
        st.markdown("---")
        st.markdown(f"### {row['Event Name']}")
        st.markdown(f"🕒 **{row['Date']} at {row['Time']}**")
        st.markdown(f"📍 **{row['Neighborhood']}**")
        st.markdown(f"📝 {row['Description']}")
        st.markdown(f"🏷️ *Tags:* {row['Tags']}")
        st.markdown(f"🔗 [More Info]({row['URL']})")

        col1, col2 = st.columns(2)
        with col1:
            st.button("📅 Add to Calendar", key=f"cal_{row['Event Name']}")
        with col2:
            st.button("🔗 Share", key=f"share_{row['Event Name']}")
