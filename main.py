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

TIMEOUT_INTERVALO = 1

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
        
        print(f'Numero da simulação: {env.now}\n')
        print(f"foto selecionada: {foto_selecionada_aleatoriamente}")
        yield env.timeout(TIMEOUT_INTERVALO)

# Será um gerador de evento.
def configurar_reconhecedor_face(env):
    global foto_selecionada_aleatoriamente
    global foto_original_criptografada
    
    while True:
        print(f"configurando foto selecionada: {foto_selecionada_aleatoriamente}")
    
        foto_selecionada = face_recognition.load_image_file(foto_selecionada_aleatoriamente)
        foto_original_criptografada = face_recognition.face_encodings(foto_selecionada)[0]
        
        yield env.timeout(TIMEOUT_INTERVALO)
    

def reconhecer_face(foto):
    global foto_original_criptografada

    e_igual = None    
    try:
        foto_selecionada = face_recognition.load_image_file(foto)
        foto_selecionada_criptografada = face_recognition.face_encodings(foto_selecionada)[0]
        
        e_igual = face_recognition.compare_faces([foto_original_criptografada], foto_selecionada_criptografada)
    except:
        pass
    
    return e_igual

# Será um gerador de evento.
def verifica_na_lista(env):
    global pessoa_reconhecida
    
    while True:
        for foto in LISTA_FOTOS:
            if reconhecer_face(foto):
                pessoa_reconhecida = True
                yield env.timeout(TIMEOUT_INTERVALO)
            else: 
                print('Pessoa não reconhecida com base no banco de dados atual')

# Será um gerador de evento.
def realizar_verificacao_entrada(env):
    global foto_selecionada_aleatoriamente 
    global pessoa_reconhecida 
    global pessoa_dados 
    global lista_pessoas_condominio
    
    while True:
        if pessoa_reconhecida:
            for pessoa in configuracao["pessoas"]:
                if pessoa["foto"] == foto_selecionada_aleatoriamente:
                    pessoa_dados = pessoa
            
            print(f"\nDados da pessoa reconhecida: {pessoa_dados['nome']}!\n")
            
            if pessoa_dados["residente"] == True:
                print(f"Bem vindo de volta, residente {pessoa_dados['nome']}\n")
                lista_pessoas_condominio.append(pessoa_dados)
            else:
                print("Você não é um residente do condomínio, verificando autorização de entrada!\n")

                if pessoa_dados["entrada_autorizada"] == True:
                    print(f"Visitante {pessoa_dados['nome']} possui autorização, por favor entre!\n")
                    lista_pessoas_condominio.append(pessoa_dados)
                else:
                    print(f"Visitante {pessoa_dados['nome']} não possui autorização de entrada!\n")
        else: 
            print("Nenhum resultado semelhante encontrado")

        yield env.timeout(TIMEOUT_INTERVALO)
        
def sair_condominio():
    pass

if __name__ == "__main__":
    env = simpy.Environment()
    
    configuracao_inicial()

    env.process(selecionar_pessoa(env))
    env.process(configurar_reconhecedor_face(env))
    env.process(verifica_na_lista(env))
    env.process(realizar_verificacao_entrada(env))
    env.run(until=20)

    print(f'Pessoas dentro do condomínio: {lista_pessoas_condominio}')

                