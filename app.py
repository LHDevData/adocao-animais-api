from flask import Flask, request, jsonify
from models import db, Animal

# Inicializa a aplicação Flask
app = Flask(__name__)

# --- Bloco de configuração do banco de dados ---
@app.before_request
def before_request():
    # Conecta ao banco de dados antes de cada requisição
    db.connect()

@app.after_request
def after_request(response):
    # Fecha a conexão com o banco de dados após cada requisição
    db.close()
    return response
# --- Fim do bloco de configuração ---


# Rota principal (página inicial) - apenas para teste
@app.route('/')
def index():
    return "API de Adoção de Animais está no ar!"

# --- Rotas da API para Animais (CRUD) ---

# Rota para LISTAR todos os animais (GET) e CRIAR um novo animal (POST)
@app.route('/animais', methods=['GET', 'POST'])
def gerenciar_animais():
    # Se o método for POST, criamos um novo animal
    if request.method == 'POST':
        dados = request.get_json()
        # Validação simples dos dados recebidos
        if not dados or 'nome' not in dados or 'especie' not in dados or 'idade' not in dados:
            return jsonify({'erro': 'Dados incompletos'}), 400

        novo_animal = Animal.create(
            nome=dados['nome'],
            especie=dados['especie'],
            idade=dados['idade'],
            disponivel=dados.get('disponivel', True) # Usa o valor enviado ou True como padrão
        )
        return jsonify(novo_animal.to_dict()), 201 # 201 = Created

    # Se o método for GET, listamos todos os animais
    elif request.method == 'GET':
        animais = Animal.select()
        lista_animais = [animal.to_dict() for animal in animais]
        return jsonify(lista_animais)

# Rota para buscar (GET), atualizar (PUT) e deletar (DELETE) um animal específico pelo ID
@app.route('/animais/<int:animal_id>', methods=['GET', 'PUT', 'DELETE'])
def gerenciar_animal_por_id(animal_id):
    try:
        # Tenta encontrar o animal pelo ID fornecido
        animal = Animal.get_by_id(animal_id)
    except Animal.DoesNotExist:
        # Se não encontrar, retorna um erro 404 (Not Found)
        return jsonify({'erro': 'Animal não encontrado'}), 404

    # Se o método for GET, retorna os dados do animal
    if request.method == 'GET':
        return jsonify(animal.to_dict())

    # Se o método for PUT, atualiza os dados do animal
    elif request.method == 'PUT':
        dados = request.get_json()
        animal.nome = dados.get('nome', animal.nome)
        animal.especie = dados.get('especie', animal.especie)
        animal.idade = dados.get('idade', animal.idade)
        animal.disponivel = dados.get('disponivel', animal.disponivel)
        animal.save()
        return jsonify(animal.to_dict())

    # Se o método for DELETE, remove o animal do banco
    elif request.method == 'DELETE':
        animal.delete_instance()
        return jsonify({'mensagem': 'Animal deletado com sucesso'}), 200 # 200 = OK


# --- Bloco para inicializar o banco de dados ---
if __name__ == '__main__':
    # Este bloco só será executado quando rodarmos o 'app.py' diretamente
    print("Inicializando o banco de dados e criando a tabela, se não existir...")
    db.connect()
    # Cria a tabela 'Animal' no banco de dados, mas só se ela não existir ainda
    db.create_tables([Animal], safe=True)
    db.close()
    print("Tabela 'Animal' pronta.")
    # Inicia a aplicação Flask para rodar localmente
    app.run(debug=True, port=5001)