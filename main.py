import streamlit as st
import pandas as pd



st.set_page_config(page_title="BBTS", page_icon="BancodoBrasil.Logomarca.VersãoPrincipal.Amarelo.RGB.png",layout="wide")


# # Carregar o dataframe do arquivo Excel
@st.cache_data
def load_data_BBTS():
    df = pd.read_excel("Mapeamento de APTs - BBTS e BBA.xlsx", sheet_name='BBTS')
    df = df.reset_index(drop=True)
    return(df)

@st.cache_data
def load_data_BBA():
    df = pd.read_excel("Mapeamento de APTs - BBTS e BBA.xlsx", sheet_name='BBA')
    df = df.reset_index(drop=True)
    return(df)

if st.button("BBTS"):
     df = load_data_BBTS()
if st.button("BBA"):
     df = load_data_BBA()

with st.sidebar:
    st.image("BancodoBrasil.Logomarca.VersãoPrincipal.Amarelo.RGB.png", use_column_width=True,  output_format="PNG")
    # Criar filtro de múltipla escolha
    selected_options = st.multiselect('Escolha as opções desejadas:', ['Finance', 'Public Administration', 'Information'], default=['Finance','Public Administration', 'Information'])
    #selected_options = st.sidebar.multiselect('Escolha as opções desejadas:', ['Finance', 'Public Administration', 'Information'], default=['Finance'])


# Função para filtrar o dataframe com base nas opções escolhidas
def filter_data(df, options):
    filtered_values = pd.DataFrame(columns=['Value', 'Options'])
    for option in options:
        if option in df.columns:
            unique_values = df[option].dropna().unique()
            for value in unique_values:
                options_list = [opt for opt in options if value in df[opt].dropna().values]
                if len(options_list) > 1:
                    options_str = ', '.join(options_list)
                    filtered_values = pd.concat([filtered_values, pd.DataFrame({'Value': [value], 'Options': [options_str]})], ignore_index=True)
                elif len(options_list) == 1:
                    filtered_values = pd.concat([filtered_values, pd.DataFrame({'Value': [value], 'Options': [options_list[0]]})], ignore_index=True)
    return filtered_values.drop_duplicates(subset='Value')


#df = load_data_BBTS()

# def filter_data(df, options):
#     filtered_df = pd.DataFrame()
#     for option in options:
#         if option in df.columns:
#             filtered_df = pd.concat([filtered_df, df.loc[:, df.columns == option]])
#     filtered_df = filtered_df.melt(var_name='Option', value_name='Value')
#     filtered_df = filtered_df.drop_duplicates(subset='Value')
#     return filtered_df


# # Carregar o dataframe
# file_path = 'caminho/para/seu/arquivo.xlsx'


col1,col2 = st.columns(2)
st.divider()
col3, col4 = st.columns(2) 
with col1:
    st.image("BancodoBrasil.Logomarca.VersãoPrincipal.Amarelo.RGB.png", use_column_width=False,  output_format="PNG")
    


with col2:
    st.markdown("<p style='color: yellow; font-size: 60px;'>Grupos Hackers que <br> atacam empresas semelhantes à <br> BBTS e ao BBA.</p>", unsafe_allow_html=True)
   #Grupos Hackers que atacam empresas semelhantes à BBTS e ao BBA



# with col3:
#     # Criar filtro de múltipla escolha
#     #selected_options = st.multiselect('Escolha as opções desejadas:', ['Finance', 'Public Administration', 'Information'])
#     df=df.reset_index (drop=True)
#     df

with col4:
     # Aplicar o filtro e mostrar o resultado
    if selected_options:
        filtered_df = filter_data(df, selected_options)
    
        st.write(filtered_df)
    else:
        st.write('Por favor, selecione pelo menos uma opção.')
