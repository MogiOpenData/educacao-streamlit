import streamlit as st

# Variaveis globais

# Carregamento de dados

# Funcoes



# ---------------------------------------------
# Configuracoes
st.set_page_config(
    page_title="Educação Brasileira",
    page_icon=":open_book:",
    layout="wide"
)

# ---------------------------------------------
# Frontend
# ---------------------------------------------


with st.sidebar:
    st.markdown("Menu lateral")
    


st.markdown("# :book: Educação no Brasil")
st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum")





# Hide 'made with streamlit'
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)