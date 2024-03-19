import streamlit as st
import pandas as pd



st.set_page_config(page_title="BBTS", page_icon="BancodoBrasil.Logomarca.VersãoPrincipal.Amarelo.RGB.png",layout="wide")


# # Carregar o dataframe do arquivo Excel
@st.cache_data
def load_data():
    df = pd.read_excel("Mapeamento de APTs - BBTS e BBA.xlsx", sheet_name='BBA')
    df = df.reset_index(drop=True)
    return(df)

@st.cache_data
def load_data_filter():
    df = pd.read_csv("Mapeamento_APTs relacionados bba.csv", sep=';')
    return(df)

# if st.button("BBTS"):
#      df = load_data_BBTS()
# if st.button("BBA"):
#      df = load_data_BBA()

with st.sidebar:
    st.image("BancodoBrasil.Logomarca.VersãoPrincipal.Amarelo.RGB.png", use_column_width=True,  output_format="PNG")
    # Criar filtro de múltipla escolha
    selected_options = st.multiselect('Escolha as opções desejadas:', ['Finance', 'Public Administration', 'Information'])
    #selected_options = st.sidebar.multiselect('Escolha as opções desejadas:', ['Finance', 'Public Administration', 'Information'], default=['Finance'])

# NUNCA RETIRAR
# # Função para filtrar o dataframe com base nas opções escolhidas
# def filter_all_data(df, options):
#     filtered_values = pd.DataFrame(columns=['Value', 'Options'])
#     for option in options:
#         if option in df.columns:
#             unique_values = df[option].dropna().unique()
#             for value in unique_values:
#                 options_list = [opt for opt in options if value in df[opt].dropna().values]
#                 if len(options_list) > 1:
#                     options_str = ', '.join(options_list)
#                     filtered_values = pd.concat([filtered_values, pd.DataFrame({'Value': [value], 'Options': [options_str]})], ignore_index=True)
#                 elif len(options_list) == 1:
#                     filtered_values = pd.concat([filtered_values, pd.DataFrame({'Value': [value], 'Options': [options_list[0]]})], ignore_index=True)
#     return filtered_values.drop_duplicates(subset='Value')


def filter_all_data(df, options):
    if len(options) == 0:
        return pd.DataFrame(columns=['Group', 'Áreas'])
    
    filtered_values = pd.DataFrame(columns=['Group', 'Áreas'])
    
    common_values = None
    for option in options:
        if option in df.columns:
            unique_values = set(df[option].dropna().unique())
            if common_values is None:
                common_values = unique_values
            else:
                common_values = common_values.intersection(unique_values)
    
    data = []
    for value in common_values:
        options_list = [opt for opt in options if value in df[opt].dropna().values]
        options_str = ', '.join(options_list)
        data.append({'Group': value, 'Áreas': options_str})
    
    filtered_values = pd.DataFrame(data)
    return filtered_values.drop_duplicates(subset='Group')


# # Função para filtrar o dataframe com base nas opções escolhidas com somente o que há em comum
# def filter_data(df, options):
#     filtered_values = pd.DataFrame(columns=['Value'])
#     for option in options:
#         if option in df.columns:
#             unique_values = df[option].dropna().unique()
#             for value in unique_values:
#                 if all(df[opt].str.contains(value, na=False) for opt in options if opt != option):
#                     filtered_values = pd.concat([filtered_values, pd.DataFrame({'Value': [value]})], ignore_index=True)
#     return filtered_values.drop_duplicates()



# def filter_data(df, options):
#     filtered_df = pd.DataFrame()
#     for option in options:
#         if option in df.columns:
#             filtered_df = pd.concat([filtered_df, df.loc[:, df.columns == option]])
#     filtered_df = filtered_df.melt(var_name='Option', value_name='Value')
#     filtered_df = filtered_df.drop_duplicates(subset='Value')
#     return filtered_df

# def filter_data(df, options):
#     if not options:
#         return pd.DataFrame()  # Retorna DataFrame vazio se nenhuma opção for selecionada
    
#     filters = []  # Lista para armazenar as condições de filtro para cada opção selecionada
#     for option in options:
#         if option in df.columns:
#             filters.append(df[option].notna())  # Adiciona a condição de não-nulo para a coluna da opção
        
#     if not filters:
#         return pd.DataFrame()  # Retorna DataFrame vazio se nenhuma coluna de filtro for encontrada
    
#     filtered_mask = pd.concat(filters, axis=1).all(axis=1)  # Cria uma máscara para linhas que atendem a todos os filtros
#     filtered_df = df[filtered_mask]  # Aplica a máscara ao DataFrame original
    
#     # Retorna somente os valores únicos que aparecem em todas as colunas filtradas
#     common_values = filtered_df.dropna(axis=1).stack().value_counts()
#     common_values = common_values[common_values == len(options)].index.tolist()
    
#     return pd.DataFrame({'Value': common_values})

def filter_data(df, options):
    if not options:
        return pd.DataFrame()  # Retorna DataFrame vazio se nenhuma opção for selecionada
    
    filtered_values = pd.DataFrame(columns=['Value'])
    for option in options:
        if option in df.columns:
            option_values = df[option].dropna().unique()  # Valores únicos na coluna da opção
            if filtered_values.empty:
                filtered_values = pd.DataFrame({'Value': option_values})
            else:
                filtered_values = pd.merge(filtered_values, pd.DataFrame({'Value': option_values}), on='Value', how='inner')
    
    return filtered_values


# # Carregar o dataframe
# file_path = 'caminho/para/seu/arquivo.xlsx'
df = load_data()
df_relacionado = load_data_filter()


col1,col2 = st.columns(2)
st.divider()
col3, col4 = st.columns(2) 
with col1:
    st.image("BancodoBrasil.Logomarca.VersãoPrincipal.Amarelo.RGB.png", use_column_width=False,  output_format="PNG")
    


with col2:
    st.markdown("<p style='color: yellow; font-size: 60px;'>Grupos Hackers que <br> atacam empresas semelhantes a <br> BBA .</p>", unsafe_allow_html=True)
   #Grupos Hackers que atacam empresas semelhantes à BBTS e ao BBA



with col3:
#     # Criar filtro de múltipla escolha
#     #selected_options = st.multiselect('Escolha as opções desejadas:', ['Finance', 'Public Administration', 'Information'])
     # Aplicar o filtro e mostrar o resultado
    st.table(df_relacionado)
    #st.dataframe(df_relacionado,hide_index=True)

with col4:
    # Aplicar o filtro e mostrar o resultado
    if selected_options:
        filtered_df = filter_all_data(df, selected_options)
        filtered_df = filtered_df.reset_index(drop=True)
        #st.table(filtered_df)
        st.dataframe(filtered_df,hide_index=True)
    else:
        st.write('Por favor, selecione pelo menos uma opção.')


    # if selected_options:
    #     filtered_df = filter_data(df, selected_options)
    #     st.write(filtered_df)
    # else:
    #     st.write('Por favor, selecione pelo menos uma opção.')

    # df=df.reset_index (drop=True)
    # df