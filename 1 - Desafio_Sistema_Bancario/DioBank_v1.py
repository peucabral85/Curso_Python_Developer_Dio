saldo = 0
LIMITE_VALOR_SAQUE = 500
LIMITE_SAQUES_DIARIO = 3
numero_saques_dia = 0
extrato = ""
menu = '''
************************* BANCO DIO ********************

************************* MENU *************************

    [D] DEPOSITAR
    [S] SACAR
    [E] EXTRATO
    [Q] SAIR

********************************************************
'''

while True:
    print(menu)
    opcao = input("Qual operação deseja realizar: ")

    if(opcao.upper() == "D"):
        while True:
            valor_deposito = float(input("\nPor favor, informe o valor do depósito: "))

            if(valor_deposito > 0):
                saldo += valor_deposito
                extrato += f"Depósito: R$ {valor_deposito:.2f}\n"
                print(f"\nValor de R$ {valor_deposito:.2f} depositado com sucesso. Novo saldo de: R$ {saldo:.2f}\n")

                opcao_deposito = input("Deseja realizar outro depósito? S ou N? ")
                if(opcao_deposito.upper() == "S"):
                    continue
                else:
                    print("\nRetornando ao Menu Principal...")
                    break
                
            else:
                print("\nFALHA! O valor informado é inválido. Digite um valor válido.\n")   

    elif(opcao.upper() == "S"):
        while True:
            valor_saque = float(input("\nPor favor, informe o valor do saque: "))

            if(valor_saque > saldo):
                print("\nFALHA! Você não tem saldo suficiente para realizar esta operação.\n")
                print("Retornando ao Menu Principal...")
                break

            elif(numero_saques_dia >= LIMITE_SAQUES_DIARIO):
                print("\nFALHA! Você excedeu a quantidade de saques diários permitidos.\n")
                print("Retornando ao Menu Principal...")
                break

            elif(valor_saque > LIMITE_VALOR_SAQUE):
                print(f"\nFALHA! O valor informado de saque excede o limite permitido de R$ {LIMITE_VALOR_SAQUE:.2f}. Digite novamente.") 

            elif(valor_saque > 0):
                saldo -= valor_saque
                extrato += f"Saque: R$ {valor_saque:.2f}\n"
                numero_saques_dia += 1
                print(f"\nValor de R$ {valor_saque:.2f} sacado com sucesso. Novo saldo de: R$ {saldo:.2f}\n")

                opcao_saque = input("Deseja realizar outro saque? S ou N? ")
                if(opcao_saque.upper() == "S"):
                    continue
                else:
                    print("\nRetornando ao Menu Principal...")
                    break

            else:
                print("\nFALHA! O valor informado é inválido. Digite um valor válido.\n")  

    elif(opcao.upper() == "E"):
        print("\n*********************** EXTRATO ************************")
        print("Não houve movimentação no período." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("********************************************************")

        opcao_extrato = input("\nDeseja realizar outra operação? S ou N? ")
        if(opcao_extrato.upper() == "S"):
            print("\nRetornando ao Menu Principal...")
        else:
            print("\nObrigado por ser cliente do nosso Banco. Volte Sempre!\n")
            break

    elif(opcao.upper() == "Q"):
        print("\nObrigado por ser cliente do nosso Banco. Volte Sempre!\n")
        break

    else:    
        print("\nOpção inválida. Selecione novamente uma operação válida.\n")