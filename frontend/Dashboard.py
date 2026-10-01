
import streamlit as st
import requests
from location import location_page

def dashboard():

    URL = "https://k0bfnvp2-8000.inc1.devtunnels.ms"

    if "attendance" not in st.session_state:
        st.session_state.attendance = {
            "message": "",
            "status": "-",
            "checkin_time": "-",
            "checkout_time": "-",
            "break_time": "0:00:00",
            "working_time": "-"
        }

    def checkin():

        employee_id = st.session_state.employee_id

        response = requests.post(
            f"{URL}/checkin",
            params={
                "employee_id": employee_id
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.attendance = data

            st.toast(
                data["message"],
                icon="✅"
            )

        else:

            data = response.json()

            st.error(
                data.get(
                    "detail",
                    "Check-in failed"
                )
            )

    def checkout():

        employee_id = st.session_state.employee_id

        response = requests.post(
            f"{URL}/checkout",
            params={
                "employee_id": employee_id
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.attendance = data

            st.toast(
                data["message"],
                icon="✅"
            )

        else:

            data = response.json()

            st.error(
                data.get(
                    "detail",
                    "Check-out failed"
                )
            )

    def take_break():

        employee_id = st.session_state.employee_id

        response = requests.post(
            f"{URL}/break/start",
            params={
                "employee_id": employee_id
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.attendance = data

            st.toast(
                data["message"],
                icon="☕"
            )

        else:

            data = response.json()

            st.error(
                data.get(
                    "detail",
                    "Unable to start break"
                )
            )

    def resume_break():

        employee_id = st.session_state.employee_id

        response = requests.post(
            f"{URL}/break/resume",
            params={
                "employee_id": employee_id
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state.attendance = data

            st.toast(
                data["message"],
                icon="▶️"
            )

        else:

            data = response.json()

            st.error(
                data.get(
                    "detail",
                    "Unable to resume break"
                )
            )

    if st.session_state.get(
        "location_verified",
        False
    ):

        st.session_state.location_verified = False

        checkin()

    tab1, tab2, tab3 = st.tabs(
        [
            "My Dashboard",
            "Details",
            "Leaves"
        ]
    )

    with tab2:

        st.header("My personal Details")

        response = requests.get(
            f"{URL}/details",
            params={
                "employee_id":
                st.session_state.employee_id
            }
        )

        if response.status_code == 200:

            details = response.json()

            if details:

                st.dataframe(
                    details,
                    use_container_width=True
                )

            else:

                st.info(
                    "No details found."
                )

        else:

            st.error(
                "Unable to fetch details."
            )

    with tab3:

        st.header("Apply for Leave")

        leave_type = st.radio(
            "Select Leave Type",
            [
                "One Day Leave",
                "Multiple Days Leave"
            ]
        )

        if leave_type == "One Day Leave":

            leave_date = st.date_input(
                "Leave Date"
            )

            start_date = leave_date
            end_date = leave_date

        else:

            start_date = st.date_input(
                "Starting Date"
            )

            end_date = st.date_input(
                "Ending Date"
            )

        reason = st.text_area(
            "Reason"
        )

        if st.button(
            "Apply Leave",
            type="primary"
        ):

            if not reason:

                st.warning(
                    "Please enter a reason"
                )

            elif end_date < start_date:

                st.warning(
                    "Ending date cannot be before starting date"
                )

            else:

                response = requests.post(
                    f"{URL}/leave",
                    json={
                        "employee_id":
                        st.session_state.employee_id,
                        "start_date":
                        str(start_date),
                        "end_date":
                        str(end_date),
                        "reason":
                        reason
                    }
                )

                data = response.json()

                st.success(
                    data["message"]
                )

        st.divider()

        st.subheader(
            "My Leave Applications"
        )

        response = requests.get(
            f"{URL}/leaves",
            params={
                "employee_id":
                st.session_state.employee_id
            }
        )

        if response.status_code == 200:

            leaves = response.json()

            if leaves:

                st.dataframe(
                    leaves,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.info(
                    "No leave applications found."
                )

        else:

            st.error(
                "Unable to fetch leave applications."
            )

    with st.sidebar:

        col1, col2, col3 = st.columns(
            [1, 4, 1]
        )

        with col2:

            st.title(
                "My Dashboard"
            )

            st.write(
            "logo.png"
                
                
            )

            st.write(
                st.session_state.full_name
            )

            st.write(
                st.session_state.email
            )

            st.write(
                st.session_state.attendance["status"]
            )

            if st.button(
                "Sign out",
                type="primary"
            ):

                st.session_state.page = "login"

                st.rerun()

    with tab1:

        col1, con, col2 = st.columns(
            [3, 3, 3]
        )

        with col1:

            st.write(" ")
        with con:

            if st.button(
                "Check In",
                type="primary",
                width=100
            ):

                st.session_state.page = "location"

                st.rerun()

        with col2:

            st.write(" ")

        st.subheader(
            "Check-in and check-out Details Report"
        )

        cont1 = st.container(
            border=True
        )

        with cont1:

            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                [2, 2, 2, 2, 1.5, 2.5, 2.5]
            )

            with col1:
                st.write("Check Out")

            with col2:
                st.write("Take Break")

            with col3:
                st.write("Resume Work")

            with col4:
                st.write("Name")

            with col5:
                st.write("Status")

            with col6:
                st.write("Check-In Time")

            with col7:
                st.write("Check-Out Time")

            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                [2, 2, 2, 2, 1.5, 2.5, 2.5]
            )
            
            with col1:
             st.button(
                    "Check Out",
                    on_click=checkout,
                    key="checkout_button",
                    
                    type="secondary"
                )
            with col2:

                 st.button(
            "Take Break",
            on_click=take_break,
            key="break_button",
            use_container_width=True,
            type="secondary"
        )
            

            with col3:

                st.button(
                        "Resume Work",
                        on_click=resume_break,
                        key="resume_button",
                        use_container_width=True,
                        type="primary"
                    )

            with col4:

                st.write(
                    st.session_state.full_name
                )

            with col5:

                st.write(
                    st.session_state.attendance[
                        "status"
                    ]
                )

            with col6:

                st.write(
                    st.session_state.attendance[
                        "checkin_time"
                    ]
                )

            with col7:

                st.write(
                    st.session_state.attendance[
                        "checkout_time"
                    ]
                )

        
        
        
        st.divider()
        container= st.container()
        
        
        with container:
            st.header("My checkin Details")    
           
           
 
 
        employee_id = st.session_state.employee_id
 
        response = requests.get(
         f"{URL}/tabledata",
        params={
            "employee_id": employee_id
        }
    )
 
        if response.status_code == 200:
 
          data = response.json()
 
          rows = []
 
          for date, details in data.items():
 
            rows.append({
                "Date": date,
                "Status": details["status"],
                "Check In": details["checkin"],
                "Check Out": details["checkout"],
                "Break Duration": details["break_duration"],
                "Working Time": details["working_time"]
            })
 
          st.dataframe(
            rows,
            use_container_width=True
        )