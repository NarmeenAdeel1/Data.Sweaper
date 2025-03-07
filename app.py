import streamlit as st
import pandas as pd
import os
from io import BytesIO

# 🏷️ Set Page Configurations
st.set_page_config(page_title="🐱‍🏍 Data Sweaper", layout="wide") 
st.title("🐱‍🏍 Data Sweaper 🚀")
st.write("👩‍💻 Created by **Narmeen Adeel Siddiqui**")
st.write("🛠️ This is a simple tool to help you clean your data. 📊 Upload your file, clean it, and download the processed version! 🎯")

# 📂 File Upload Section
uploaded_file = st.file_uploader("📂 Upload Files (CSV or Excel):", type=['csv', 'xlsx'], accept_multiple_files=True)
st.write("✨ Upload your file and let **Narmeen Adeel Siddiqui's tool** clean it for you! 😉")  

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"❌ File type not supported: {file_ext}")
        continue

    # 📜 File Details Section
    st.write(f"📜 **File Name:** {file.name}")
    st.write(f"📏 **File Size:** {file.size/1024} KB")

    # 👀 Preview Data
    st.write("🔍 **Preview the Head of the DataFrame:**")
    st.dataframe(df.head())

    # 🧼 Data Cleaning Options
    st.subheader("🧼 Data Cleaning Options")
    if st.checkbox(f"📝 Data Cleaning Options for {file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🗑️ Remove Duplicates From {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("✅ Duplicates Removed Successfully! 😊")

        with col2:
            if st.button(f"🚀 Drop Missing Values From {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("✅ Missing Values Have Been Filled Successfully! 😊")   

    # 📌 Column Selection Section  
    st.subheader("📌 Select Columns to Convert")  
    columns = st.multiselect(f"🎯 Choose Columns for {file.name}", df.columns, default=df.columns)   
    df = df[columns]

    # 📊 Data Visualization Section
    st.subheader("📊 Data Visualization")
    if st.checkbox(f"📈 Show Data Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

    # 🔄 Conversion Section
    st.subheader("💫 Conversion Options")
    conversion_type = st.radio(f"🔄 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
    if st.button(f"⚡ Convert {file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

        # 📥 Download Button 
        st.download_button(
            label=f"📥 Click Here to Download {file_name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type,
        )

# 🎉 Final Success Message
st.success("🎈 All Files Have Been Converted Successfully! ❤️")  
st.write("📌 Developed by **Narmeen Adeel Siddiqui** | 🚀 Happy Cleaning! 💡")
