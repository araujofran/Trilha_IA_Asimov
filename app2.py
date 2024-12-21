from langchain_community.document_loaders import YoutubeLoader
from deep_translator import GoogleTranslator
from fpdf import FPDF

# Função para dividir o texto em partes menores
def dividir_texto(texto, limite=500):
    palavras = texto.split()
    partes = []
    parte_atual = []
    comprimento_atual = 0

    for palavra in palavras:
        if comprimento_atual + len(palavra) + 1 > limite:
            partes.append(' '.join(parte_atual))
            parte_atual = []
            comprimento_atual = 0
        parte_atual.append(palavra)
        comprimento_atual += len(palavra) + 1

    if parte_atual:
        partes.append(' '.join(parte_atual))

    return partes

# Função para traduzir o texto
def traduzir_texto(texto, destino='pt'):
    tradutor = GoogleTranslator(source='auto', target=destino)
    partes = dividir_texto(texto)
    traducao_completa = []

    for parte in partes:
        traducao = tradutor.translate(parte)
        traducao_completa.append(traducao)

    return ' '.join(traducao_completa)

# Função para criar o PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Transcrição Traduzida', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()

def criar_pdf(texto, nome_arquivo):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Transcrição Traduzida')
    pdf.chapter_body(texto)
    pdf.output(nome_arquivo, 'F')

# Função para criar o arquivo de texto
def criar_txt(texto, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(texto)

# Usando a URL fornecida
video_loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=dtaomFaE8xk",
                                              language=["en"])
document = video_loader.load()

# Traduzir o conteúdo do vídeo
conteudo_original = document[0].page_content
conteudo_traduzido = traduzir_texto(conteudo_original)

# Criar o PDF com o texto traduzido
nome_arquivo_pdf = "transcricao_traduzida.pdf"
criar_pdf(conteudo_traduzido, nome_arquivo_pdf)

# Criar o arquivo de texto com o texto traduzido
nome_arquivo_txt = "transcricao_traduzida.txt"
criar_txt(conteudo_traduzido, nome_arquivo_txt)

print("Conteúdo Original:")
print(conteudo_original)
print("\nConteúdo Traduzido:")
print(conteudo_traduzido)
print(f"\nPDF criado: {nome_arquivo_pdf}")
print(f"Arquivo de texto criado: {nome_arquivo_txt}")






