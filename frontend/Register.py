import streamlit as st
import requests
from datetime import date

# from frontend import sign_in

def register():
    BACKEND_URL = "http://127.0.0.1:8000/register/employee"

    st.set_page_config(
        page_title="Employee Registration",
        page_icon="👤",
        layout="wide"
    )

    st.title("Employee Registration")

    st.caption(
        "Please enter your details to create your employee profile."
    )

    with st.form("employee_registration_form"):

        st.subheader("1. Personal Details")

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                full_name = st.text_input(
                    "Full Name",
                    placeholder="Enter your full name"
                )

            with col2:

                email = st.text_input(
                    "Email",
                    placeholder="example@email.com"
                )

            col1, col2 = st.columns(2)

            with col1:

                date_of_birth = st.date_input(
                    "Date of Birth",
                    value=date(2000, 1, 1),
                    min_value=date(1950, 1, 1),
                    max_value=date.today()
                )

            with col2:

                gender = st.selectbox(
                    "Gender",
                    [
                        "Select",
                        "Female",
                        "Male",
                        "Other"
                    ]
                )

            col1, col2 = st.columns(2)

            with col1:

                marital_status = st.selectbox(
                    "Marital Status",
                    [
                        "Select",
                        "Single",
                        "Married"
                    ]
                )

            with col2:

                nationality = st.text_input(
                    "Nationality",
                    value="Indian"
                )

        st.subheader("2. Contact & Address Details")

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                mobile = st.text_input(
                    "Mobile Number",
                    placeholder="Enter 10-digit mobile number"
                )

            with col2:

                alternate_mobile = st.text_input(
                    "Alternate Mobile Number",
                    placeholder="Enter 10-digit mobile number"
                )

            st.write("Present Address")

            present_address = st.text_area(
                "Present Address",
                placeholder="Enter your complete address",
                label_visibility="collapsed"
            )

        st.subheader("3. Account Security")

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter password"
                )

            with col2:

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter password"
                )

        st.write("")

        _, col2, _ = st.columns([1, 1, 1])

        with col2:

            submit = st.form_submit_button(
                "Submit Registration",
                width="stretch",
                type="primary"
            )

    if submit:

        if (
            not full_name.strip()
            or not email.strip()
            or gender == "Select"
            or marital_status == "Select"
            or not nationality.strip()
            or not mobile.strip()
            or not alternate_mobile.strip()
            or not present_address.strip()
            or not password
            or not confirm_password
        ):
            st.error("Please fill all the fields.")

        elif (
            "@" not in email
            or "." not in email
            or email.startswith("@")
            or email.endswith("@")
        ):
            st.error("Please enter a valid email address.")

        elif not mobile.isdigit() or len(mobile) != 10:
            st.error("Mobile number must contain exactly 10 digits.")

        elif (
            not alternate_mobile.isdigit()
            or len(alternate_mobile) != 10
        ):
            st.error(
                "Alternate mobile number must contain exactly 10 digits."
            )

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:
            payload = {
                "full_name": full_name,
                "email": email,
                "date_of_birth": str(date_of_birth),
                "gender": gender,
                "marital_status": marital_status,
                "nationality": nationality,
                "mobile": mobile,
                "alternate_mobile": alternate_mobile,
                "present_address": present_address,
                "password": password
            }

            if st.session_state.get("last_submit_payload") != payload:
                try:
                    response = requests.post(BACKEND_URL, json=payload)
                    try:
                        res_data = response.json()
                    except Exception:
                        res_data = {}

                    st.session_state["last_submit_payload"] = payload
                    st.session_state["last_submit_status"] = response.status_code
                    st.session_state["last_submit_data"] = res_data
                except requests.exceptions.ConnectionError:
                    st.session_state["last_submit_payload"] = payload
                    st.session_state["last_submit_status"] = 503
                    st.session_state["last_submit_data"] = {"detail": "Unable to connect to backend server."}
                except Exception as e:
                    st.session_state["last_submit_payload"] = payload
                    st.session_state["last_submit_status"] = 500
                    st.session_state["last_submit_data"] = {"detail": f"An unexpected error occurred: {e}"}

            status_code = st.session_state.get("last_submit_status")
            res_data = st.session_state.get("last_submit_data", {})

            if status_code == 200:
                st.success(res_data.get("message", "Employee registered successfully!"))
                st.session_state.page = "login"
                st.rerun()
            else:
                error_msg = res_data.get("detail", "Registration failed.")
                st.error(error_msg)