from mongodb_handler import MongoDBHandler

comentarios = [
    (1, 'Excelente smartphone! Muito rápido e câmera incrível.'),
    (1, 'Ótimo produto, mas achei o preço um pouco alto.'),
    (3, 'TV com qualidade de imagem fantástica. Super recomendo!'),
    (6, 'Café delicioso, aroma incrível. Compro sempre!'),
    (13, 'Tênis confortável, mas esperava mais pela marca.'),
    (11, 'Camisa de excelente qualidade. Tecido muito bom.'),
    (19, 'Bicicleta boa, mas veio com alguns ajustes a fazer.'),
    (22, 'Hidratante maravilhoso! Deixa a pele super macia.'),
    (31, 'Livro envolvente, não consegui parar de ler!'),
    (37, 'Minha filha adorou! Brinquedo de qualidade.'),
    (2, 'Notebook rápido, mas esquenta um pouco durante uso intenso.'),
    (4, 'Fone com som excelente, bateria dura bastante.'),
    (16, 'Panelas antiaderentes de verdade. Muito satisfeita!'),
    (26, 'Livro bom, mas esperava mais do autor.'),
    (35, 'Quebra-cabeça desafiador e divertido para toda família.')
]

def replace_comments():
    mongo_handler = MongoDBHandler()
    # Limpar a coleção de comentários existente
    mongo_handler.db['comments'].delete_many({})
    # Inserir os novos comentários
    for prod_id, comentario in comentarios:
        mongo_handler.insert_comment(prod_id, comentario)
    mongo_handler.close()

if __name__ == "__main__":
    replace_comments()
