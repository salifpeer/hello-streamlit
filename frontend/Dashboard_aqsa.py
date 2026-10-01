import streamlit as st
import pandas as pd

tab1, tab2, tab3 = st.tabs(["My Dashboard", "Details", "Leaves"])

with st.sidebar:

    c1, c2 = st.columns([5, 3])

    with c1:
        st.write(" ")

    with c2:
        st.sidebar.title("My dashboard")

        st.sidebar.image(
            "https://th.bing.com/th/id/OIP.G37tgeQqSNt7v2oPfj9ltQHaE7?w=205&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3",
            width=100
        )

        st.sidebar.write("name")
        st.sidebar.write("id")
        st.sidebar.write("email")

        st.sidebar.button("Sign out", type="primary")


with tab1:

    col1, con, col2 = st.columns([3, 3, 3])

    with col1:st.button("Apply Leave",width=100,type="primary")

    with con:st.button("Check in",type="primary",width=100)

    with col2:st.button("Apply WFH",width=100,type="primary")

    st.subheader("Check-in and check-out Details Report")

    cont1 = st.container(border=True)

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
                key="checkout_1",
                use_container_width=True
            )

        with col2:
            st.button(
                "Take Break",
                key="break_1",
                use_container_width=True
            )

        with col3:
            st.button(
                "Resume",
                key="resume_1",
                use_container_width=True
            )

        with col4:
            st.write("CBXNS381 - Salif Peer")

        with col5:
            st.write("Checked In")

        with col6:
            st.write("24-Sep-2026 09:48 AM")

        with col7:
            st.write("-")

        col1, col2, col3, col4, col5, col6, col7 = st.columns(
            [2, 2, 2, 2, 1.5, 2.5, 2.5]
        )

        with col1:
            st.button(
                "Check Out",
                key="checkout_2",
                use_container_width=True
            )

        with col2:
            st.button(
                "Take Break",
                key="break_2",
                use_container_width=True
            )

    


with tab2:

    st.title("My Details")

    data = {}

    associate_photo = data.get("associate_photo", "")
    associate_id = data.get("associate_id", "")
    associate_name = data.get("associate_name", "")
    official_email = data.get("official_email", "")
    mobile_number = data.get("mobile_number", "")

    details = pd.DataFrame([
        {
            "Associate Photo": associate_photo,
            "Associate ID": associate_id,
            "Associate Name": associate_name,
            "Official Email": official_email,
            "Mobile Number": mobile_number
        }
    ])

    st.dataframe(details,column_config={
            "Associate Photo": st.column_config.ImageColumn(
                "Associate Photo",
                width="small"
            ),
            "Associate ID": st.column_config.TextColumn(
                "Associate ID"
            ),
            "Associate Name": st.column_config.TextColumn(
                "Associate Name"
            ),
            "Official Email": st.column_config.TextColumn(
                "Official Email"
            ),
            "Mobile Number": st.column_config.TextColumn(
                "Mobile Number"
            )
        },
        hide_index=True,
        use_container_width=True
    )
with tab3:

    st.title("Leaves")