import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="CX Checklist",
    layout="centered",
    initial_sidebar_state="expanded"
)

# === GRUPOS E SUBGRUPOS COM PERGUNTAS NUMERADAS ===
grupos = {
    "Purpose: Assess suitability to drive CX decisions and produce quality data": [
        {
            "nome": "1. Confirm that you need the survey and each question in it",
            "perguntas": [
                "1- Is a CX survey the right tool for your goal?",
                "2- Do you know how the survey will inform decisions about CX?",
                "3- Do you know how you’ll communicate the survey findings to stakeholders?",
                "4- Do you know for each question how the response data will inform CX decisions?",
                "5- Does each question ask about something you don't already know about your customers and their experiences?",
                "6- Is each question applicable to the customer at the time of the survey?",
                "7- Do you know — for each question — how you’ll analyze the responses you receive?",
                "8- Do you have no more than two to six questions for transactional surveys and four to 15 questions for relationship surveys?"
            ]
        },
        {
            "nome": "2. Design questions and answer options that create valid and reliable data",
            "perguntas": [
                "9- Does each question ask about just one thing?",
                "10- Does wording for each question avoid biasing the respondent?",
                "11- Do you avoid question types that cause respondent bias?",
                "12- Do you avoid using many different scale types?",
                "13- Are all scales oriented in the same direction?",
                "14- Is each scale labeled clearly?",
                "15- Did you randomize answer options to avoid response bias except where the order of options helps reduce cognitive load?",
                "16- Are questions “optional” if you're not sure that customers know the answer?"
            ]
        }
    ],
    "Ease: Assess design for respondents’ ease of completion": [
    {
        "nome": "3. Give customers a sense of progress and control",
        "perguntas": [
            "17- Are you communicating the purpose of the survey to customers?",
            "18- Do you give respondents a sense of how long the survey will take?",
            "19- Is there an order to the question that a customer can discern?",
            "20- Do you let customers decide which questions they want to answer?",
            "21- Do you give customers a chance to provide additional feedback that they want to share?",
            "22- Do your open-ended questions encourage a detailed response?",
            "23- Do you give customers a sense of the progress they make along the survey?",
            "24- Do you include mental breaks or transitions if the survey is long or when the topic is changing?",
            "25- Are error messages clear enough to let customers progress in the survey?"
        ]
    },
    {
        "nome": "4. Word questions and answer options to avoid confusion and ambiguity",
        "perguntas": [
            "26- Can respondents easily understand each question and answer option, even if they are distracted?",
            "27- Is each question and answer option so precise that each respondent interprets it the same way?",
            "28- Are your answer options collectively exhaustive?",
            "29- Do you avoid question types that cause cognitive load for respondents?",
            "30- Do you avoid scale types that cause excessive cognitive load for respondents?",
            "31- Does the question text match the scale and answer options used?"
        ]
    }
],

    "Governance: Assess adherence to usability, accessibility, and communication standards": [
    {
        "nome": "5. Apply accessibility and usability standards",
        "perguntas": [
            "32- Does your survey meet accessibility criteria?",
            "33- Does the use of design elements in the survey minimize perceived burden?",
            "34- Does your survey display correctly on mobile devices, desktops, and within messaging platforms?",
            "35- Is your survey available in the languages most spoken by your customers?",
            "36- Have you pretested the survey with colleagues?",
            "37- Have you pretested the survey in the live mode with actual customers?"
        ]
    },
    {
        "nome": "6. Apply guidelines for customer-directed communication",
        "perguntas": [
            "38- Is your survey 'on brand' — does it look and sound like it came from your organization?",
            "39- Is your survey invitation optimized for passing spam filters?",
            "40- Do you use customers’ preferred communication channels to send surveys?",
            "41- Do you embed surveys in the customer workflow and in existing communications?",
            "42- Are you avoiding surveying individual customers too frequently?",
            "43- Have you checked how many other communications to a customer are scheduled to go out during the same time as your survey?",
            "44- Are your surveys compliant with regulations?"
        ]
    }
]
}


# === ESTADO GLOBAL ===
if "grupo" not in st.session_state:
    st.session_state.grupo = list(grupos.keys())[0]
if "pagina" not in st.session_state:
    st.session_state.pagina = 0
if "respostas" not in st.session_state:
    st.session_state.respostas = {}

st.sidebar.image("logo.webp", width=180)




# === MENU LATERAL ===
st.sidebar.title("Menu de Navegação")
grupo_selecionado = st.sidebar.radio("Escolha o grupo:", list(grupos.keys()))

# Se mudou o grupo no menu, zera a página
if grupo_selecionado != st.session_state.grupo:
    st.session_state.grupo = grupo_selecionado
    st.session_state.pagina = 0

grupo_atual = st.session_state.grupo
subgrupos = grupos[grupo_atual]
pagina = st.session_state.pagina
subgrupo_atual = subgrupos[pagina]

# === EXIBIÇÃO DO GRUPO E SUBGRUPO ===
st.title("CX Survey Quality Checklist")
st.subheader(grupo_atual)
st.header(subgrupo_atual["nome"])

# === FORMULÁRIO ===
for pergunta in subgrupo_atual["perguntas"]:
    chave = f"{grupo_atual}|||{subgrupo_atual['nome']}|||{pergunta}"
    st.session_state.respostas[chave] = st.radio(pergunta, ["Sim", "Não"], key=chave)

# === NAVEGAÇÃO ENTRE SUBGRUPOS ===
if "navegacao" not in st.session_state:
    st.session_state.navegacao = None

col1, col2, col3 = st.columns(3)
with col1:
    if pagina > 0:
        if st.button("⬅️ Anterior"):
            st.session_state.pagina -= 1
            st.session_state.navegacao = "voltar"
            st.rerun()

with col3:
    if pagina < len(subgrupos) - 1:
        if st.button("Próximo ➡️"):
            st.session_state.pagina += 1
            st.session_state.navegacao = "avancar"
            st.rerun()
    else:
        if st.button("✅ Finalizar e Enviar"):
            dados = []
            for chave, resposta in st.session_state.respostas.items():
                partes = chave.split("|||")
                if len(partes) == 3:
                    grupo, subgrupo, pergunta = partes
                    dados.append({
                        "Grupo": grupo,
                        "Subgrupo": subgrupo,
                        "Pergunta": pergunta,
                        "Resposta": resposta
                    })

            df = pd.DataFrame(dados)
            nao = df[df["Resposta"] == "Não"]

            if nao.empty:
                st.success("✅ Todas as perguntas foram respondidas com 'Sim'.")
            else:
                st.warning("⚠️ Perguntas respondidas com 'Não':")
                st.dataframe(nao[["Grupo", "Subgrupo", "Pergunta"]].reset_index(drop=True))

            # csv = df.to_csv(index=False).encode("utf-8")
            # st.download_button("📄 Baixar CSV", data=csv, file_name="respostas_cx.csv", mime="text/csv")

            # Exportar como Excel (.xlsx)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Respostas')

            output.seek(0)  # voltar ao início do arquivo

            st.download_button(
                label="📊 Baixar Excel",
                data=output,
                file_name="respostas_cx.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            


# === TEMA CUSTOMIZADO PARA SIDEBAR ===
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #007FFF;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)
