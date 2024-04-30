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
