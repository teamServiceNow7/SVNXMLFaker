import streamlit as st
import xml.etree.ElementTree as ET
import time
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta
 
sidebar_bg_img = """
    
    <style>

    #MainBg
    .st-emotion-cache-1r4qj8v {
    position: absolute;
    background: #FFFAFA;
    color: rgb(49, 51, 63);
    inset: 0px;
    color-scheme: light;
    overflow: hidden;
    }

    h1 {
    font-family: "Font Awesome 6 Pro", sans-serif;
    font-weight: 800;
    font-variant: small-caps;
    background: linear-gradient(to top, #032C41, #02506B);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    padding: 0rem 0px 1rem;
    margin: 0px;
    line-height: 1;
    }

    /*Image Title*/
    .st-emotion-cache-1v0mbdj {
    display: block;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    flex-direction: column;
    -webkit-box-align: stretch;
    align-items: stretch;
    width: auto;
    -webkit-box-flex: 0;
    flex-grow: 0;
    margin-bottom: 1rem;
    margin-top: 0rem;
    }

    .st-emotion-cache-1jicfl2 {
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* header violet*/
    h2{
    background-color: #920113;
    color: white;
    font-variant-caps: all-small-caps;
    text-align: center;
    border-radius: 10px;
    }

    h2 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    letter-spacing: -0.005em;
    padding: 0.25rem 0px;
    margin: 0px;
    line-height: 1.2;
    }
    
    h4{
    color: #920113;
    }
    
    [data-testid= "stThumbValue"]{
    color: #920113;
    }

    /*Logo*/
    .st-emotion-cache-5drf04 {
    height: 7rem;
    max-width: 20rem;
    margin: 0.25rem 0.5rem 0.25rem 0px;
    z-index: 999990;
    }

    /*sidebar heading-demodata xml*/
    .st-emotion-cache-1gwvy71 {
    padding: 0px 1.5rem 6rem;
    }

    .st-emotion-cache-1gwvy71 h1 {
    font-family: "League Spartan", sans-serif;
    color: #ffffff;
    background-color: #032C41;
    font-size: 23px;
    }

     /*sidebar gap */
    .st-emotion-cache-1dfdf75 {
    width: 282px;
    position: relative;
    display: flex;
    flex: 0.5 0.5 0%;
    flex-direction: column;
    gap: 0.5rem;
    flex-wrap: nowrap;
    }

    /*date expander gap*/
    .st-emotion-cache-phzz4j {
    width: 248px;
    position: relative;
    /* display: flex; */
    flex: 0.5 0.5 0%;
    flex-direction: column;
    gap: 0.25rem;
    }

    .st-emotion-cache-1mi2ry5 {
    display: flex;
    -webkit-box-pack: justify;
    justify-content: space-between;
    -webkit-box-align: start;
    align-items: start;
    padding:  0.5rem 0.5rem 0.25rem ;
    }

    /*Sidebar Components*/
    .st-emotion-cache-ue6h4q {
    font-size: 14px;
    color: rgb(49, 51, 63);
    display: flex;
    visibility: visible;
    margin-bottom: 0.5rem;
    height: auto;
    min-height: 1.5rem;
    vertical-align: middle;
    flex-direction: row;
    -webkit-box-align: center;
    align-items: center;
    }


    [data-testid="stSidebar"]{
    background-color: #E6EDF1;    
    width: 15%;
    }

    [data-testid= "stHeader"]{
    background-color: #920113;
    color: #ffffff;
    padding: 1rem;
    }

    [data-testid= "stSidebarUserContent"]{
    background-color: #6d0b17;
    height: 1px;
    }

    [data-testid= "stSidebarHeader"]{
    background-color: #6d0b17;
    }

    /*side bar subhead*/
    .st-emotion-cache-1whx7iy p{
    font-weight: bold;
    font-size: 20px;
    }

    .st-emotion-cache-1ag92y2{
    background-color: #E6EDF1; 
    }
    
    /*for paragraph*/
    p, ol, ul, dl {
        margin-top: 1rem;
        margin-right: 0px;
        margin-bottom: 1rem;
        margin-left: 0px;
        font-size: 1rem;
        font-weight: 400;
    }

    /*expander margin*/
    .st-emotion-cache-p5msec {
        position: relative;
        display: flex;
        width: 100%;
        font-size: 14px;
        padding: 0px 1rem;
        list-style-type: none;
        background-color:#E6EDF1; 
    }

    </style>                 
            
"""

#Function for Usage 
def parse_usage_summary(tree,root,min, max,new_source=None, new_date=None, total_idle_dur=None,total_session_dur = None):

    st.write("  ")
    cols = st.columns(4)  # Adjust the number of columns as needed
    col_idx = 0
    value = 0  # Initialize value here

    for idx, elem in enumerate(root.findall('.//samp_eng_app_usage_summary'), 1):
        if min <= idx <= max:
            if new_source:
                source_elem = elem.find('source')
                if source_elem is not None:
                    source_elem.text = new_source
            if new_date:
                usage_date_elem = elem.find('usage_date')
                if usage_date_elem is not None and usage_date_elem.text is not None:
                    try:
                        date_obj = datetime.strptime(usage_date_elem.text, '%Y-%m-%d')
                        new_date_obj = new_date - date_obj.date()
                        if idx == min:
                            value = new_date_obj.days
                            min = -1
                        new_date1 = date_obj + timedelta(days=value)
                        usage_date_elem.text = new_date1.strftime('%Y-%m-%d')
                    except OverflowError:
                        st.error(f"Date calculation overflow at index {idx}. Original idle duration: {idle_date_elem.text}")
                else:
                    min = min+1
                    usage_date_elem.text = new_date.strftime('%Y-%m-%d')
                 
            if total_idle_dur:
                idle_date_elem = elem.find('total_idle_dur')
                if idle_date_elem is not None and idle_date_elem.text is not None:
                    try:
                        date_obj = datetime.strptime(idle_date_elem.text, '%Y-%m-%d %H:%M:%S')
                        new_date_obj = total_idle_dur - date_obj
                        if idx == min:
                            value = new_date_obj.total_seconds() / 60
                            min = -1
                        new_date1 = date_obj + timedelta(minutes=value)
                        idle_date_elem.text = new_date1.strftime('%Y-%m-%d %H:%M:%S')
                    except OverflowError:
                        st.error(f"Date calculation overflow at index {idx}. Original idle duration: {idle_date_elem.text}")
                else:
                    min = min+1
                    idle_date_elem.text = total_idle_dur.strftime('%Y-%m-%d %H:%M:%S')
                 
            if total_session_dur:
                session_date_elem = elem.find('total_sess_dur')
                if session_date_elem is not None and session_date_elem.text is not None:
                    try:
                        date_obj = datetime.strptime(session_date_elem.text, '%Y-%m-%d %H:%M:%S')
                        new_date_obj = total_session_dur - date_obj
                        if idx == min:
                            value = new_date_obj.total_seconds() / 60
                            min = -1
                        new_date1 = date_obj + timedelta(minutes=value)
                        session_date_elem.text = new_date1.strftime('%Y-%m-%d %H:%M:%S')
                    except OverflowError:
                        st.error(f"Date calculation overflow at index {idx}. Original idle duration: {session_date_elem.text}")
                else:
                    min = min+1
                    session_date_elem.text = total_session_dur.strftime('%Y-%m-%d %H:%M:%S')
           
            with cols[col_idx % 4].expander(f"#### Object {idx}", expanded=True):
                st.markdown(f"""
                **Product**: {elem.find('norm_product').get('display_value') if elem.find('norm_product') is not None else 'N/A'}  
                **Source**: {elem.find('source').text if elem.find('source') is not None else 'N/A'}  
                **Created on**: {elem.find('sys_created_on').text if elem.find('sys_created_on') is not None else 'N/A'}  
                **Updated on**: {elem.find('sys_updated_on').text if elem.find('sys_updated_on') is not None else 'N/A'}  
                **Idle Duration**: {elem.find('total_idle_dur').text if elem.find('total_idle_dur') is not None else 'N/A'}  
                **Session Duration**: {elem.find('total_sess_dur').text if elem.find('total_sess_dur') is not None else 'N/A'}  
                **Usage Date**: {elem.find('usage_date').text if elem.find('usage_date') is not None else 'N/A'}  
                """)
            col_idx += 1

    return tree

#Function for concurrent usage 
def parse_concurrent_usage(tree, root,min,max, new_source=None, new_date=None):
    
    st.write("  ")
    cols = st.columns(4)  # Adjust the number of columns as needed
    col_idx = 0
    value = 0
 
    for idx, elem in enumerate(root.findall('.//samp_eng_app_concurrent_usage'), 1):
 
        if ((idx <= max) and (idx >= min)):
            if new_source:
                source_elem = elem.find('source')
                if source_elem is None:
                    source_elem = ET.SubElement(elem, 'source')
                source_elem.text = new_source
            if new_date:
                concurrent_date_elem = elem.find('usage_date')
                if concurrent_date_elem is not None and concurrent_date_elem.text is not None:
                    try:
                        date_obj = datetime.strptime(concurrent_date_elem.text, '%Y-%m-%d')
                        new_date_obj = new_date - date_obj.date()
                        if idx == min:
                            value = new_date_obj.days
                            min = -1
                        new_date1 = date_obj + timedelta(days = value)
                        concurrent_date_elem.text = new_date1  
                        concurrent_date_elem.text = concurrent_date_elem.text.strftime('%Y-%m-%d')
                    except ValueError as e:
                        st.error(f"Error parsing date at index {idx}: {str(e)}")
                else:
                    min = min+1
                    concurrent_date_elem.text = new_date.strftime('%Y-%m-%d')
           
            with cols[col_idx % 4].expander(f"#### Object {idx}", expanded=True):
                st.markdown(f"""
                **License Name**: {elem.find('license').get('display_value') if elem.find('license') is not None else 'N/A'}  
                **Source**: {elem.find('source').text if elem.find('source') is not None else 'N/A'}  
                **Usage Date**: {elem.find('usage_date').text if elem.find('usage_date') is not None else 'N/A'}  
                **Created on**: {elem.find('sys_created_on').text if elem.find('sys_created_on') is not None else 'N/A'}  
                **Updated on**: {elem.find('sys_updated_on').text if elem.find('sys_updated_on') is not None else 'N/A'}  
                """)
            col_idx += 1
   
    return tree
 
#Function for Denial 
def parse_denial(tree,root,min,max,new_source=None, new_date = None):

    st.write("  ")
    cols = st.columns(4)  # Adjust the number of columns as needed
    col_idx = 0
    value = 0
    for idx, elem in enumerate(root.findall('.//samp_eng_app_denial'), 1):
 
        if ((idx <= max) and (idx >= min)):  #Condition for the slider
            if new_source:
                source_elem = elem.find('source')
                if source_elem is None:
                    source_elem = ET.SubElement(elem, 'source')
                source_elem.text = new_source
            if new_date:
                denial_date_elem = elem.find('denial_date')
                if denial_date_elem is not None and denial_date_elem.text is not None:
                    try:
                        date_obj = datetime.strptime(denial_date_elem.text, '%Y-%m-%d')
                        new_date_obj = new_date - date_obj.date()        
                        if idx == min:
                            value = new_date_obj.days
                            min = -1
                        new_date1 = date_obj + timedelta(days=value)
                        denial_date_elem.text = new_date1.strftime('%Y-%m-%d')
                    except ValueError as e:
                        st.error(f"Error parsing date at index {idx}: {str(e)}")
                else:
                    min = min+1
                    denial_date_elem.text = new_date.strftime('%Y-%m-%d')
                
            
            with cols[col_idx % 4].expander(f"#### Object {idx}", expanded=True):
                st.markdown(f"""
                **Denial Date**: {elem.find('denial_date').text if elem.find('denial_date') is not None else 'N/A'}  
                **Computer Name**: {elem.find('computer').get('display_value') if elem.find('computer') is not None else 'N/A'}  
                **Product**: {elem.find('norm_product').get('display_value') if elem.find('norm_product') is not None else 'N/A'}  
                **Source**: {elem.find('source').text if elem.find('source') is not None else 'N/A'}  
                **Created on**: {elem.find('sys_created_on').text if elem.find('sys_created_on') is not None else 'N/A'}  
                **Updated on**: {elem.find('sys_updated_on').text if elem.find('sys_updated_on') is not None else 'N/A'}  
                **Total Denial Count**: {elem.find('total_denial_count').text if elem.find('total_denial_count') is not None else 'N/A'}  
                """)
            col_idx += 1
    
    return tree

#Function for writing the XML file
def save_modified_xml(file_name, tree):
    modified_xml = BytesIO()
    tree.write(modified_xml, encoding='utf-8', xml_declaration=True)
    modified_xml.seek(0)
    st.session_state["modified_xml"] = modified_xml
    return modified_xml

#Main Function 
def main():
    st.image("XML_TitleHeader.png")
    #st.title("ServiceNow ENGINEERING DEMO DATA MODIFIER")
    #st.divider()

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    # Sidebar for file selection and source update
    st.sidebar.title("ServiceNow ENGINEERING DEMO DATA MODIFIER")
    st.sidebar.divider()
    uploaded_files = st.sidebar.file_uploader("Choose XML files", accept_multiple_files=True, type=["xml"])
   
    if uploaded_files:
        file_names = [file.name for file in uploaded_files]
        selected_file_name = st.sidebar.selectbox("Select a file to focus on", file_names)
       
        selected_file = None
        for uploaded_file in uploaded_files:
            if uploaded_file.name == selected_file_name:
                selected_file = uploaded_file
                break
 
        if selected_file:
           
            file_name = selected_file.name

            # Remove the prefix, file extension, and underscores, then convert to proper case
            display_file_name = file_name.replace("samp_eng_app_", "").replace("_", " ").rsplit('.', 1)[0].title()

            st.header(f"Update {display_file_name}")
           
            # Load and parse the XML file
            tree = ET.parse(selected_file)
            root = tree.getroot()
            usage_elements = None
            usage = root.find('.//samp_eng_app_usage_summary[@action="INSERT_OR_UPDATE"]')
            concurrent = root.find('.//samp_eng_app_concurrent_usage[@action="INSERT_OR_UPDATE"]')
            denial = root.find('.//samp_eng_app_denial[@action="INSERT_OR_UPDATE"]')
         
            # Find all <samp_eng_app_concurrent_usage> elements with the specified action attribute
            if usage:
                usage_elements = root.findall('.//samp_eng_app_usage_summary[@action="INSERT_OR_UPDATE"]')
               
            elif concurrent:
                usage_elements = root.findall('.//samp_eng_app_concurrent_usage[@action="INSERT_OR_UPDATE"]')
    
            elif denial:
                usage_elements = root.findall('.//samp_eng_app_denial[@action="INSERT_OR_UPDATE"]')
                # Count the elements
            count = len(usage_elements)

            min_range, max_range = st.sidebar.slider("Select Range",min_value=1, max_value=count,value=(1,count),key="select_range")
            # Fields that are always visible
            new_source = st.sidebar.text_input("New Source Value", "")
           
            st.sidebar.subheader("New Date Value", "")

            # Determine the appropriate label [EDITED  ]
            if denial:
                label = "Update Denial Date"
            else:
                label = "Update Usage Date"

            # Display the date input with the corresponding label
            with st.sidebar.expander(f"#### {label}"):
                st.markdown("")
                new_date = st.date_input("Enter Start Date",value=None)

            if usage:
                with st.sidebar.expander(f"#### {"Update Idle Duration"}"):
                    st.markdown("")
                    idle_dur_date = st.date_input("Enter Idle Duration (Date)",value=None)
                    idle_dur_time = st.time_input("Enter Idle Duration (Time)",value=None,step=60)
                    
                with st.sidebar.expander(f"#### {"Session Duration"}"):
                    st.markdown("")
                    session_dur_date = st.date_input("Enter Session Duration (Date)",value=None)
                    session_dur_time = st.time_input("Enter Session Duration (Time)",value=None,step=60)

                if((idle_dur_date is not None) and (idle_dur_time is not None)):
                    total_idle_dur = datetime.combine(idle_dur_date,idle_dur_time)
                else:
                    total_idle_dur = None            
                if((session_dur_date is not None) and (session_dur_time is not None) ):        
                    total_session_dur = datetime.combine(session_dur_date,session_dur_time)
                else:
                    total_session_dur = None
    
            
            update_button = st.sidebar.button("Update All Fields")
            st.sidebar.divider()

 
            if usage:
                tree = parse_usage_summary(tree,root,min_range,max_range, new_source if update_button else None, new_date if update_button else None,total_idle_dur if update_button else None, total_session_dur if update_button else None)

            elif concurrent:
                tree = parse_concurrent_usage(tree,root,min_range,max_range, new_source if update_button else None, new_date if update_button else None)
           
            elif denial:
                tree = parse_denial(tree,root,min_range,max_range, new_source if update_button else None, new_date if update_button else None)
                
            else:
                st.write(f"Unknown file type: {file_name}")
                return
            
            if update_button:
                modified_xml = save_modified_xml(file_name, tree)
                st.session_state["modified_xml"] = modified_xml
                st.sidebar.download_button(
                label="Download Modified XML",
                data = modified_xml,    
                file_name=file_name,
                mime='application/xml',
                type="primary"
                )
                st.sidebar.divider()
                st.success(":white_check_mark: All fields updated successfully!")

if __name__ == "__main__":
    DDMIcon= Image.open("DDM_Icon.ico")
    st.set_page_config(
        page_title="ServiceNow Engineering Demo Data Modifier",
        layout="wide",
        page_icon=DDMIcon)
    
    st.markdown(sidebar_bg_img, unsafe_allow_html=True)
    st.logo("logoSN.png")
    main()
    
