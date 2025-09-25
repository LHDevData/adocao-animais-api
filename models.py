import os
from peewee import *
from playhouse.db_url import connect

# Conecta ao banco de dados usando uma variável de ambiente.
# Se a variável não existir, cria um banco local chamado 'animais.db'.
# Isso nos ajuda a usar um banco de dados diferente no deploy (Railway) e no desenvolvimento local.
db = connect(os.environ.get('DATABASE_URL', 'sqlite:///animais.db'))

# Classe base do modelo que especifica o banco de dados a ser usado.
class BaseModel(Model):
    class Meta:
        database = db

# Modelo para a tabela de Animais.
# Cada atributo representa uma coluna na tabela.
class Animal(BaseModel):
    nome = CharField()
    especie = CharField()
    idade = IntegerField()
    disponivel = BooleanField(default=True) # Por padrão, um animal cadastrado está disponível

    def to_dict(self):
        # Função útil para converter os dados do animal para um formato JSON.
        return {
            'id': self.id,
            'nome': self.nome,
            'especie': self.especie,
            'idade': self.idade,
            'disponivel': self.disponivel
        }