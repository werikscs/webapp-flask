from flask import Flask, render_template, request
from PIL import Image
import io
from classificador import classificar
import base64

app = Flask(__name__)
application = app

# Lista global para armazenar o histórico das imagens classificadas
historico_imagens = []

@app.route('/', methods=['GET', 'POST'])
def index():
    classification_result = None
    image_data = None
    
    if request.method == 'POST':
        if 'classify' in request.form:
            if 'image' not in request.files:
                return "Nenhuma imagem foi enviada"
            image_file = request.files['image']
            if image_file.filename == '':
                return "Nenhuma imagem foi selecionada"

            # Lê a imagem diretamente da requisição
            image = Image.open(image_file.stream)
            
            # Converte a imagem em bytes para passar para o classificador
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format)
            img_byte_arr = img_byte_arr.getvalue()

            # Classifica a imagem
            classificacao = classificar(img_byte_arr)
            raça = classificacao['raça']
            confiança = classificacao['confiança']

            # Formata o resultado para a imagem principal
            classification_result = f"Raça Prevista: {raça} com {confiança * 100:.2f}% de confiança"

            # Codifica a imagem em base64 para renderizar na página sem salvar em disco
            image_data = base64.b64encode(img_byte_arr).decode('utf-8')

            # Adiciona a imagem ao histórico
            historico_imagens.append({
                'image_data': image_data,
                'raça': raça,
                'confiança': f"{confiança * 100:.2f}%"  # Formata para exibir só nas miniaturas
            })

    # Passa o histórico de imagens para o template
    return render_template('index.html', classification_result=classification_result, image_data=image_data, historico_imagens=historico_imagens)

if __name__ == '__main__':
    app.run()
