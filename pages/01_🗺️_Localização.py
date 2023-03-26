import streamlit as st
import pandas as pd
import pydeck as pdk


# ---------------------------------------------
# Variaveis globais
dict_cor_categoria = {
    'PUBLICA': [6, 141, 157],
    "PARTICULAR": [83, 28, 179]
}

dict_raio_abrangencia = {
    'Péssimo': 1000,
    'Regular': 525,
    'Excelente': 250
}


# ---------------------------------------------
# Funcoes
@st.cache_data(ttl=0)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

def preprocess_data(df):
    # Preprocessamento dos dados
    # 01 - Substitui , para . nas colunas LATITUDE e LONGITUDE
    df['LATITUDE'] = df['LATITUDE'].str.replace(',','.')
    df['LONGITUDE'] = df['LONGITUDE'].str.replace(',','.')
    # 02 - Cols LATITUDE e LONGITUDE para tipo float
    df['LATITUDE'] = df['LATITUDE'].astype(float)
    df['LONGITUDE'] = df['LONGITUDE'].astype(float)
    df['QNTDE_ESTUDANTES'] = df['QNTDE_ESTUDANTES'].astype(float)
    # 03 - Cria coluna de cores com base na categoria da escola
    df['cor_categoria'] = df['CATEGORIA'].map(dict_cor_categoria)
    return df


# ---------------------------------------------
# Carregamento de dados
df = load_data(st.secrets["public_sheets_localizacao"])
df = preprocess_data(df)


# ---------------------------------------------
# Dados mastigados do dataset
qntd_dados = len(df)
qntd_publicas = len(df[df['CATEGORIA'] == 'PUBLICA'])
qntd_particulares = len(df[df['CATEGORIA'] == 'PARTICULAR'])

# ---------------------------------------------
# Frontend
# ---------------------------------------------

st.markdown("# :world_map: Escolas e Localização")

st.markdown("A localização das escolas municipais é de suma importância, pois a localização das escolas atrelada ao índice de acessibilidade permite que estudantes permaneçam tendo acesso qualificado à educação, sem deixar que o percurso se torne um empecilho na hora dos estudos.")


st.write("Quantidade de escolas mapeadas: ", qntd_dados)

st.markdown("---")
st.markdown("#")

col1, col2 = st.columns(2)

# Input raio de abrangencia
with col1:
    raio_abrangencia = st.select_slider(
        'Selecione o raio de abrangência das escolas por classificação',
        options=['Péssimo', 'Regular', 'Excelente'],
        value="Excelente",
        help="O raio de abrangência escolhido será exibido no mapa abaixo")
# Explicação
if raio_abrangencia == 'Excelente':
    st.success(":white_check_mark: Os círculos mostram o raio de abrangência das escolas em um cenário ideal de cobertura regional das escolas")
elif raio_abrangencia == 'Regular':
    st.warning(":ok: Os círculos mostram o raio de abrangência das escolas em um cenário regular de cobertura regional das escolas")
else:
    st.error(":heavy_exclamation_mark: Os círculos mostram o raio de abrangência das escolas em um cenário péssimo de cobertura regional das escolas")

with col2:
    option = st.selectbox(
    'Categoria da escola',
    ('Todos', 'Pública', 'Particular'))

################
# Map DeckGL
# Define a layer to display on a map
layer_raio_abrangencia = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=False,
    opacity=0.1,
    stroked=True,
    filled=False,
    radius_scale=dict_raio_abrangencia[raio_abrangencia],
    line_width_min_pixels=1,
    get_position="[LONGITUDE, LATITUDE]",
    get_line_color=[0, 0, 0],
)

layer_escola = pdk.Layer(
    "ScatterplotLayer",
    df,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=50,
    radius_min_pixels=1,
    radius_max_pixels=50,
    line_width_min_pixels=1,
    get_position="[LONGITUDE, LATITUDE]",
    get_fill_color="cor_categoria",
    get_line_color=[0, 0, 0],
)
# Set the viewport location
view_state = pdk.ViewState(latitude=-22.385131, longitude=-46.948222, zoom=13, bearing=0, pitch=0)
# Render
map_pydeck = pdk.Deck(
    map_style=None,
    layers=[layer_raio_abrangencia, layer_escola],
    initial_view_state=view_state,
    tooltip={"text": "{ESCOLA}\n{CATEGORIA}"})
st.pydeck_chart(map_pydeck)
################
