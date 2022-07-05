from time import time
import face_recognition
import json 
import random
import simpy

ARQUIVO_CONFIGURACAO = 'configuracao.json'

LISTA_FOTOS = [
    "BD/faces/Caco Ciocler.jpg",
    "BD/faces/Debora Bloch.jpg",
    "BD/faces/Emilio Zurita.jpg",
    "BD/faces/Luciano Huck.jpg",
    "BD/faces/Luciano Szafir.jpg",
    "BD/faces/Marcos Mion.jpg",
    "BD/faces/Mateus Solano.jpg"
]


def configuracao_inicial():
    global configuracao
    global foto_selecionada_aleatoriamente 
    global pessoa_reconhecida 
    global pessoa_dados 
    global lista_pessoas_condominio
    
    with open(ARQUIVO_CONFIGURACAO, "r") as arquivo_configuracao: configuracao = json.load(arquivo_configuracao)
    pessoa_reconhecida = False
    pessoa_dados = {}
    lista_pessoas_condominio = []
    
# Será um gerador de evento.
def selecionar_pessoa(env):
    global foto_selecionada_aleatoriamente
    while True:
        foto_selecionada_aleatoriamente = random.choice(LISTA_FOTOS)
        
        print(f"foto selecionada: {foto_selecionada_aleatoriamente}")
        yield env.timeout(1)

# Será um gerador de evento.
def configurar_reconhecedor_face(env):
    global foto_selecionada_aleatoriamente
    global foto_original_criptografada
    
    while True:
        print(f"configurando foto selecionada: {foto_selecionada_aleatoriamente}")
    
        foto_selecionada = face_recognition.load_image_file(foto_selecionada_aleatoriamente)
        foto_original_criptografada = face_recognition.face_encodings(foto_selecionada)[0]
        
        yield env.timeout(1)
    

def reconhecer_face(foto):
    global foto_original_criptografada
    
    e_igual = None
    
    try:
        foto_selecionada = face_recognition.load_image_file(foto)
        foto_selecionada_criptografada = face_recognition.face_encodings(foto_selecionada)[0]
        
        e_igual = face_recognition.compare_faces([foto_original_criptografada], foto_selecionada_criptografada)
        print(e_igual)
    except:
        pass
    
    return e_igual

def verifica_na_lista():
    global pessoa_reconhecida
    
    for foto in LISTA_FOTOS:
        if reconhecer_face(foto):
            pessoa_reconhecida = True
       
def realizar_verificacao_entrada():
    global foto_selecionada_aleatoriamente 
    global pessoa_reconhecida 
    global pessoa_dados 
    global lista_pessoas_condominio
    
    if pessoa_reconhecida:
        for pessoa in configuracao["pessoas"]:
            if pessoa["foto"] == foto_selecionada_aleatoriamente:
                pessoa_dados = pessoa
        
        print(f"\nDados da pessoa reconhecida: {pessoa_dados}!\n")
        
        if pessoa_dados["residente"] == True:
            print(f"Bem vindo de volta, {pessoa_dados['nome']}\n")
            lista_pessoas_condominio = pessoa_dados
        else:
            print("Você não é um residente do condomínio, verificando autorização de entrada!\n")

            if pessoa_dados["entrada_autorizada"] == True:
                print(f"Visitante {pessoa_dados['nome']} possui autorização, por favor entre!\n")
                lista_pessoas_condominio = pessoa_dados
            else:
                print(f"Visitante {pessoa_dados['nome']} não possui autorização de entrada!\n")
    else: 
        print("Nenhum resultado semelhante encontrado")
        
if __name__ == "__main__":
    env = simpy.Environment()
    
    configuracao_inicial()

    # selecionar_pessoa()
    env.process(selecionar_pessoa(env))
    env.process(configurar_reconhecedor_face(env))
    env.run(until=10)
    
    # configurar_reconhecedor_face()
    
    # verifica_na_lista()
    
    # realizar_verificacao_entrada()
    

                