# program       ExemploLibSAT.py
# author        Daniel de Morais InfoCotidiano
# installation  Exemplo de uso da biblioteca ACBrLibSAT do Projeto ACBr utilizando Python 
#               SingleThread (ST) No-GUI
# date-written  20/07/2024

import ctypes
import json
import os
import sys

# Obtem a pasta do projeto
diretorio_script = os.path.dirname(os.path.abspath(__file__))

#DLL ACBrLibSAT utilizada neste projeto é 64 ST (Single Thread)
PATH_DLL                = os.path.abspath(os.path.join(diretorio_script,r"ACBrLib\x64\ACBrSat64.dll"))
PATH_ACBRLIB            = os.path.abspath(os.path.join(diretorio_script, "ACBrLib.INI"))
PATH_LOG                = os.path.abspath(os.path.join(diretorio_script, "Log"))
PATH_SCHEMA             = os.path.abspath(os.path.join(diretorio_script, "Schemas"))
ARQ_VENDA_INI           = os.path.abspath(os.path.join(diretorio_script, "CFe.ini"))
CFG_SAT_DLL             = os.path.abspath(os.path.join(diretorio_script,r"Sat\dllsat.dll"))
PATH_ARQVENDA           = os.path.abspath(os.path.join(diretorio_script, "Arquivos"))


#Constantes de Configuração Emitente, SoftHouse e sat


#Configuração Kit desenvolvedor SAT Bematech
CFG_CNPJSH              = '16716114000172'
CFG_NUMERO_CAIXA        = '1'
CFG_EMITENTE_CNPJ       = '27101611000182'
CFG_EMITENTE_IE         = '111111111111'
CFG_EMITENTE_REGTRIB    = '1'
CFG_SAT_ASSINATURA      ='SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT'
CFG_SAT_MODELO          = '1'
'''
CFG_CNPJSH              = '11111111111111'
CFG_NUMERO_CAIXA        = '1'
CFG_EMITENTE_CNPJ       = '11111111111111'
CFG_EMITENTE_IE         = '111111111111'
CFG_EMITENTE_REGTRIB    = '0'
CFG_SAT_ASSINATURA      ='9d4c4eef8c515e2c1269c2e4fff0719d526c5096422bf1defa20df50ba06469a28adb25ba0447befbced7c0f805a5cc58496b7b23497af9a04f69c77f17c0ce68161f8e4ca7e3a94c827b6c563ca6f47aea05fa90a8ce3e4327853bb2d664ba226728fff1e2c6275ecc9b20129e1c1d2671a837aa1d265b36809501b519dbc08129e1c1d2671a837aa1d265b36809501b519dbc08129e1c1d2671a837aa1d265b36809501b519dbc08129e1c'
CFG_SAT_MODELO          = '1'
'''

#Cria a pasta log se nao existir
if not os.path.exists(PATH_LOG):
   os.makedirs(PATH_LOG) 
#Cria a pasta Arquivos Vendas se nao existir
if not os.path.exists(PATH_ARQVENDA):
   os.makedirs(PATH_ARQVENDA) 

#DLL do sat é 64Bits

CFG_SAT_CODIGO_ATIVACAO = '00000000'

# Definindo a variável global
arquivo_sat = ""


#Tamanho da resposta q pode variar entao utilize a funcao define_bufferResposta() para as suas necessidades
tamanho_inicial = 9096
esTamanho = ctypes.c_ulong(tamanho_inicial)
sResposta = ctypes.create_string_buffer(tamanho_inicial)

#Verifica se a dll da Lib está no path indicado
if not os.path.exists(PATH_DLL):
   print(f"(Procurando DLL ACBrLib SAT) O arquivo '{PATH_DLL}' não existe.")
   sys.exit(1)
   
#Verifica se a dll do SAT está no path indicado
if not os.path.exists(CFG_SAT_DLL):
   print(f"(Procurando DLL do Fabricante SAT) O arquivo '{CFG_SAT_DLL}' não existe.")
   sys.exit(1)
   

# Carregar a DLL, ajustes os paths para seu ambiente.
acbr_lib = ctypes.CDLL(PATH_DLL)

#Inicializar a Biblioteca
retorno = acbr_lib.SAT_Inicializar(PATH_ACBRLIB.encode("utf-8"),"".encode("utf-8"))
if retorno != 0:
    print("Ocorreu um erro ao inicializar a biblioteca. Codigo:",retorno)
    sys.exit(1)
    
#configurando tipo de repsosta retorno 
acbr_lib.SAT_ConfigGravarValor("Principal".encode("utf-8"), "TipoResposta".encode("utf-8"), str(2).encode("utf-8"))
        
#configurando Dados Do Emitente e SoftwareHouse
acbr_lib.SAT_ConfigGravarValor("SAT".encode("utf-8"), "Modelo".encode("utf-8"), CFG_SAT_MODELO.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SAT".encode("utf-8"), "CodigoDeAtivacao".encode("utf-8"), CFG_SAT_CODIGO_ATIVACAO.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SAT".encode("utf-8"), "SignAC".encode("utf-8"), CFG_SAT_ASSINATURA.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SAT".encode("utf-8"), "NomeDLL".encode("utf-8"), CFG_SAT_DLL.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfig".encode("utf-8"), "ide_numeroCaixa".encode("utf-8"), CFG_NUMERO_CAIXA.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfig".encode("utf-8"), "emit_CNPJ".encode("utf-8"), CFG_EMITENTE_CNPJ.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfig".encode("utf-8"), "emit_IE".encode("utf-8"), CFG_EMITENTE_IE.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfig".encode("utf-8"), "emit_cRegTrib".encode("utf-8"), CFG_EMITENTE_REGTRIB.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfig".encode("utf-8"), "ide_CNPJ".encode("utf-8"), CFG_SAT_MODELO.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfig".encode("utf-8"), "ArqSchema".encode("utf-8"), PATH_SCHEMA.encode("utf-8"))
#configuracao Arquivos
acbr_lib.SAT_ConfigGravarValor("SATConfigArquivos".encode("utf-8"), "SalvarCFe".encode("utf-8"), str(1).encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfigArquivos".encode("utf-8"), "SalvarCFeCanc".encode("utf-8"), str(1).encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfigArquivos".encode("utf-8"), "SepararPorCNPJ".encode("utf-8"), str(1).encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfigArquivos".encode("utf-8"), "SepararPorModelo".encode("utf-8"), str(1).encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfigArquivos".encode("utf-8"), "SepararPorAno".encode("utf-8"), str(1).encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfigArquivos".encode("utf-8"), "PastaCFeVenda".encode("utf-8"), PATH_ARQVENDA.encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("SATConfigArquivos".encode("utf-8"), "SepararPorAno".encode("utf-8"), str(1).encode("utf-8"))
#log
acbr_lib.SAT_ConfigGravarValor("Principal".encode("utf-8"), "LogNivel".encode("utf-8"), str(4).encode("utf-8"))
acbr_lib.SAT_ConfigGravarValor("Principal".encode("utf-8"), "LogPath".encode("utf-8"), PATH_LOG.encode("utf-8"))

def define_bufferResposta(novo_tamanho):
    global tamanho_inicial, esTamanho, sResposta
    tamanho_inicial = novo_tamanho
    esTamanho = ctypes.c_ulong(tamanho_inicial)
    sResposta = ctypes.create_string_buffer(tamanho_inicial)
    return tamanho_inicial, esTamanho, sResposta 

def retorna_bufferResposta():    
    global tamanho_inicial, esTamanho, sResposta
    return tamanho_inicial, esTamanho, sResposta    

def atualizar_status_sat(novo_status):
    global arquivo_sat
    arquivo_sat = rf"{novo_status}".encode('utf-8')
    
def verificar_status_sat():
    global arquivo_sat
    return arquivo_sat    

def limpar_tela():
    if os.name == 'nt':  
        os.system('cls')
    else:
        os.system('clear')

#Inicializar SAT
retorno = acbr_lib.SAT_InicializarSAT();
if retorno != 0:
    print('Ocorreu um erro ao InicializarSAT, código:',retorno)
    sys.exit(1)

def exibir_menu():
    limpar_tela()
    print("Menu:")
    print("1. Consulta SAT")
    print("2. Criar e Enviar XML")
    print("3. Imprimir Cupom")
    print("4. Sair")
    
        
def opcao1():
    define_bufferResposta(9096)
    resultado = acbr_lib.SAT_ConsultarStatusOperacional(sResposta, ctypes.byref(esTamanho))
    resposta_completa = sResposta.value.decode("utf-8")
    if resultado == 0:
        print('-----------------------------------------------------------------------------------------')
        print(resposta_completa)
    else:
        print('Erro ao consultar SAT, Código:',resultado)

def opcao2():
    '''
    ATENÇÃO !
    O arquivo de venda esta em INI, para obter um ini válido, segue o link:
    https://acbr.sourceforge.io/ACBrLib/ModeloCFeINISimplificadovalido.html
    Você precisa alterar o cnpj da softwarehouse, assinatura, cnpj e ie do emitente.
    '''
    define_bufferResposta(30600)
    #Verifica se o INI da venda exemplo path indicado
    if not os.path.exists(ARQ_VENDA_INI):
        print(f"(Procurando Exemplo de INI Venda SAT) O arquivo '{ARQ_VENDA_INI}' não existe.")
        sys.exit(1)
    
    resultado = acbr_lib.SAT_CriarEnviarCFe(ARQ_VENDA_INI.encode('utf-8'), sResposta, ctypes.byref(esTamanho))
    if resultado != 0:
        print("Erro ao criarEnviarCEF, código:",resultado)
        sys.exit(1)
        
    json_string = sResposta.value.decode("utf-8")
    dados_json = json.loads(json_string)
    if dados_json['ENVIO']["CodigoDeRetorno"] == 6000:
        print("SAT Emitido com sucesso:",dados_json['ENVIO']["CodigoDeRetorno"] )
        print("Número Sessão:",dados_json['ENVIO']["NumeroSessao"] )
        print("Arquivo      :",dados_json['ENVIO']["Arquivo"] )
        print("XML      :",dados_json['ENVIO']["XML"] )
        if len(dados_json['ENVIO']["Arquivo"]) != 0: #verifica se foi retornado o Path Arquivo, para ser utilizado na impressao
            atualizar_status_sat(dados_json['ENVIO']["Arquivo"])
        else:
            atualizar_status_sat(dados_json['ENVIO']["XML"]) #se Arquivo nao foi devolvido, usar XML puro
    else:
        print("Erro ao Emitir SAT: ",dados_json['ENVIO']["CodigoDeRetorno"] )
        print("Número Sessão:",dados_json['ENVIO']["NumeroSessao"] )
        verificar_status_sat()
        
def opcao3():
    #print('Imprimir XML ',verificar_status_sat())
    #if os.path.exists(verificar_status_sat()):
        resposta = acbr_lib.SAT_ImprimirExtratoVenda(verificar_status_sat());
        if resposta == 0:
            print('Impresso com sucesso !')
        else:    
            print('Erro ao imprimir ',verificar_status_sat())
    #else:
    #    print("O arquivo não existe.",)

def aguardar_tecla():
    input("Pressione Enter para continuar...")
  
    
while True:
    exibir_menu()
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        opcao1()       
        aguardar_tecla()
    elif escolha == "2":
        opcao2()
        aguardar_tecla()
    elif escolha == "3":
        opcao3()
    elif escolha == "4":
        print("Saindo...")
        acbr_lib.SAT_Finalizar()

        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")    