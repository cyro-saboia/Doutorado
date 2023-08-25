import os

pasta_origem = "../yolov7x/data/val"  # Insira o caminho para a pasta onde estão os arquivos PNG
pasta_destino = "../yolov7x/data/val"  # Insira o caminho para a pasta de destino

for nome_arquivo in os.listdir(pasta_origem):
    if nome_arquivo.endswith(".png"):
        caminho_origem = os.path.join(pasta_origem, nome_arquivo)
        nome_arquivo_sem_extensao = os.path.splitext(nome_arquivo)[0]
        novo_nome_arquivo = nome_arquivo_sem_extensao + ".jpg"
        caminho_destino = os.path.join(pasta_destino, novo_nome_arquivo)
        os.rename(caminho_origem, caminho_destino)