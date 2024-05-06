def Text(text, font_size='large'):
    latex_text = rf"$\textsf{{\{font_size} {text}}}$"
    return latex_text

tabs_font_css = """
<style>
div[class*="stNumberInput"] label {
  font-size: 26px;
  color: black;
}
</style>
"""

def custom_table_style():
    # CSS to inject contained in a triple-quoted string
    table_style = """
    <style>
    /* Adds styling to the table headers */
    thead tr th {
        background-color: #f0f0f0;  /* Light grey background */
        color: black;               /* Black text */
        font-size: 22pt;           /* Larger font size */
    }
    /* Style for the table data cells */
    tbody tr td {
        color: black;               /* Black text */
        font-size: 20pt;           /* Slightly smaller font size than headers */
    }
    </style>
    """

    # Display the CSS style
    st.markdown(table_style, unsafe_allow_html=True)
