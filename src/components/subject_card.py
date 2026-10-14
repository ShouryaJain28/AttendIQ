
import streamlit as st
import html as html_utils


def subject_card(name, code, section, stats=None, footer_callback=None):
    safe_name = html_utils.escape(str(name))
    safe_code = html_utils.escape(str(code))
    safe_section = html_utils.escape(str(section))

    card_html = f"""
    <div style="
        background: white;
        border-left: 8px solid #EB459E;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        color: #1e293b;
    ">
        <h3 style="margin: 0; color: #1e293b; font-size: 1.5rem;">
            {safe_name}
        </h3>

        <p style="color: #64748b; margin: 10px 0;">
            Code:
            <span style="
                background: #E0E3FF;
                color: #5865F2;
                padding: 2px 8px;
                border-radius: 5px;
            ">{safe_code}</span>
            | Section: {safe_section}
        </p>
    """

    if stats:
        card_html += """
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        """

        for icon, label, value in stats:
            card_html += f"""
            <div style="
                background: #fff0f8;
                padding: 5px 12px;
                border-radius: 12px;
                font-size: 0.9rem;
                color: #334155;
            ">
                {html_utils.escape(str(icon))}
                <b>{html_utils.escape(str(value))}</b>
                {html_utils.escape(str(label))}
            </div>
            """

        card_html += "</div>"

    card_html += "</div>"

    st.html(card_html)

    if footer_callback is not None:
        footer_callback()
