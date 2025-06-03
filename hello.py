import streamlit as st
import pandas as pd

st.set_page_config(page_title="Weather Data CSV File Viewer", page_icon="📄")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select a page",
    ["Home", "DataFrame", "Graph", "Date Graph", "Wind Gust Dir Frequency", "Simple Graph"]
)

# File uploader (shared between pages)
uploaded_file = st.sidebar.file_uploader("Choose a Weather Data CSV file", type="csv")

# Store the dataframe in session state for access across pages
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state["df"] = df
else:
    st.session_state["df"] = None

# Detect location columns (commonly named 'location', 'site', 'station', etc.)
def get_location_column(df):
    location_keywords = ["location", "site", "station", "area", "place"]
    for col in df.columns:
        if any(keyword in col.lower() for keyword in location_keywords):
            return col
    return None

if page == "Home":
    st.title("Weather Data CSV File Viewer")
    if uploaded_file is not None:
        st.write("Weather Data CSV file uploaded successfully.")
    else:
        st.info("Please upload a Weather Data CSV file to display its contents.")

elif page == "DataFrame":
    st.title("DataFrame Page")
    if st.session_state.get("df") is not None:
        st.dataframe(st.session_state["df"])
    else:
        st.info("No Weather Data CSV file uploaded yet. Please upload a file on the Home page.")

elif page == "Graph":
    st.title("Graph Page")
    df = st.session_state.get("df")
    if df is not None:
        location_col = get_location_column(df)
        if location_col:
            locations = df[location_col].dropna().unique()
            selected_location = st.selectbox("Select weather station location", locations)
            df = df[df[location_col] == selected_location]
        numeric_cols = df.select_dtypes(include='number').columns
        max_rows = len(df)
        # ...existing code...
        
        row_limit = st.number_input(
            "Limit number of rows to display (set to max for all rows)",
            min_value=1,
            max_value=max_rows,
            value=min(100, max_rows),
            step=100
        )
        use_all_rows = st.checkbox("Show all rows (max)", value=False)
        if use_all_rows:
            df_limited = df
        else:
            df_limited = df.head(row_limit)
        
        # ...use df_limited in all graph plotting code as before...
        if len(numeric_cols) > 0:
            col = st.selectbox("Select column for histogram", numeric_cols)
            bins = st.slider("Number of bins", min_value=5, max_value=100, value=20)
            st.bar_chart(df_limited[col].value_counts(bins=bins).sort_index())
        else:
            st.warning("No numeric columns found to plot.")
    else:
        st.info("No CSV file uploaded yet. Please upload a file on the Home page.")

elif page == "Date Graph":
    st.title("Date Graph Page")
    df = st.session_state.get("df")
    if df is not None:
        location_col = get_location_column(df)
        if location_col:
            locations = df[location_col].dropna().unique()
            selected_location = st.selectbox("Select location", locations)
            df = df[df[location_col] == selected_location]
        date_cols = df.select_dtypes(include=["datetime", "datetime64", "datetime64[ns]"]).columns.tolist()
        if not date_cols:
            date_cols = [col for col in df.columns if "date" in col.lower()]
        if date_cols:
            date_col = st.selectbox("Select Date column", date_cols)
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) > 0:
                y_cols = st.multiselect(
                    "Select up to 2 data columns to plot", numeric_cols, default=numeric_cols[:2], max_selections=2
                )
                if y_cols:
                    max_rows = len(df)
                    # ...existing code...
                    
                    row_limit = st.number_input(
                        "Limit number of rows to display (set to max for all rows)",
                        min_value=1,
                        max_value=max_rows,
                        value=min(100, max_rows),
                        step=100
                    )
                    use_all_rows = st.checkbox("Show all rows (max)", value=False)
                    if use_all_rows:
                        df_limited = df
                    else:
                        df_limited = df.head(row_limit)
            
                    # ...use df_limited in all graph plotting code as before...
                    st.line_chart(df_limited.set_index(date_col)[y_cols])
                else:
                    st.info("Please select at least one data column to plot.")
            else:
                st.warning("No numeric columns found to plot.")
        else:
            st.warning("No date column found in the data.")
    else:
        st.info("No CSV file uploaded yet. Please upload a file on the Home page.")

elif page == "Wind Gust Dir Frequency":
    st.title("Wind Gust Direction Frequency")
    df = st.session_state.get("df")
    if df is not None:
        location_col = get_location_column(df)
        if location_col:
            locations = df[location_col].dropna().unique()
            selected_location = st.selectbox("Select location", locations)
            df = df[df[location_col] == selected_location]
        gust_dir_cols = [col for col in df.columns if "gust" in col.lower() and "dir" in col.lower()]
        if gust_dir_cols:
            gust_dir_col = st.selectbox("Select Wind Gust Direction column", gust_dir_cols)
            max_rows = len(df)
            row_limit = st.number_input(
                "Limit number of rows to display (set to max for all rows)",
                min_value=1,
                max_value=max_rows,
                value=min(100, max_rows),
                step=100
            )
            use_all_rows = st.checkbox("Show all rows (max)", value=False)
            if use_all_rows:
                df_limited = df
            else:
                df_limited = df.head(row_limit)

            # Define compass order
            compass_order = [
                "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
            ]
            # Count and order by compass
            value_counts = df_limited[gust_dir_col].value_counts()
            ordered_counts = value_counts.reindex(compass_order).fillna(0)
            st.bar_chart(ordered_counts)
        else:
            st.warning("No wind gust direction column found in the data.")
    else:
        st.info("No CSV file uploaded yet. Please upload a file on the Home page.")

elif page == "Simple Graph":
    st.title("Simple Graph Page")
    df = st.session_state.get("df")
    if df is not None:
        location_col = get_location_column(df)
        if location_col:
            locations = df[location_col].dropna().unique()
            selected_location = st.selectbox("Select location", locations)
            df = df[df[location_col] == selected_location]
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("Select X-axis", numeric_cols)
            y_axis = st.selectbox("Select Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
            max_rows = len(df)
            row_limit = st.number_input(
                "Limit number of rows to display (set to max for all rows)",
                min_value=1,
                max_value=max_rows,
                value=min(100, max_rows),
                step=100
            )
            use_all_rows = st.checkbox("Show all rows (max)", value=False)
            if use_all_rows:
                df_limited = df
            else:
                df_limited = df.head(row_limit)
            st.line_chart(df_limited[[x_axis, y_axis]])
        elif len(numeric_cols) == 1:
            st.line_chart(df[numeric_cols[0]])
        else:
            st.warning("No numeric columns found to plot.")
    else:
        st.info("No CSV file uploaded yet. Please upload a file on the Home page.")