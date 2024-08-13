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

    /*new date value*/
    .st-emotion-cache-1gwvy71 h3 {
    font-size: 20px;
    font-weight: bold;
    }   

    .st-emotion-cache-1ag92y2{
    background-color: #E6EDF1; 
    }
    
    /*for paragraph*/
    p, ol, ul, dl {
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
    # Initializion of values
    error = False
    col_idx = 0
    usage_value = 0  
    increment_date_idle = 0
    increment_date_sess = 0
    flag = 0
    min_usage = min
    min_sess = min
    min_idle = min

    for idx, elem in enumerate(root.findall('.//samp_eng_app_usage_summary'), 1):
        #condition for the slider
        if min <= idx <= max:
            #To change the source
            if new_source:
                source_elem = elem.find('source')
                if source_elem is not None:
                    source_elem.text = new_source
            #To change the usage_date in usage
            if new_date:
                usage_date_elem = elem.find('usage_date')
                #condition if the usage_date_elem.text have a value
                if usage_date_elem is not None and usage_date_elem.text is not None:
                    try:
                        #calling the function to adjust the usage date
                        value = adjust_date_element(usage_date_elem,None,None,new_date, idx, min_usage,flag,usage_value)
                        #storing the increment date value to use to other iterations
                        usage_value = value
                    #catching the errors (this will print if there are wrong format in date and if it have date calculation overflow)
                    except ValueError as e:
                        st.error(f"Error parsing date at index {idx}: time data '01-01-2024' does not match format YYYY-MM-DD")
                        error = True
                    except OverflowError:
                        st.error(f"Date calculation overflow at index {idx}. Original idle duration: {usage_date_elem.text}")
                        error = True
                else:
                    #adjusting the min_usage to get the next value if the first value is none
                    min_usage = min_usage+1
                    #replacing all that have the none value into the inputted start date
                    usage_date_elem.text = new_date.strftime('%Y-%m-%d')

            #To change the total_idle_dur in usage
            if total_idle_dur:
                idle_date_elem = elem.find('total_idle_dur')
                #condition if the idle_date_elem.text have a value
                if idle_date_elem is not None and idle_date_elem.text is not None:
                    try:
                        #declaring of adjust variable to use in the function
                        adjust = 0
                        #calling the function to adjust idle_date
                        new_adjust_idle = adjust_session_idle(idle_date_elem,None,total_idle_dur, idx, min_idle,adjust,increment_date_idle)
                        #storing the increment date value to use to other iterations
                        increment_date_idle = new_adjust_idle
                    #catching the errors (this will print if there are wrong format in date and if it have date calculation overflow)
                    except OverflowError:
                        st.error(f"Date calculation overflow at index {idx}. Original idle duration: {idle_date_elem.text}")
                        error = True
                    except ValueError as e:
                        st.error(f"Error parsing date at index {idx}: time data '01-01-2024' does not match format YYYY-MM-DD")
                        error = True
                else:
                    #adjusting the min_idle to get the next value if the first value is none
                    min_idle = min_idle+1
                    #replacing all that have the none value into the inputted start date
                    idle_date_elem.text = total_idle_dur.strftime('%Y-%m-%d %H:%M:%S')

            #To change the total_session_dur in usage
            if total_session_dur:
                session_date_elem = elem.find('total_sess_dur')
                #condition if the session_date_elem.text have a value
                if session_date_elem is not None and session_date_elem.text is not None:
                    try:
                        #declaring of adjust variable to use in the function
                        adjust = 1
                        #calling the function to adjust session_date
                        new_adjust_sess = adjust_session_idle(None,session_date_elem,total_session_dur, idx, min_sess,adjust,increment_date_sess)
                        #storing the increment date value to use to other iterations
                        increment_date_sess = new_adjust_sess
                    #catching the errors (this will print if there are wrong format in date and if it have date calculation overflow)
                    except OverflowError:
                        st.error(f"Date calculation overflow at index {idx}. Original idle duration: {session_date_elem.text}")
                        error = True
                    except ValueError as e:
                        st.error(f"Error parsing date at index {idx}: time data '01-01-2024' does not match format YYYY-MM-DD")
                        error = True
                else:
                    #adjusting the min_idle to get the next value if the first value is none
                    min_sess = min_sess+1
                    #replacing all that have the none value into the inputted start date
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

    return error, tree

#Function for concurrent usage 
def parse_concurrent_usage(tree, root,min,max, new_source=None, new_date=None):
    
    st.write("  ")
    cols = st.columns(4)  # Adjust the number of columns as needed
    col_idx = 0
    flag = 1
    value1 = 0
    error = False
 
    for idx, elem in enumerate(root.findall('.//samp_eng_app_concurrent_usage'), 1):
        #condition for the slider
        if ((idx <= max) and (idx >= min)):
            #to change the source
            if new_source:
                source_elem = elem.find('source')
                if source_elem is None:
                    source_elem = ET.SubElement(elem, 'source')
                source_elem.text = new_source
            #to change the usage_date in concurrent
            if new_date:
                concurrent_date_elem = elem.find('usage_date')
                #condition if the concurrent_date_elem.text have a value
                if concurrent_date_elem is not None and concurrent_date_elem.text is not None:
                    try:
                        #calling the function to adjust the usage_date in concurrent
                        value = adjust_date_element(None,concurrent_date_elem,None,new_date, idx, min,flag,value1)
                        #storing the increment date value to use to other iterations
                        value1 = value
                    #catching the errors (this will print if there are wrong format in date)
                    except ValueError as e:
                        st.error(f"Error parsing date at index {idx}: time data '01-01-2024' does not match format YYYY-MM-DD")
                        error = True
                else:
                    #adjusting the min_idle to get the next value if the first value is none
                    min = min+1
                    #replacing all that have the none value into the inputted start date
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
   
    return error, tree
 
#Function for Denial 
def parse_denial(tree,root,min,max,new_source=None, new_date = None):

    st.write("  ")
    cols = st.columns(4)  # Adjust the number of columns as needed
    col_idx = 0
    flag = 2
    value1 = 0
    error = False 
    for idx, elem in enumerate(root.findall('.//samp_eng_app_denial'), 1):
        #Condition for the slider
        if ((idx <= max) and (idx >= min)):  
            #to change the source
            if new_source:
                source_elem = elem.find('source')
                if source_elem is None:
                    source_elem = ET.SubElement(elem, 'source')
                source_elem.text = new_source
            #to change the denial_date
            if new_date:
                denial_date_elem = elem.find('denial_date')
                #condition if the denial_date_elem.text have a value
                if denial_date_elem is not None and denial_date_elem.text is not None:
                    try:
                        #calling the function to adjust the usage_date in concurrent
                        value = adjust_date_element(None,None,denial_date_elem,new_date, idx, min,flag,value1)
                        #storing the increment date value to use to other iterations
                        value1 = value
                    #catching the errors (this will print if there are wrong format in date)
                    except ValueError as e:
                        st.error(f"Error parsing date at index {idx}: time data '01-01-2024' does not match format YYYY-MM-DD")
                        error = True
                else:
                    #adjusting the min_idle to get the next value if the first value is none
                    min = min+1
                    #replacing all that have the none value into the inputted start date
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
    
    return error, tree

#function to adjust session and idle date
def adjust_session_idle(idle_date_elem,session_date_elem,total_dur, idx, min,adjust,value1):
    
    # Parse the date from the appropriate element's text based on the 'adjust' flag
    if (adjust == 0):
        date_obj = datetime.strptime(idle_date_elem.text, '%Y-%m-%d %H:%M:%S')
    elif (adjust == 1):
        date_obj = datetime.strptime(session_date_elem.text, '%Y-%m-%d %H:%M:%S')
    
    # Calculate the new date by subtracting the parsed date from the total duration
    new_date_obj = total_dur - date_obj
    
    # Adjust the date if the index matches the minimum value
    if idx == min:
        # Convert the difference to minutes and update 'value1'
        value1 = new_date_obj.total_seconds() / 60
        # Set min_value to -1 to prevent further changes
        min = -1  
    # Calculate the new date by adding 'value1' minutes to the original date
    new_date1 = date_obj + timedelta(minutes=value1)
    
    # Update the text of the appropriate date element with the new formatted date
    if (adjust == 0):
        idle_date_elem.text = new_date1.strftime('%Y-%m-%d %H:%M:%S')
    elif (adjust == 1):
        session_date_elem.text = new_date1.strftime('%Y-%m-%d %H:%M:%S')
    #Return the value to retain the increment date
    return value1

#Function to adjust date_element
def adjust_date_element(usage_date_elem,concurrent_date_elem,denial_date_elem, new_date, idx, min,flag,value1):
    
    # Parse the date from the appropriate element's text based on the 'flag' flag
    if (flag == 0):
        date_obj = datetime.strptime(usage_date_elem.text, '%Y-%m-%d')
    elif (flag == 1):
        date_obj = datetime.strptime(concurrent_date_elem.text, '%Y-%m-%d')
    elif (flag == 2):
        date_obj = datetime.strptime(denial_date_elem.text, '%Y-%m-%d')
    
    # Calculate the difference in days between new_date and the parsed date
    new_date_obj = new_date - date_obj.date()
    
    # Adjust the date if the index matches the minimum value
    if idx == min:
        #get the days of the interval
        value1 = new_date_obj.days
        # Set min_value to -1 to prevent further changes
        min = -1  
    # Adjust the date by adding the interval days to the original date
    new_date1 = date_obj + timedelta(days=value1)
    
    # Update the text of the appropriate date element with the new formatted date
    if (flag == 0):
        usage_date_elem.text = new_date1.strftime('%Y-%m-%d')
    elif (flag == 1):
        concurrent_date_elem.text = new_date1.strftime('%Y-%m-%d')
    elif (flag == 2):
        denial_date_elem.text = new_date1.strftime('%Y-%m-%d')

    #Return the value to retain the increment date
    return value1
 
#Function for writing the XML file
def save_modified_xml(file_name, tree):
    modified_xml = BytesIO()
    tree.write(modified_xml, encoding='utf-8', xml_declaration=True)
    modified_xml.seek(0)
    return modified_xml

#Main Function 
def main():
    st.image("XML_TitleHeader.png")
    #st.title("ServiceNow ENGINEERING DEMO DATA MODIFIER")
    #st.divider()
    placeholder = st.empty()

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
    with st.sidebar.expander(f"#### UPLOAD FILES"):
        uploaded_files = st.file_uploader("Choose XML files", accept_multiple_files=True, type=["xml"])
   
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
            with st.sidebar.expander(f"#### Edit Source Value", expanded=True):
                st.markdown("")
                new_source = st.text_input("New Source Value", "")
           
            #st.sidebar.subheader("New Date Value", "")

            # Determine the appropriate label [EDITED  ]
            if denial:
                label = "Edit Denial Date"
            else:
                label = "Edit Usage Date"

            # Display the date input with the corresponding label
            with st.sidebar.expander(f"#### {label}", expanded=True):
                st.markdown("")
                new_date = st.date_input("Enter Start Date",value=None)

            if usage:
                with st.sidebar.expander(f"#### {"Edit Idle Duration"}"):
                    st.markdown("")
                    idle_dur_date = st.date_input("Enter Idle Duration (Date)",value=None)
                    idle_dur_time = st.time_input("Enter Idle Duration (Time)",value=None,step=60)
                    
                with st.sidebar.expander(f"#### {"Session Duration"}"):
                    st.markdown("")
                    session_dur_date = st.date_input("Enter Session Duration (Date)",value=None)
                    session_dur_time = st.time_input("Enter Session Duration (Time)",value=None,step=60)
                #condition to not update if there is one none in either idle_dur_date or idle_dur time
                if((idle_dur_date is not None) and (idle_dur_time is not None)):
                    total_idle_dur = datetime.combine(idle_dur_date,idle_dur_time)
                else:
                    total_idle_dur = None 
                #condition to not update if there is one none in either session_dur_date or session_dur_time
                if((session_dur_date is not None) and (session_dur_time is not None) ):        
                    total_session_dur = datetime.combine(session_dur_date,session_dur_time)
                else:
                    total_session_dur = None
   
            update_button = st.sidebar.button("Update All Fields")
            st.sidebar.divider()

 
            if usage:
                error, tree = parse_usage_summary(tree,root,min_range,max_range, new_source if update_button else None, new_date if update_button else None,total_idle_dur if update_button else None, total_session_dur if update_button else None)

            elif concurrent:
                error, tree = parse_concurrent_usage(tree,root,min_range,max_range, new_source if update_button else None, new_date if update_button else None)
           
            elif denial:
                error, tree = parse_denial(tree,root,min_range,max_range, new_source if update_button else None, new_date if update_button else None)
                
            else:
                st.write(f"Unknown file type: {file_name}")
                return
            
            if update_button:
                modified_xml = save_modified_xml(file_name, tree)
                st.sidebar.download_button(
                label="Download Modified XML",
                data = modified_xml,    
                file_name=file_name,
                mime='application/xml',
                type="primary"
                )
                if error: placeholder.error(":x: Not Updated!")
                else: placeholder.success(":white_check_mark: All fields updated successfully!")

if __name__ == "__main__":
    DDMIcon= Image.open("DDM_Icon.ico")
    st.set_page_config(
        page_title="ServiceNow Engineering Demo Data Modifier",
        layout="wide",
        page_icon=DDMIcon)
    
    st.markdown(sidebar_bg_img, unsafe_allow_html=True)
    st.logo("logoSN.png")
    main()
    
