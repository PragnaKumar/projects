import streamlit as st
import pandas as pd
import datetime
import base64
import io

# selected_columns = ['Code', 'Name', 'Date', 'First In Time', 'Last Out Time',  'Total_Out_Duration']
selected_columns = ['Code', 'Name', 'Date','In Time', 'Out Time', 'Duration', 'Total_Out_Duration']


@st.cache_data
def calculate_total_duration(df):
    df_filtered = df.fillna("00:00")
    column_filter = df_filtered[df_filtered.columns[df_filtered.columns.str.startswith('DurationOut')]]

    total_duration = []
    for x in range(len(df_filtered)):
        total_duration.append(pd.to_timedelta(column_filter.iloc[x]+":00").dt.total_seconds().sum() / 3600)

    df_filtered["Total_Out_Duration"] = total_duration
    df_filtered["Total_Out_Duration"] = df_filtered["Total_Out_Duration"].apply(lambda x: '{:02}:{:02}:{:02}'.format(int(x), int((x * 60) % 60), int((x * 3600) % 60)))
    
    result_pd = df_filtered[selected_columns]    
    return result_pd


@st.cache_data
def calculate_total_in_duration(df):
    duration = df["Duration"]
    total_out_duration = df["Total_Out_Duration"]
    
    total_in_duration = []
    for x in range(len(df)):
        total_duration_hours = pd.to_timedelta(duration.iloc[x]).total_seconds() / 3600
        total_out_duration_hours = pd.to_timedelta(total_out_duration.iloc[x]).total_seconds() / 3600
        time_difference = total_duration_hours - total_out_duration_hours
        total_in_duration.append(time_difference)

    return [str(datetime.timedelta(seconds=duration * 3600)) for duration in total_in_duration]


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
                # st.sidebar.multiselect("Select Columns", df.columns, selected_columns)
                st.write(df)
                # Calculate total duration
            with st.spinner("Calculating total duration..."):
                df["Duration"] = df["Duration"].apply(lambda x: f"{x}:00")
                df["Duration"] = df["Duration"].apply(lambda x: x.replace("-:00", "00:00:00"))
                df_calculated = calculate_total_duration(df)
                df_calculated["Total_In_Duration"] = calculate_total_in_duration(df_calculated)
                st.success("File Uploaded Successfully!")
                # Display DataFrame
            st.subheader("Results:")
            st.write(df_calculated)
            
        except Exception as e:
            st.error(f"Error: {e}")
            return
    
        st.success("Calculation Successfully Done!")
        
        excel_link = get_table_download_link(df_calculated)
        st.download_button(label='📥 Download Current Result',
                                data=df_calculated ,
                                file_name= 'df_test.xlsx')
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

@st.cache_data
def generate_excel(df):
    # Create a virtual in-memory Excel file
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    # Save the Excel file to a local variable
    excel_data = excel_buffer.read()

    # Provide download link
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="output.xlsx">Download Excel File</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("Excel File Generated Successfully!")


if __name__ == "__main__":
    main()
