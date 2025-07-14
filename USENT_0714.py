import streamlit as st
import pandas as pd
import zipfile
import io
import os
import time



# from pandas.api.types import CategoricalDtype # Import CategoricalDtype
st.set_page_config(layout="wide")


logo_link_cxpt = r"C:\Users\VACOAzizS1\Documents\Python Scripts\USENT\UnZip-LOINC-app-main\USENT_Logo-removebg.png"
with st.sidebar:
  st.image(logo_link_cxpt, width=100, caption=None)

# st.image(logo_link_cxpt, width=200, caption=None)

col1, col2 = st.columns([1, 2]) # Adjust the ratio as needed
with col1:
    st.image(logo_link_cxpt, width=260, caption=None)

with col2:
    st.write(f"# Unzip Summary of Episode Note")




# Create a permanent unzip directory
# UNZIP_DIR = "unzipped_files"
UNZIP_DIR = r"C:\Users\VACOAzizS1\Documents\Python Scripts\USENT"
os.makedirs(UNZIP_DIR, exist_ok=True)

# Title & Sidebar
st.sidebar.header('Unzip Summary of Episode Note (USENT)')
# st.header('Unzip Summary of Episode Note (USENT)')

# Upload Meta File
uploaded_file = st.sidebar.file_uploader("Browse a Meta Data File", type=['csv'])

# Upload ZIP file
uploaded_zip = st.sidebar.file_uploader("Browse a Zipped File", type=["zip"])
zip_bytes = None



df = None  # Placeholder for the dataframe
file_names = []  # Placeholder for file names

if uploaded_file is None:
    st.warning("Please upload a Meta File to proceed.")

# If Meta file is uploaded
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(f"")
    st.write(f"")
    st.write(f"")
    st.write(f"## Meta Data & C-CDA XML Files:")
    # st.title("_Data Upload Completed_ :sunglasses:")
    st.write(f"##### #️⃣ Number of Listed File Names in the Meta Data: {len(df)}")
    
    # st.write(f"First 5 rows of the meta data:")
    # st.write(df.head())

    # loinc_file = pd.crosstab(df['Organization'], df['CDA_Document_Code'])
    # st.write(f"###### 🏣 Organization by LOINC:")  
    # st.write(loinc_file.head())

    if uploaded_zip is None:
        st.warning("Please upload a C-CDA Zip File to proceed.")
    
    
if uploaded_zip is not None:
    zip_bytes = io.BytesIO(uploaded_zip.read())

    with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
        file_list = zip_ref.namelist()
        st.write(f"##### #️⃣ Number of C-CDA XML files in the zipped folder: {len(file_list)}")

    # Proceed if Meta file is uploaded
    if st.checkbox(" ⚙️ " "Filter Data by Loinc and Organization"):
    # if st.button(f" #### ⚙️ Filter Data by Loinc and Organization"):
        if df is not None:
            # Sidebar Filters
            loinc_options = ["All LOINC"] + sorted(df['CDA_Document_Code'].dropna().unique())
            selected_loinc = st.selectbox(f"## Filter by LOINC", loinc_options)
        
            org_options = ["All Organization"] + sorted(df['Organization'].dropna().unique())
            selected_org = st.selectbox("Filter by Organization", org_options)
        
            # Start with full data
            filtered_df = df.copy()
        
            # Apply LOINC filter
            if selected_loinc != "All LOINC":
                filtered_df = filtered_df[filtered_df['CDA_Document_Code'] == selected_loinc]
        
            # Apply Organization filter
            if selected_org == "All Organization":
                filtered_df_by_loinc_org = filtered_df
            else:
                filtered_df_by_loinc_org = filtered_df[filtered_df["Organization"] == selected_org]
    
         # st.write(filtered_df_by_loinc_org['File_Name'].to_list()[:10])

        # Show unzip button only if ZIP is uploaded
        if uploaded_zip is not None:
            # if st.button("UnZip Matching Files"):
            start_time = time.time()  # ⏱️ Start timer

            with zipfile.ZipFile(zip_bytes, "r") as zip_ref:
                filtered_files = filtered_df_by_loinc_org['File_Name'].dropna().unique().tolist()
                filtered_files_set = set(filtered_files)

                mached_files = []
                for i, file in enumerate(zip_ref.namelist()):
                    base_name = os.path.basename(file)
                    if base_name in filtered_files_set:
                        mached_files.append(base_name)

                # if st.checkbox(" ⚙️ " "Filter Data by Loinc and "):
                st.write(f"##### #️⃣  Number of files filtered by  {selected_loinc} and {selected_org}: &nbsp; {len(filtered_df_by_loinc_org)}")
                st.write(f"##### #️⃣  Number of C-CDA xml files matched filtered files: &nbsp; {len(mached_files)}")

                extracted_files = []
                total_files = len(filtered_files_set)
                if st.button(f"👉 UnZip and Extract Filtered C-CDA XML Files"):
                    progress = st.progress(0, text="Unzipping and Extracting files...")
                    for i, file in enumerate(zip_ref.namelist()):
                        base_name = os.path.basename(file)
                        if base_name in filtered_files_set:
                            zip_ref.extract(file, UNZIP_DIR)
                            extracted_files.append(base_name)
                            
                        progress.progress(min((i + 1) / total_files, 1.0),
                                          text=f"Extracting: {min(i+1, total_files)} / {total_files}")
    
                    end_time = time.time()  # ⏱️ End timer
                    time_taken = end_time - start_time
        
                    if extracted_files:
                        progress.progress(1.0, text="✅ Unzipping and Extraction completed!")
                        # st.subheader("_Unzipping and Extracting are Completed_ :sunglasses:")
                        st.success(f"✅ Extracted {len(extracted_files)} C-CDA XML file(s) to the folder: &nbsp; '{UNZIP_DIR}' ")
                        st.info(f"🕒 Run Time: {time_taken:.3f} seconds")
                    else:
                        st.warning("⚠️ No matching files found in the ZIP archive.")

# else:
#     st.warning("Please upload a C-CDA Zip File to proceed.")