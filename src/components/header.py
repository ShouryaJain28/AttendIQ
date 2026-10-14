import streamlit as st
from textwrap import dedent

LOGO_URL = "https://i.ibb.co/YTYGn5qV/logo.png"



def header_home():
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:30px;">
            <img src="{LOGO_URL}"
                 alt="AttendIQ Logo"
                 style="height:100px; width:auto;">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            text-align: center;
            color: #FFFFFF;
            font-size: 56px;
            font-weight: 900;
            line-height: 1.2;
            margin: 15px 0 25px 0;
        ">AttendIQ</div>
        """,
        unsafe_allow_html=True,
    )




def header_dashboard():
    col1, col2 = st.columns([1, 3], vertical_alignment="center")

    with col1:
        st.image(LOGO_URL, width=85)

    with col2:
        st.markdown(
            "<div style='color:#5865F2; font-size:32px; "
            "font-weight:700; line-height:1.2;'>AttendIQ</div>",
            unsafe_allow_html=True,
        )

