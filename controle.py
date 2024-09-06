import streamlit as st
import math
from fpdf import FPDF
from PIL import Image

#  Configurações da página web
logo = 'ufal.png'
img_logo = Image.open(logo)
arquivo = 'ufal.png'
image = Image.open(arquivo)
PAGE_CONFIG = {"page_title": "Web app | UFAL",
               "page_icon": image,
               "layout": "wide",
               "initial_sidebar_state": "auto",
               }

st.set_page_config(**PAGE_CONFIG)
imagem_caminho = 'ufal.png'

st.title('Dimensionamento de Barreiras')
st.subheader('Controle Ambiental')
st.write('Elaborado por: Adriel Lucas Ferreira de Oliveira')
st.write('')

st.number_input('Profundidade da Foz:', min_value=0.0, format='%f', step=1.0, key = 'prof', help='Valor em metros')
calado_barreira = st.session_state.prof * 0.2

with st.container(border=True):
    st.markdown(f'<h4>Calado da Barreira: <span style="color: red;">{calado_barreira:.2f} metros</span></h4>',
                unsafe_allow_html=True)

st.number_input('Velocidade do vento:', min_value=0.0, format='%f', step=1.0, key = 'vvent', help='Km/h')
velocidade_vento_nos = st.session_state.vvent * 0.53996

with st.container(border=True):
    if velocidade_vento_nos < 21:
        st.markdown(
            f'<h4>Velocidade do vento é de: <span style="color: red;">{velocidade_vento_nos:.2f} nós</span>. É indicado o uso de <span style="color: red;">Barreira Tipo Cerca e Tipo Cortina</span></h4>',
            unsafe_allow_html=True)
    elif 21 <= velocidade_vento_nos <= 30:
        st.markdown(
            f'<h4>Velocidade do vento é de: <span style="color: red;">{velocidade_vento_nos:.2f} nós</span>. É indicado o uso de <span style="color: red;">Barreira Tipo Cortina</span></h4>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            f'<h4>Velocidade do vento é de: <span style="color: red;">{velocidade_vento_nos:.2f} nós</span>. Condição desfavorável para o uso de barreiras</h4>',
            unsafe_allow_html=True)

st.number_input('Largura da Foz do Rio:', min_value=0.0, format='%f', step=10.0, key = 'lf', help='m')
dados = {
    1: 75,
    1.2: 60,
    1.4: 45,
    1.75: 35,
    3.7: 15
}

# Input do usuário
velocidade = st.number_input('Velocidade da corrente:', min_value=0.0, format='%f', step=0.1, key='vcor', help='nós')

# Comparação com os dados
def obter_angulo(velocidade):
    # Encontrar a velocidade mais próxima na tabela
    velocidades_disponiveis = sorted(dados.keys())
    for v in velocidades_disponiveis:
        if velocidade <= v:
            return dados[v]
    return "Velocidade fora do intervalo"

# Mostrar o ângulo correspondente
angulo = obter_angulo(velocidade)

# Exibir o ângulo formatado
with st.container(border=True):
    if isinstance(angulo, int):  # Verifica se o valor é um número inteiro
        st.markdown(f'<h4>Ângulo Correspondente: <span style="color: red;">{angulo:.0f}°</span></h4>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<h4>{angulo}</h4>', unsafe_allow_html=True)  # Exibe mensagem para valores fora do intervalo

Bc = 0
if st.session_state.lf > 0 and st.session_state.vcor >= 0:
    Bc = st.session_state.lf * (st.session_state.vcor + 1.5)
    with st.container(border=True):
        st.markdown(f'<h4>Comprimento das Barreiras: <span style="color: red;">{Bc:.0f} metros</span></h4>',
                    unsafe_allow_html=True)
else:
    st.warning("Por favor, preencha os valores de largura da foz e velocidade da corrente corretamente.")

st.number_input('Digite o raio da barreira', min_value=0.0, format='%f', step=0.1, key ='rb', help='metros')

if st.session_state.rb > 0 and calado_barreira > 0 and calado_barreira <= st.session_state.rb:
    theta = 2 * math.acos(1 - (calado_barreira / st.session_state.rb))
    C_submerso = st.session_state.rb * theta
    As = C_submerso * Bc
    Av = (2 * math.pi * st.session_state.rb * Bc) - As
    Fc = 26 * As * (st.session_state.vcor ** 2)
    Fv = 26 * Av * ((velocidade_vento_nos / 40) ** 2)

    with st.container(border=True):
        st.markdown(f'<h4>Carga Suportada, Força da Correnteza: <span style="color: red;">{Fc:.0f} kgf</span></h4>',
                    unsafe_allow_html=True)
        st.markdown(f'<h4>Carga Suportada, Força da Vento: <span style="color: red;">{Fv:.0f} kgf</span></h4>',
                    unsafe_allow_html=True)
elif st.session_state.rb <= 0:
    st.warning("O raio da barreira deve ser maior que zero.")
elif calado_barreira > st.session_state.rb:
    st.warning("O calado da barreira deve ser menor ou igual ao raio da barreira.")

if Bc > 0:
    Na = Bc / 15
    Cc = (st.session_state.prof * 7) / Na
    with st.container(border=True):
        st.markdown(f'<h4>Número de Âncoras: <span style="color: red;">{Na:.0f} âncoras</span></h4>',
                    unsafe_allow_html=True)
        st.markdown(f'<h4>Número de Estacas: <span style="color: red;">{Na:.0f} estacas</span></h4>',
                    unsafe_allow_html=True)
        st.markdown(f'<h4>Número de Boias de Arnique: <span style="color: red;">{Na:.0f} boias</span></h4>',
                    unsafe_allow_html=True)
        st.markdown(f'<h4>Comprimentos de Cabos: <span style="color: red;">{Cc:.2f} metros</span></h4>',
                    unsafe_allow_html=True)
else:
    st.warning("Comprimento das barreiras (Bc) não pode ser zero.")

st.number_input('Tempo de Mobilização:', min_value=0.0, format='%f', step=1.0, key = 'mobt', help='horas')
st.number_input('Tempo de Deslocamento:', min_value=0.0, format='%f', step=1.0, key = 'deslt', help='horas')
st.number_input('Tempo de Instalação:', min_value=0.0, format='%f', step=1.0, key = 'instt', help='horas')
st.number_input('Distância do Derramamento:', min_value=0.0, format='%f', step=10.0, key = 'distd', help='Km')
st.number_input('Velocidade Média de Deslocamento:', min_value=0.0, format='%f', step=10.0, key = 'vd', help='km/h')

if (st.session_state.mobt >= 0 and st.session_state.deslt >= 0 and st.session_state.instt >= 0 and st.session_state.vd > 0):
    Tr = st.session_state.mobt + st.session_state.deslt + st.session_state.instt
    D = st.session_state.vd * (Tr - (st.session_state.mobt + st.session_state.instt))
    toqt = st.session_state.distd / st.session_state.vd

    with st.container(border=True):
        if Tr <= toqt:
            st.markdown(f'<h4>Tempo de Resposta: <span style="color: red;">{Tr:.0f} horas</span></h4>',
                        unsafe_allow_html=True)
            st.markdown(f'<h4>Distância Entre o Inventário e o Estuário: <span style="color: red;">{D:.0f} metros</span></h4>',
                        unsafe_allow_html=True)
        else:
            st.error('O tempo de resposta precisa ser menor que o tempo mínimo de toque de óleo no estuário')
else:
    st.warning("Preencha todos os campos corretamente para calcular o tempo de resposta e a distância.")

# Função para gerar PDF
def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.image(imagem_caminho, x=10, y=3, w=40)
    pdf.cell(200, 10, txt="Dimensionamento de Barreiras", ln=True, align='C')
    pdf.cell(200, 10, txt="Controle Ambiental", ln=True, align='C')
    pdf.cell(200, 10, txt="Centro de Tecnologias (CTEC)", ln=True, align='C')
    pdf.cell(200, 10, txt="Elaborado por: Adriel Lucas Ferreira de Oliveira", ln=True, align='C')

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Calado da Barreira: {calado_barreira:.2f} metros", ln=True)
    pdf.cell(200, 10, txt=f"Velocidade do vento: {velocidade_vento_nos:.2f} nós", ln=True)
    pdf.cell(200, 10, txt=f"Ângulo Correspondente: {angulo:.0f}°", ln=True)
    pdf.cell(200, 10, txt=f"Comprimento das Barreiras: {Bc:.0f} metros", ln=True)
    pdf.cell(200, 10, txt=f"Carga Suportada, Força da Correnteza: {Fc:.0f} kgf", ln=True)
    pdf.cell(200, 10, txt=f"Carga Suportada, Força da Vento: {Fv:.0f} kgf", ln=True)
    pdf.cell(200, 10, txt=f"Número de Âncoras: {Na:.0f} âncoras", ln=True)
    pdf.cell(200, 10, txt=f"Número de Estacas: {Na:.0f} estacas", ln=True)
    pdf.cell(200, 10, txt=f"Número de Boias de Arnique: {Na:.0f} boias", ln=True)
    pdf.cell(200, 10, txt=f"Comprimentos de Cabos: {Cc:.2f} metros", ln=True)
    pdf.cell(200, 10, txt=f"Tempo de Resposta: {Tr:.0f} horas", ln=True)
    pdf.cell(200, 10, txt=f"Distância Entre o Inventário e o Estuário: {D:.0f} metros", ln=True)

    return pdf.output(dest='S').encode('latin1')

# Botão de download do PDF
if st.session_state.lf > 0 and st.session_state.vcor > 0 and st.session_state.rb > 0 and st.session_state.vd > 0:
    pdf_data = gerar_pdf()
    st.download_button(label="Baixar PDF", data=pdf_data, file_name="dimensionamento_barreiras.pdf", mime='application/pdf')
else:
    st.warning("Preencha todos os campos necessários antes de gerar o PDF.")
