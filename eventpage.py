

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt
import pymongo
from dateutil import parser
import time
from collections import defaultdict



#Database Connections
@st.cache_resource
def init_connection():
    try:
        db_username = st.secrets.db_username
        db_password = st.secrets.db_password

        mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)

        client = pymongo.MongoClient(mongo_uri)
        # mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/
        # client=pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
        return client
    except:
        st.write("Connection Could not be Established with database")

client = init_connection()
db= client['EventDatabase']

collection = db['Webinars']


def main():
    
    
    today = datetime.now()
    start_date = today - timedelta(days=today.day - 1)
    # st.sidebar.write(start_date)
    end_date = start_date + timedelta(days=365)
    # st.sidebar.write(end_date)
    column1, column2 = st.columns(2)
    with column1:
        event_input = st.text_input("Enter Webinar/Event")
        event_speaker = st.text_input('Enter Speaker')
        options = ["Select", "profstraining.com", "hcprofs.com", "hospcompliance.com", "bankingeducator.com", "pharmaprofs.com", "webinarsacademy.com"]
        event_website = st.selectbox("Select Website", options)
        event_submit = st.button("Submit", key="submit_event")
    
    with column2:
        event_date = st.date_input("Select date", today, min_value=start_date, max_value=end_date)
        event_time = st.time_input('Select time',dt.time(10, 00) )
        event_duration = st.number_input('Enter Duration(mins)', min_value=0)
        options = ["Select", "Account", "Banking&Finance", "Finance", "FoodSafety", "Healthcare", "HumanResource", "Insurance", "Pharmaceutical"]
        event_industry = st.selectbox("Select Industry", options)
    st.caption("---------------------------------------------------")
    
    columns1, columns2 = st.columns(2)
    month_number=today.month
    month_names = ["January", "February", "March", "April","May","June", "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month_number-1]
    with columns2:
        page_number = st.number_input("Month number:", min_value=1, value=month_number, max_value=12,)
        st.markdown("<br>", unsafe_allow_html=True) 
        page_name = month_names[page_number-1]
    
    with columns1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(page_name)
        st.markdown("<br>", unsafe_allow_html=True) 

    
    # st.sidebar.write(today)
    
    
    st.sidebar.subheader("Event Schedules")
    
    

    if event_submit:
        # parsed_date = parser.parse(event_date)
        # date = parsed_date.strftime("%Y-%m-%d")
        formatted_date = event_date.strftime("%Y-%m-%d")
        formatted_time = event_time.strftime("%H:%M")
        # Find the weekday
        weekday_number = event_date.weekday()
        # Map weekday number to its name
        weekday_names = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekday_name = weekday_names[weekday_number]
        new_document = {'Webinar':event_input,'Speaker': event_speaker, 'Website':event_website, 'Industry': event_industry, 'Date':formatted_date, 'Time':formatted_time, 'Day': weekday_name, 'Duration':event_duration,'Status':'Active'}
        try:                                
            collection.insert_one(new_document)
            st.sidebar.success("Event Created")
        except:
            st.sidebar.error("Failed to create event")
        
        time.sleep(2)
        
        # Refresh the app
        # st.experimental_rerun()  
        
        
    


                       
    # Display the calendar
    days_of_month = 31
    if page_name=='January' or page_name=='March' or page_name=='May' or page_name=='July' or page_name=='August' or page_name=='October' or page_name=='December':
        days_of_month=32
    elif page_name=='February':
        days_of_month=30
    elif page_name=='April' or page_name=='June' or page_name=='May' or page_name=='September' or page_name=='November':
        days_of_month=31
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    # Create a defaultdict to store data for each month
    monthly_data = defaultdict(list)
    events = collection.find({}).sort("Date", pymongo.DESCENDING)
    for event in events:
        id = event.get("_id")
        webinar = event.get("Webinar")
        speaker = event.get("Speaker")
        date = event.get("Date")
        timing = event.get("Time")
        day = event.get('Day')
        duration = event.get('Duration')
        status = event.get('Status')
        industry = event.get('Industry')
        #Website
        website = event.get('Website')
        date_string = date

        # Split the string by "-"
        date_parts = date_string.split("-")

        # Extract the month (index 1 in the split result)
        month_int = int(date_parts[1])
        
    
        day_int = int(date_parts[2])
        # Create a dictionary with event details
        event_data = {
        "ID": id,
        "Webinar": webinar,
        "Speaker": speaker,
        "Timing": timing,
        "Day": day,
        "Duration": duration,
        "Status": status,
        "Industry": industry,
        "Date": date,
        "Website": website,
    }

        # Append the event data to the corresponding month
        monthly_data[month_int].append((day_int, event_data))
    # st.caption(monthly_data)
    
    
    events_for_month = monthly_data.get(page_number, [])
    # st.write(events_for_month)
    
    day_numbers = [entry[0] for entry in events_for_month]
   
       




    def display(events_for_day):
        st.sidebar.write("-------------------------------------")
        # st.session_state.status
        with st.container():
            extracted_dict = events_for_day
            id_value = extracted_dict.get("ID", None)
            webinar_value = extracted_dict.get("Webinar", None)
            speaker_value = extracted_dict.get("Speaker", None)
            timing_value = extracted_dict.get("Timing", None)
            day_value = extracted_dict.get("Day", None)
            duration_value = extracted_dict.get("Duration", None)
            status_value = extracted_dict.get('Status', None)
            date_value = extracted_dict.get('Date', None)
            industry_value = extracted_dict.get('Industry', None)
            website_value = extracted_dict.get('Website', None)
            
            # Convert the string to a datetime object
            original_date = datetime.strptime(date_value, "%Y-%m-%d")
            
            # Format the datetime object as a string with the desired format
            formatted_date_string = original_date.strftime("%d-%m-%Y")

            st.sidebar.write(f"**{webinar_value}**")
            st.sidebar.write(f"**{speaker_value}**")
            st.sidebar.write(f"**{industry_value}**")
            st.sidebar.write(f"**{formatted_date_string}**")
            st.sidebar.write(f"**{website_value}**")
            st.sidebar.write(f"**{timing_value}**")
            st.sidebar.write(f"**{day_value}**")
            st.sidebar.write(f"**{duration_value}**")
            st.sidebar.warning(f"**{status_value}**")
            
            Active_button_key = f"Active_checkbox_{id_value}"
            Postpone_button_key = f"Postpone_checkbox_{id_value}"
            Cancelled_button_key = f"Cancelled_checkbox_{id_value}"
            if status_value =='Active':
                
                st.sidebar.button("Postpone", key=Postpone_button_key, on_click=postpone_callback, args=(id_value, ))
                    

                st.sidebar.button("Cancel", key=Cancelled_button_key, on_click=cancel_callback, args=(id_value, ))
                    

               
            elif status_value =='Postpone':
                st.sidebar.button("Activate", key=Active_button_key, on_click=active_callback, args=(id_value, ))
                    
                # st.session_state.cancel_value = st.sidebar.button("Cancelled", key=Cancelled_button_key)
                st.sidebar.button("Cancel", key=Cancelled_button_key, on_click=cancel_callback, args=(id_value, ))
                    
               
            elif status_value =='Cancelled':
                # st.session_state.active_value = st.sidebar.button("Active", key=Active_button_key, on_click=active_callback, )
                st.sidebar.button("Activate", key=Active_button_key, on_click=active_callback,args=(id_value, ) )
                    

                # st.session_state.postpone_value = st.sidebar.button("Postpone", key=Postpone_button_key)
                st.sidebar.button("Postpone", key=Postpone_button_key, on_click=postpone_callback, args=(id_value, ))
                
            
            
            
    def active_callback(id_value):
        update(id_value, "Active")
        
    def postpone_callback(id_value):
        update(id_value, "Postponed")
        
    def cancel_callback(id_value):
        update(id_value, "Cancelled")
        


    def update(id_value, status_value):   
        try: 
            collection.update_one(
                      {"_id": id_value},
                        {"$set": {"Status": status_value}})
            st.sidebar.success(f"Status Changed to {status_value}")
        except:
            st.siderbar.error("Failed!")
        time.sleep(1)

    

    count=0
    for i in range(1,days_of_month):
        count+=1
        if i in day_numbers:
            matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
            extracted_dict = matching_entry[1]
            webinar_value = extracted_dict.get("Webinar", None)
            id_value = extracted_dict.get("ID", None)
            status_value = extracted_dict.get("Status", None)
            webinar_button_key = f"webinar_button_{count}_{id_value}"
            if webinar_value == 'Holiday':
                message_button = f"{i} Holiday"
            elif (status_value=='Active' and webinar_value!='Holiday'):
                message_button = f"{i} Booked"
            elif (status_value!='Active' and webinar_value!='Holiday'):
                message_button = f"{i} {status_value}"
        
      
        if i%7==1:
            with col1:
                st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                
                with st.container():
                    
                    if i in day_numbers:
                        # matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
                        # extracted_dict = matching_entry[1]
                        # webinar_value = extracted_dict.get("Webinar", None)
                        # id_value = extracted_dict.get("ID", None)
                        # status_value = extracted_dict.get("Status", None)
                        # webinar_button_key = f"webinar_button_{count}_{id_value}"
                        # if webinar_value == 'Holiday':
                        #     message_button = 'Holiday'
                        # elif (status_value=='Active' and webinar_value!='Holiday')
                        #     message_button = 'Booked'
                        # elif (status_value!='Active' and webinar_value!='Holiday')
                        #     message_button = 'status_value'
                    
                        
                        if st.button(message_button, key = webinar_button_key):
                            events_for_day = [event for event in events_for_month if event[0] == i]
                            for count in range(0,len(events_for_day)):
                                display(events_for_day[count][1])


                        # st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    else:
                        st.write(i)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)

            
        # Add spacing between columns
        elif i%7==2:
            with col2:
                st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                with st.container():
                    
                    if i in day_numbers:
                        # matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
                        # extracted_dict = matching_entry[1]
                        # webinar_value = extracted_dict.get("Webinar", None)
                        # id_value = extracted_dict.get("ID", None)
                        # status_value = extracted_dict.get("Status", None)
                        # webinar_button_key = f"webinar_button_{count}_{id_value}"
                        # # webinar_button_key = f"webinar_button_{count}"
                        # # webinar_button_key = f"webinar_button_{id_value}"
                        # # st.write(extracted_dict, key = webinar_button_key)
                        # if webinar_value == 'Holiday':
                        #     message_button = 'Holiday'
                        # elif (status_value=='Active' and webinar_value!='Holiday')
                        #     message_button = 'Booked'
                        # elif (status_value!='Active' and webinar_value!='Holiday')
                        #     message_button = 'status_value'
                        if st.button(message_button, key = webinar_button_key):
                            events_for_day = [event for event in events_for_month if event[0] == i]
                            for count in range(0,len(events_for_day)):
                                display(events_for_day[count][1])
                        
                        # st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    else:
                        st.write(i)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
        elif i%7==3:
            with col3:
                st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                with st.container():
                    if i in day_numbers:
                        # matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
                        # extracted_dict = matching_entry[1]
                        # webinar_value = extracted_dict.get("Webinar", None)
                        # status_value = extracted_dict.get("Status", None)
                        # id_value = extracted_dict.get("ID", None)
                        # webinar_button_key = f"webinar_button_{count}_{id_value}"
                        # # webinar_button_key = f"webinar_button_{count}"
                        # if webinar_value == 'Holiday':
                        #     message_button = 'Holiday'
                        # elif (status_value=='Active' and webinar_value!='Holiday')
                        #     message_button = 'Booked'
                        # elif (status_value!='Active' and webinar_value!='Holiday')
                        #     message_button = 'status_value'
                        if st.button(message_button, key = webinar_button_key):
                            events_for_day = [event for event in events_for_month if event[0] == i]
                            for count in range(0,len(events_for_day)):
                                display(events_for_day[count][1])
                        # st.markdown("<br>", unsafe_allow_html=True)
                        # st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    else:
                        st.write(i)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
        elif i%7==4:
            with col4:
                st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                with st.container():
                    if i in day_numbers:
                        # matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
                        # extracted_dict = matching_entry[1]
                        # webinar_value = extracted_dict.get("Webinar", None)
                        # id_value = extracted_dict.get("ID", None)
                        # status_value = extracted_dict.get("Status", None)
                        # if webinar_value == 'Holiday':
                        #     message_button = 'Holiday'
                        # elif (status_value=='Active' and webinar_value!='Holiday')
                        #     message_button = 'Booked'
                        # elif (status_value!='Active' and webinar_value!='Holiday')
                        #     message_button = 'status_value'
                        # webinar_button_key = f"webinar_button_{count}_{id_value}"
                        # # webinar_button_key = f"webinar_button_{count}"
                        if st.button(message_button, key = webinar_button_key):
                            events_for_day = [event for event in events_for_month if event[0] == i]
                            for count in range(0,len(events_for_day)):
                                display(events_for_day[count][1])
                        # st.markdown("<br>", unsafe_allow_html=True)
                        # st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    else:
                        st.write(i)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
        elif i%7==5:
            with col5:
                st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                with st.container():
                    if i in day_numbers:
                        # matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
                        # extracted_dict = matching_entry[1]
                        # webinar_value = extracted_dict.get("Webinar", None)
                        # id_value = extracted_dict.get("ID", None)
                        # status_value = extracted_dict.get("Status", None)
                        # webinar_button_key = f"webinar_button_{count}_{id_value}"
                        # # webinar_button_key = f"webinar_button_{count}"
                        # if webinar_value == 'Holiday':
                        #     message_button = 'Holiday'
                        # elif (status_value=='Active' and webinar_value!='Holiday')
                        #     message_button = 'Booked'
                        # elif (status_value!='Active' and webinar_value!='Holiday')
                        #     message_button = 'status_value'
                        if st.button(message_button, key = webinar_button_key):
                            events_for_day = [event for event in events_for_month if event[0] == i]
                            for count in range(0,len(events_for_day)):
                                display(events_for_day[count][1])
                        # st.markdown("<br>", unsafe_allow_html=True)
                        # st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    else:
                        st.write(i)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
        elif i%7==6:
            with col6:
                st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                with st.container():
                    if i in day_numbers:
                        # matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
                        # extracted_dict = matching_entry[1]
                        # webinar_value = extracted_dict.get("Webinar", None)
                        # id_value = extracted_dict.get("ID", None)
                        # status_value = extracted_dict.get("Status", None)
                        # webinar_button_key = f"webinar_button_{count}_{id_value}"
                        # # webinar_button_key = f"webinar_button_{count}"
                        # if webinar_value == 'Holiday':
                        #     message_button = 'Holiday'
                        # elif (status_value=='Active' and webinar_value!='Holiday')
                        #     message_button = 'Booked'
                        # elif (status_value!='Active' and webinar_value!='Holiday')
                        #     message_button = 'status_value'
                        if st.button(message_button, key = webinar_button_key):
                            events_for_day = [event for event in events_for_month if event[0] == i]
                            for count in range(0,len(events_for_day)):
                                display(events_for_day[count][1])
                        # st.markdown("<br>", unsafe_allow_html=True)
                        # st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    else:
                        st.write(i)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
        elif i%7==0:
            with col7:
                st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                with st.container():
                    if i in day_numbers:
                        # matching_entry = next((entry for entry in events_for_month if entry[0] == i), None)
                        # extracted_dict = matching_entry[1]
                        # webinar_value = extracted_dict.get("Webinar", None)
                        # id_value = extracted_dict.get("ID", None)
                        # status_value = extracted_dict.get("Status", None)
                        # webinar_button_key = f"webinar_button_{count}_{id_value}"
                        # # webinar_button_key = f"webinar_button_{count}"
                        # if webinar_value == 'Holiday':
                        #     message_button = 'Holiday'
                        # elif (status_value=='Active' and webinar_value!='Holiday')
                        #     message_button = 'Booked'
                        # elif (status_value!='Active' and webinar_value!='Holiday')
                        #     message_button = 'status_value'
                        if st.button(message_button, key = webinar_button_key):
                            events_for_day = [event for event in events_for_month if event[0] == i]
                            for count in range(0,len(events_for_day)):
                                display(events_for_day[count][1])
                        # st.markdown("<br>", unsafe_allow_html=True)
                        # st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    else:
                        st.write(i)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                        st.markdown("&nbsp;&nbsp;&nbsp;", unsafe_allow_html=True)
                    
 
   
