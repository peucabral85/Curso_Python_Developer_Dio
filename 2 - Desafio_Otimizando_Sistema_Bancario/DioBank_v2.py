import re
import textwrap
from sys import exit

def menu_principal(usuarios, contas):
    menu = '''
********************************************************
               BANCO DIO - MENU PRINCIPAL
********************************************************
    [L] LOGAR
    [C] CADASTRAR USUÁRIO
    [Q] SAIR
********************************************************
'''
    while True:
        print(menu)
        opcao = input("Qual operação deseja realizar: ")

        if(opcao.upper() == "L"):
            if(len(usuarios) != 0):
                cpf_usuario = input("Informe seu CPF cadastrado: (somente números): ")

                if(validar_cpf(cpf_usuario) != True):
                    print("\n@@@ FALHA! CPF inválido! @@@")

                else:    

                    usuario = verifica_usuario(cpf_usuario, usuarios)

                    if(usuario == None):
                        print("\n@@@ FALHA! CPF não cadastrado! @@@")

                    else:    
                        usuario_logado = usuario["nome"]
                        print(f"\n*** Bem vindo, {usuario_logado.title()} ***")

                        menu_usuario(usuario, contas)
            else:
                print("\n@@@ FALHA! Não há nenhum usuário cadastrado para realizar Login! @@@")

        elif(opcao.upper() == "C"):
            cadastrar_usuario(usuarios)

        elif(opcao.upper() == "Q"):
            print("\n*** Obrigado por ser cliente do nosso Banco. Volte Sempre! ***\n")
            exit()

        else:
            print("\n@@@ FALHA! O valor informado é inválido. Digite um valor válido. @@@\n")

def menu_usuario(usuario,contas):
    menu_usuario = '''

********************************************************
               BANCO DIO - MENU USUÁRIO
********************************************************
    [C] CADASTRAR CONTA
    [A] ACESSAR CONTA
    [E] CANCELAR CONTA
    [L] LISTAR CONTAS
    [Q] SAIR DO MENU
********************************************************
'''

    while True:

        AGENCIA = "0001"
        saldo = 0
        extrato =""
        numero_saques_dia = 0

        print(menu_usuario)
        opcao = input("Qual operação deseja realizar: ")

        if(opcao.upper() == "C"):
            numero_conta = len(contas) + 1
            conta = cadastrar_conta(AGENCIA, numero_conta, saldo, numero_saques_dia, extrato, usuario)
            contas.append(conta)
            print("\n*** Conta criada com sucesso! ***\n")

        elif(opcao.upper() == "A"):
            print("\n")

            if not contas:
                print("@@@ Usuário não possui contas abertas! @@@")

            else:    
                for conta in contas:
                    if usuario['cpf'] == conta['usuario']['cpf']:
                        print(f"    Agência: {conta['agencia']} C/C: {conta['numero_conta']}")

                opcao_conta = int(input("\nDigite o número da conta que você deseja acessar: "))

                numero_conta = verifica_conta(opcao_conta, contas, usuario)
                if(numero_conta == None):
                    print(f"\n@@@ Sr.(a) {conta['usuario']['nome'].title()}, você não é titular desta conta informada. Acesso negado! @@@")
                else:
                    menu_conta(numero_conta, contas, usuario)

        elif(opcao.upper() == "E"):
            print("\n")

            if not contas:
                print("@@@ Usuário não possui contas abertas! @@@")

            else:
                for conta in contas:
                    if usuario['cpf'] == conta['usuario']['cpf']:
                        print(f"    Agência: {conta['agencia']} C/C: {conta['numero_conta']}")

                opcao_conta = int(input("\nDigite o número da conta que você deseja cancelar: "))

                numero_conta = verifica_conta(opcao_conta, contas, usuario)

                if(numero_conta != None):
                    possui_saldo = verifica_saldo(opcao_conta, contas)

                    if(possui_saldo == None):
                        cancelar_conta(opcao_conta, contas)
                    else:
                        print("\n@@@ Conta com saldo. Não pode ser cancelada! @@@")  

                else:
                    print("\n@@@ FALHA! A conta informada não existe ou não é de sua titularidade! @@@")


        elif(opcao.upper() == "L"):
            listar_contas(contas, usuario)

        elif(opcao.upper() == "Q"):
            print("\n*** Retornando ao Menu Principal... ***\n")
            break

        else:
            print("\n@@@ FALHA! O valor informado é inválido. Digite um valor válido. @@@\n")


def menu_conta(numero_conta, contas, usuario):
    menu_conta = f'''
********************************************************
               BANCO DIO - MENU CONTA {numero_conta['numero_conta']}
********************************************************
    [D] DEPOSITAR
    [S] SACAR
    [T] TRANSFERÊNCIA
    [E] EXTRATO
    [Q] SAIR DO MENU
********************************************************
'''
    while True:

        LIMITE_VALOR_SAQUE = 500
        LIMITE_SAQUES_DIARIO = 3

        print(menu_conta)
        opcao = input("Qual operação deseja realizar: ")

        if(opcao.upper() == "D"):
            valor_deposito = float(input("\nPor favor, informe o valor do depósito: "))
            depositar(valor_deposito, numero_conta)

        elif(opcao.upper() == "S"):
            valor_saque = float(input("\nPor favor, informe o valor do saque: "))
            sacar(valor_saque = valor_saque, limite_valor_saque = LIMITE_VALOR_SAQUE,
                  limite_saques_diario = LIMITE_SAQUES_DIARIO, numero_conta = numero_conta)
            
        elif(opcao.upper() == "T"):
            opcao_titularidade = str(input("\nDeseja transferir para conta de mesma titularidade? S ou N: "))
            if(opcao_titularidade.upper() == "S"):
                print("\n")
                contador = 0
                for conta in contas:
                    if numero_conta['usuario']['cpf'] == conta['usuario']['cpf'] and numero_conta['numero_conta'] != conta['numero_conta']:
                        print(f"    Agência: {conta['agencia']} C/C: {conta['numero_conta']}") 
                        contador += 1

                if(contador < 1):
                    print("@@@ Titular não possui mais contas abertas! @@@")
                    continue         

                opcao_conta_transferencia = int(input("\nDigite o número da conta que receberá a transferência: "))
                numero_conta_transferencia = verifica_conta(opcao_conta_transferencia, contas, usuario)
                if(numero_conta_transferencia == None):
                    print("\n@@@ FALHA! Conta não existe ou não é de sua titularidade. @@@")
                else:
                  #  numero_conta_transferencia = verifica_conta_transferencia(opcao_conta_transferencia, contas, usuario)
                    if(numero_conta['numero_conta'] == opcao_conta_transferencia):
                        print("\n@@@ OPERAÇÃO INVÁLIDA. Conta informada é a mesma que está logada! @@@")  
                    else:      
                        valor_transferencia = float(input("\nPor favor, informe o valor da transferência: "))       

                        transferir(valor_transferencia, numero_conta, numero_conta_transferencia)

            else:
                opcao_conta_transferencia = int(input("\nDigite o nº da conta para transferência: "))
                numero_conta_tranferencia = verifica_conta_outra_titularidade(opcao_conta_transferencia, contas)

                if(numero_conta_tranferencia != None):
                    #numero_conta_transferencia = verifica_conta_outra_titularidade_transferencia(opcao_conta_transferencia, contas, usuario)
                    if(numero_conta_tranferencia['usuario']['cpf'] == numero_conta['usuario']['cpf']):
                        print("\n@@@ OPERAÇÃO INVÁLIDA. Conta informada é de mesma titularidade da conta logada! @@@")
                    else:    
                        valor_transferencia = float(input("\nPor favor, informe o valor da transferência: "))
                        while True:
                            opcao_transferencia = input(f"\nSerá transferido o valor de R$ {valor_transferencia:.2f} para a conta nº {numero_conta_tranferencia['numero_conta']} em nome do(a) Sr.(a) {numero_conta_tranferencia['usuario']['nome'].title()}. Confirma S ou N? ")
                            if(opcao_transferencia.upper() == "S"):
                                transferir(valor_transferencia, numero_conta, numero_conta_tranferencia)
                                break
                            elif(opcao_transferencia.upper() == "N"):
                                print("\n*** Operação de transferência cancelada! ****")
                                break
                            else:
                                print("\n@@@ Opção incorreta! Digite novamente. @@@")    

                else:
                    print("\n@@@ O número de conta informado não existe! @@@")    

        elif(opcao.upper() == "E"):
            exibir_extrato(numero_conta)

        elif(opcao.upper() == "Q"):
            print("\n*** Retornando ao Menu de Usuário... ***\n")
            break

        else:
            print("\n@@@ FALHA! O valor informado é inválido. Digite um valor válido. @@@\n")
      

def cadastrar_usuario(usuarios):
    cpf = input("Informe o seu CPF: (somente números): ")

    if(validar_cpf(cpf) != True):
        print("\n@@@ FALHA! CPF inválido! @@@")
        return

    else:    
        usuario = verifica_usuario(cpf, usuarios)

        if usuario:
            print("\n@@@ Já existe um usuário cadastrado com este CPF! @@@")
            return

    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-yyyy): ")
    endereço = input("Informe o seu endereço (logradouro, nº - Bairro - Cidade/UF): ")

    usuarios.append({"nome" : nome, "data_nascimento" : data_nascimento, "cpf": cpf, "endereço" : endereço})

    print("\n*** Usuário criado com sucesso! ***")

def verifica_usuario(cpf, usuarios):
    verifica_cpf = [usuario for usuario in usuarios if usuario["cpf"] == cpf]

    return verifica_cpf[0] if verifica_cpf else None

def verifica_conta(numero_conta, contas, usuario):
    verifica_conta = [conta for conta in contas if conta["numero_conta"] == numero_conta and conta["usuario"]["cpf"] == usuario["cpf"]]

    return verifica_conta[0] if verifica_conta else None

def verifica_conta_outra_titularidade(numero_conta, contas):
    verifica_conta = [conta for conta in contas if conta["numero_conta"] == numero_conta]

    return verifica_conta[0] if verifica_conta else None

def verifica_saldo(opcao_conta, contas):
    verifica_saldo = [conta for conta in contas if conta["numero_conta"] == opcao_conta and conta["saldo"] > 0]

    return True if verifica_saldo else None

def cadastrar_conta(agencia, numero_conta, saldo, numero_saques_dia, extrato, usuario):
    return {'agencia': agencia, 'numero_conta': numero_conta, 'saldo': saldo,
            'numero_saques_dia': numero_saques_dia, 'extrato': extrato, 'usuario': usuario}

def cancelar_conta(opcao_conta, contas):
 
    for indice, conta in enumerate(contas):
        if conta.get('numero_conta') == opcao_conta:
            break

    contas.pop(indice)
    print("\n*** Conta cancelada com sucesso! ***")

def listar_contas(contas, usuario):
    if not contas:
        print("\n@@@ Usuário não possui contas abertas! @@@")  
    else:
        print("\n")
        print(f"O Sr.(a) {usuario['nome'].title()} possui as seguintes contas:\n")
        print("*" * 56)
        for conta in contas:
            if conta['usuario']['cpf'] == usuario['cpf']:
                linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                """
                print(textwrap.dedent(linha))
        print("*" * 56)                              

def depositar(valor_deposito, numero_conta, /):
    if(valor_deposito > 0):
        numero_conta['saldo'] += valor_deposito
        numero_conta['extrato'] += f"Depósito: + R$ {valor_deposito:.2f}\n"
        print(f"\nValor de R$ {valor_deposito:.2f} depositado com sucesso. Novo saldo de: R$ {numero_conta['saldo']:.2f}\n")
    else:
        print("\n@@@ FALHA! O valor informado é inválido. Digite um valor válido. @@@\n")


def sacar(*, valor_saque, limite_valor_saque, limite_saques_diario, numero_conta):

    if(valor_saque > numero_conta['saldo']):
        print("\n@@@ FALHA! Você não tem saldo suficiente para realizar esta operação. @@@\n")

    elif(numero_conta['numero_saques_dia'] >= limite_saques_diario):
        print("\n@@@ FALHA! Você excedeu a quantidade de saques diários permitidos. @@@\n")

    elif(valor_saque > limite_valor_saque):
        print(f"\n@@@ FALHA! O valor informado de saque excede o limite permitido de R$ {limite_valor_saque:.2f}. Digite novamente. @@@")

    elif(valor_saque > 0):
        numero_conta['saldo'] -= valor_saque
        numero_conta['extrato'] += f"Saque: - R$ {valor_saque:.2f}\n"
        numero_conta['numero_saques_dia'] += 1
        print(f"\nValor de R$ {valor_saque:.2f} sacado com sucesso. Novo saldo de: R$ {numero_conta['saldo']:.2f}\n")

    else:
        print("\n@@@ FALHA! O valor informado é inválido. Digite um valor válido. @@@\n")

def transferir(valor_transferencia, numero_conta, numero_conta_transferencia):
    if(valor_transferencia > numero_conta['saldo']):
        print("\n@@@ FALHA! Você não tem saldo suficiente para realizar esta operação. @@@\n")

    elif(valor_transferencia > 0):
        numero_conta['saldo'] -= valor_transferencia
        numero_conta_transferencia['saldo'] += valor_transferencia
        numero_conta['extrato'] += f"""Tranferência: - R$ {valor_transferencia:.2f} para {numero_conta_transferencia['usuario']['nome'].title()}
                Agência: {numero_conta_transferencia['agencia']} CC: {numero_conta_transferencia['numero_conta']}\n"""
        numero_conta_transferencia['extrato'] += f"""Tranferência: + R$ {valor_transferencia:.2f} de {numero_conta['usuario']['nome'].title()}
                Agência: {numero_conta['agencia']} CC: {numero_conta['numero_conta']}\n"""
        print(f"\nValor de R$ {valor_transferencia:.2f} transferido com sucesso. Novo saldo de: R$ {numero_conta['saldo']:.2f}\n") 

    else:
        print("\n@@@ FALHA! O valor informado é inválido. Digite um valor válido. @@@\n")               


def exibir_extrato(numero_conta):
    print("\n*********************** EXTRATO ************************")
    print("Não houve movimentação no período." if not numero_conta['extrato'] else numero_conta['extrato'])
    print(f"\nSaldo: R$ {numero_conta['saldo']:.2f}")
    print("********************************************************")

def validar_cpf(cpf: str) -> bool:

    # Obtém apenas os números do CPF, ignorando pontuações
    numeros = [int(digito) for digito in cpf if digito.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numeros) != 11 or len(set(numeros)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    soma_dos_produtos = sum(a*b for a, b in zip(numeros[0:9], range(10, 1, -1)))
    digito_esperado = (soma_dos_produtos * 10 % 11) % 10
    if numeros[9] != digito_esperado:
        return False

    # Validação do segundo dígito verificador:
    soma_dos_produtos = sum(a*b for a, b in zip(numeros[0:10], range(11, 1, -1)))
    digito_esperado = (soma_dos_produtos * 10 % 11) % 10
    if numeros[10] != digito_esperado:
        return False

    return True    

def main():

    usuarios = []
    contas = []

    menu_principal(usuarios,contas)

main()
