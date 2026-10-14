
import os
import streamlit as st
import segno
import io


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    # Use the deployed URL when configured; otherwise use localhost.
    app_domain = os.getenv(
        "ATTENDIQ_APP_URL",
        "http://localhost:8501"
    ).rstrip("/")

    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header(f"Join {subject_name}")

    # Generate QR code
    qr = segno.make(join_url, error="m")

    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=4)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info("Copy this link to share on WhatsApp or Email")

        st.link_button(
            "Open Class Link",
            join_url,
            use_container_width=True,
        )

    with col2:
        st.markdown("### Scan to Join")
        st.image(
            out.getvalue(),
            caption="QR code for class joining",
            use_container_width=True,
        )
