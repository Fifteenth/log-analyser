import streamlit as st

def sidebar_navigation():
    """Renders the sidebar navigation and returns the selected page."""

    # Sidebar Styling
    st.markdown(
        """
        <style>
        /* Reduce top padding of the whole sidebar */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: px !important;
        }

        /* Navigation title styling */
        .sidebar-title {
            font-size: 22px;
            font-weight: 600;
            color: #333;
            padding-bottom: 4;
            margin-top: 0px;
        }

        /* Radio button styling */
        div[data-testid="stSidebar"] label {
            font-size: 20px;
            font-weight: 500;
            margin-bottom: 12px !important;
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar title
    st.sidebar.markdown('<div class="sidebar-title">🧭 Navigation</div>', unsafe_allow_html=True)

    # Page options with icons
    nav_options = {
        "Log Analysis": "🔍 Log Analysis",
        "About Us": "ℹ️ About Us",
        "Methodology": "📚 Methodology"
    }

    # Show radio without label
    page_display = st.sidebar.radio(label="", options=list(nav_options.values()))
    page_key = [k for k, v in nav_options.items() if v == page_display][0]

    return page_key
