# Weather Data CSV File Viewer

This Streamlit app allows you to upload and explore weather data from a CSV file. It provides interactive pages for viewing, filtering, and visualizing your data in several ways.

## Features

- **Home**: Upload a CSV file and see upload status.
- **DataFrame**: View the entire CSV as a table.
- **Graph**: Display a histogram of a selected numeric column, with options to filter by location and limit the number of rows.
- **Date Graph**: Plot up to two numeric columns against a date column, with location and row limit controls.
- **Wind Gust Dir Frequency**: Visualize the frequency of wind gust directions, ordered by compass points, with location and row limit controls.
- **Simple Graph**: Plot any two numeric columns against each other as a line chart, with location and row limit controls.

## How to Use

1. **Install requirements**
   ```
   pip install streamlit pandas
   ```

2. **Run the app**
   ```
   streamlit run hello.py
   ```

3. **Interact**
   - Use the sidebar to upload your CSV file.
   - Navigate between pages using the sidebar menu.
   - Use the controls on each page to filter by location, select columns, and limit the number of rows displayed.

## Notes

- The app tries to auto-detect location and date columns based on common names.
- Wind gust direction graphs use compass order:  
  `N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW`
- All graphs allow you to limit the number of rows or show all data.

---

Built with [Streamlit](https://streamlit.io/) and [pandas](https://pandas.pydata.org/).