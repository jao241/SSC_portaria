# SSC_portaria
Um projeto baseado em um mini mundo para um sistema sensivel a contexto que funciona com base no reconhecimento de face (no caso do repositório, foram utilizadas imagens).
<br>
Utiliza-se da linguagem <i>Python</i> e algumas bibliotecas, cujos nomes encontram-se no arquivo requirements.txt.

Matéria: Interface Homem Máquina
Aluno: João Vitor Lima Lago Santos (2019119013)

Ideia: SSC para uma portaria de condomínio.

Descrição: Trata-se de um sistema que ficará disposto na portaria de um condomínio e será responsável por verificar as pessoas que entram e saem do mesmo. Terá a capacidade de reconhecer rostos e verificar-los numa base de dados, caso seja reconhecido como residente o acesso ao condomínio será consedido, caso contrário, será buscada uma autorização que deverá estar previamente disponível na base de dados, o que validará se poderá passar pela portaria ou não. Por fim verificará a saida das pessoas, para questão de segurança e controle sobre as pessoas presentes no condomínio.

Obs: A base de dados conterá imagens de residentes aleatórias e também as imagens dos não residentes, representando uma grande banco de informações fictícias.

As seguintes operações serão simuladas:

  1) Reconhecimento de pessoa na portaria pela face;
  2) Verificar se é um residente do condomínio;
  3) Verificar autorização de entrada no condomínio (No caso de um não residente, ex: Pessoas convidadas pelos residentes, funcionários que não moram no local, entregadores...);
  4) Liberação de pessoas do condomínio;