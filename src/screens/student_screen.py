import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier,
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
)
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {student_data['name']}")

        if st.button(
            "Logout",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
        ):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("student_data", None)
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)

    with c1:
        st.header("Your Enrolled Subjects")

    with c2:
        if st.button(
            "Enroll in Subject",
            type="primary",
            width="stretch",
            key=f"enroll_subject_{student_id}",
        ):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your enrolled subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log["subject_id"]

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]["total"] += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    if not subjects:
        st.info("You are not enrolled in any subjects yet.")
    else:
        cols = st.columns(2)

        for i, sub_node in enumerate(subjects):
            sub = sub_node.get("subjects")

            if not sub:
                st.warning("Subject details could not be loaded for one enrollment.")
                continue

            sid = sub["subject_id"]

            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll_button(
                current_sid=sid,
                current_sub=sub,
            ):
                if st.button(
                    "Unenroll from this course",
                    type="tertiary",
                    width="stretch",
                    icon=":material/delete_forever:",
                    key=f"unenroll_{student_id}_{current_sid}",
                ):
                    unenroll_student_to_subject(student_id, current_sid)
                    st.toast(f"Unenrolled from " f"{current_sub['name']} successfully!")
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=[
                        ("📅", "Total", stats["total"]),
                        ("✅", "Attended", stats["attended"]),
                    ],
                    footer_callback=unenroll_button,
                )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    # FaceID heading with a lighter, cleaner font
    
    # FaceID heading with a lighter, cleaner font
    st.markdown(
        """
        <style>
        h2.faceid-login-title,
        h2.faceid-login-title * {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 28px !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
            letter-spacing: 0.2px !important;
            margin-bottom: 0 !important;
        }

        div[data-testid="stMarkdownContainer"] p.faceid-camera-instruction {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 400 !important;
        }
        </style>

        <h2 class="faceid-login-title" style="text-align:center;">
            Login using FaceID
        </h2>
        """,
        unsafe_allow_html=True,
    )


    st.space()
    st.space()

    show_registration = False

    # Camera instruction in black
    st.markdown(
        """
        <p class="faceid-camera-instruction">
            Position your face in the center
        </p>
        """,
        unsafe_allow_html=True,
    )

    photo_source = st.camera_input("")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found!")

            elif num_faces > 1:
                st.warning("Multiple faces found")

            elif detected:
                student_id = list(detected.keys())[0]
                all_students = get_all_students()

                student = next(
                    (s for s in all_students if s["student_id"] == student_id),
                    None,
                )

                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student

                    st.toast(f"Welcome back {student['name']}")

                    time.sleep(1)
                    st.rerun()

            else:
                st.info("Face not recognized! You might be a new student.")
                show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Register new Profile")

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Hamza Rizvi",
            )

            st.subheader("Optional: Voice Enrollment")
            st.info("Enroll your voice for voice-only attendance.")

            audio_data = None

            try:
                audio_data = st.audio_input(
                    "Record a short phrase like I am present, " "My name is Akash."
                )
            except Exception:
                st.error("Audio data failed!")

            if st.button(
                "Create Account",
                type="primary",
                key="create_student_account",
            ):
                if new_name:
                    with st.spinner("Creating profile..."):
                        img = np.array(Image.open(photo_source))

                        encodings = get_face_embeddings(img)

                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None

                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )

                            if response_data:
                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]

                                st.toast(f"Profile created! Hi {new_name}!")

                                time.sleep(1)
                                st.rerun()

                        else:
                            st.error(
                                "Couldn't capture your facial "
                                "features for registration."
                            )
                else:
                    st.warning("Please enter your name!")

    footer_dashboard()
