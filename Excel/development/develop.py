import streamlit as st
import pandas as pd
import base64
import io

# selected_columns = ['Code', 'Name', 'Date', 'First In Time', 'Last Out Time', 'Total_Out_Duration']
selected_columns = ['Code', 'Name', 'Date', 'In Time', 'Out Time', 'Duration', 'Total_In_Duration', 'Total_Out_Duration']

@st.cache_data
def calculate_total_duration(df):
    df_filtered = df.fillna("00:00")
    column_filter = df_filtered[df_filtered.columns[df_filtered.columns.str.startswith('DurationOut')]]
    column_filter2 = df_filtered['Duration']
    
    total_outduration = []
    total_intime = []  # Moved this line outside the loop
    
    for x in range(len(df_filtered)):
        total_outduration.append(pd.to_timedelta(column_filter.iloc[x] + ":00").dt.total_seconds().sum() / 3600)

        # Ensure correct formatting before converting to timedelta
        total_duration_str = column_filter2.iloc[x]
        total_duration_str = total_duration_str if pd.notna(total_duration_str) else "00:00:00"
        
        try:
            total_duration = pd.to_timedelta(total_duration_str).total_seconds()
        except ValueError:
            print(f"Error converting Total Duration at index {x}: {total_duration_str}")

        time_difference = pd.to_timedelta(total_duration, unit='s') - pd.to_timedelta(total_outduration[x], unit='h')
        total_intime.append(time_difference)

    df_filtered["Total_Out_Duration"] = total_outduration
    df_filtered["Total_Out_Duration"] = df_filtered["Total_Out_Duration"].apply(lambda x: '{:02}:{:02}:{:02}'.format(int(x), int((x * 60) % 60), int((x * 3600) % 60)))
    
    # Moved the assignment of the entire list to the DataFrame column outside the loop
    df_filtered["Total_In_Duration"] = total_intime
    
    result_pd = df_filtered[selected_columns]   
        
    return result_pd

def main():
    st.title("Total Out Time Summary")
    # File upload in the sidebar
    uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        st.sidebar.success("File Uploaded Successfully!")
        # Read Excel file
        try:
            with st.spinner("Loading data..."):
                df = pd.read_excel(uploaded_file, header=5)
                st.write(df)
                # Calculate total duration
            with st.spinner("Calculating total duration..."):
                df_calculated = calculate_total_duration(df)
                st.success("File Uploaded Successfully!")
                # Display DataFrame
            st.subheader("Results:")
            st.write(df_calculated[selected_columns])
            
            total_in_duration = df_calculated["Total_In_Duration"].tolist()
            st.write("Total In Duration List:", total_in_duration)
            
        except Exception as e:
            st.error(f"Error: {e}")
            return
    
        st.success("Calculation Successfully Done!")
        
        excel_link = get_table_download_link(df_calculated)
        st.sidebar.markdown(excel_link, unsafe_allow_html=True)
        
@st.cache_data
def get_table_download_link(df):
    # Create a virtual in-memory Excel file
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    # B64 encoding
    b64 = base64.b64encode(excel_buffer.read()).decode()

    # Provide the download link
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="output.xlsx">Download Excel File</a>'
    return href

if __name__ == "__main__":
    main()
