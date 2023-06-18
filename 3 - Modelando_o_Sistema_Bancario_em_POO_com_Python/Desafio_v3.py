import textwrap
from abc import ABC, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def realizar_transacao_transf(self, conta, conta_destino, transacao):
        transacao.registrar_transf(conta, conta_destino)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def cancelar_conta(self, conta):
        self.contas.remove(conta.numero)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @classmethod
    def cancela_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("\n@@@ Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print(f"\nValor de R$ {valor:.2f} sacado com sucesso. Novo saldo de: R$ {self._saldo:.2f}\n")
            return True

        else:
            print("\nFALHA! O valor informado é inválido")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\nValor de R$ {valor:.2f} depositado com sucesso. Novo saldo de: R$ {self._saldo:.2f}\n")

        else:
            print("\n@@@ FALHA! O valor informado é inválido. @@@")
            return False

        return True

    def transferir(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("\n@@@ FALHA! Você não tem saldo suficiente para realizar esta operação. @@@\n")

        elif(valor > 0):
            self._saldo -= valor
            print(f"\nValor de R$ {valor:.2f} transferido com sucesso. Novo saldo de: R$ {self._saldo:.2f}\n")
            return True

        else:
            print("\nFALHA! O valor informado é inválido")

        return False

    def transferir_conta_destino(self, valor):

        if(valor > 0):
            self._saldo += valor
            return True

        else:
            print("\nFALHA! O valor informado é inválido")

        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == "Saque"])

        if valor > self.limite:
            print("\n@@@ O valor do Saque excede o limite. @@@")

        elif numero_saques >= self.limite_saques:
            print("\n@@@ Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "operacao": transacao.operacao,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

    def adicionar_transacao_transf(self, transacao, conta, conta_transferencia):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "operacao": transacao.operacao,
                "valor": transacao.valor,
                "conta": conta.numero,
                "titular": conta.cliente.nome,
                "conta_destino": conta_transferencia.numero,
                "titular_conta_destino": conta_transferencia.cliente.nome,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._operacao = '-'

    @property
    def valor(self):
        return self._valor

    @property
    def operacao(self):
        return self._operacao

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._operacao = '+'

    @property
    def valor(self):
        return self._valor

    @property
    def operacao(self):
        return self._operacao

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Transferencia(Transacao):
    def __init__(self, valor):
        self._valor = valor
        self._operacao = None

    @property
    def valor(self):
        return self._valor

    @property
    def operacao(self):
        return self._operacao

    def registrar_transf(self, conta, conta_transferencia):
        sucesso_transacao = conta.transferir(self.valor)
        sucesso_transacao_transf = conta_transferencia.transferir_conta_destino(self.valor)

        if sucesso_transacao:
            self._operacao = "-"
            conta.historico.adicionar_transacao_transf(self, conta, conta_transferencia)

        if sucesso_transacao_transf:
            self._operacao = "+"
            conta_transferencia.historico.adicionar_transacao_transf(self, conta, conta_transferencia)

def verifica_cliente(cpf_cliente, clientes):
    clientes_verificados = [cliente for cliente in clientes if cliente.cpf == cpf_cliente]
    return clientes_verificados[0] if clientes_verificados else None

def verifica_conta(numero_conta, contas, cliente):
     conta_verificada = [conta for conta in contas if conta.numero == numero_conta and conta.cliente.cpf == cliente.cpf]
     return conta_verificada[0] if conta_verificada else None

def verifica_conta_outra_titularidade(numero_conta, contas):
     conta_verificada = [conta for conta in contas if conta.numero == numero_conta]
     return conta_verificada[0] if conta_verificada else None

def verifica_saldo(numero_conta, contas):
    verifica_saldo = [conta for conta in contas if conta.numero == numero_conta.numero and conta.saldo > 0]

    return True if verifica_saldo else None

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF: (somente números): ")

    if(validar_cpf(cpf) != True):
        print("\n@@@ FALHA! CPF inválido! @@@")
        return

    else:
        cliente = verifica_cliente(cpf, clientes)

        if cliente:
            print("\n@@@ Já existe um cliente cadastrado com este CPF! @@@")
            return

    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-yyyy): ")
    endereço = input("Informe o seu endereço (logradouro, nº - Bairro - Cidade/UF): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereço)

    clientes.append(cliente)

    print("\n*** Cliente criado com sucesso! ***")

def cadastrar_conta(numero_conta, cliente, contas):
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n*** Conta criada com sucesso! ***\n")

def cancelar_conta(numero_conta, cliente, contas):
    conta = ContaCorrente.cancela_conta(cliente=cliente, numero=numero_conta)
    contas.remove(conta.numero)
    cliente.contas.remove(conta.numero)

    print("\n*** Conta cancelada com sucesso! ***")

def exibir_extrato(numero_conta):
    print("\n*********************** EXTRATO ************************")
    transacoes = numero_conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            if 'Transferencia' in {transacao['tipo']} and '+' in {transacao['operacao']}:
                extrato += f"\n{transacao['tipo']}:\n\t{transacao['operacao']} R$ {transacao['valor']:.2f} de {transacao['titular']} C/C: {transacao['conta']} "
            elif 'Transferencia' in {transacao['tipo']} and '-' in {transacao['operacao']}:
                extrato += f"\n{transacao['tipo']}:\n\t{transacao['operacao']} R$ {transacao['valor']:.2f} para {transacao['titular_conta_destino']} C/C: {transacao['conta_destino']} "
            else:
                extrato += f"\n{transacao['tipo']}:\n\t{transacao['operacao']} R$ {transacao['valor']:.2f}"


    print(extrato)
    print(f"\nSaldo:\n\tR$ {numero_conta.saldo:.2f}")
    print("********************************************************")

def listar_contas(contas, cliente):
    if not contas:
        print("\n@@@ Cliente não possui contas abertas! @@@")
    else:
        print("\n")
        print(f"O Sr.(a) {cliente.nome.title()} possui as seguintes contas:\n")
        print("*" * 56)
        for conta in contas:
            if conta.cliente.cpf == cliente.cpf:
                linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero}
                """
                print(textwrap.dedent(linha))
        print("*" * 56)

def menu_principal(clientes,contas):
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

        if opcao.upper() == "L":
            if(len(clientes) != 0):
                cpf_cliente = input("Informe seu CPF cadastrado: (somente números): ")

                if(validar_cpf(cpf_cliente) != True):
                    print("\n@@@ FALHA! CPF inválido! @@@")

                else:
                    cliente = verifica_cliente(cpf_cliente, clientes)

                    if(cliente == None):
                        print("\n@@@ FALHA! CPF não cadastrado! @@@")

                    else:
                        print(f"\n*** Bem vindo, {cliente.nome.title()} ***")

                        menu_usuario(cliente, contas)
            else:
                print("\n@@@ FALHA! Não há nenhum usuário cadastrado para realizar Login! @@@")


        elif opcao.upper() == "C":
            cadastrar_cliente(clientes)

        elif opcao.upper() == "Q":
            print("\n*** Obrigado por ser cliente do nosso Banco. Volte Sempre! ***\n")
            exit()

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

def menu_usuario(cliente,contas):
    menu_cliente = '''

********************************************************
               BANCO DIO - MENU CLIENTE
********************************************************
    [C] CADASTRAR CONTA
    [A] ACESSAR CONTA
    [E] CANCELAR CONTA
    [L] LISTAR CONTAS
    [Q] SAIR DO MENU
********************************************************
'''

    while True:

        print(menu_cliente)
        opcao = input("Qual operação deseja realizar: ")

        if(opcao.upper() == "C"):
            numero_conta = len(contas) + 1
            cadastrar_conta(numero_conta, cliente, contas)

        elif(opcao.upper() == "A"):
            if not contas:
                print("\n@@@ Cliente não possui contas abertas! @@@")

            else:
                for conta in contas:
                    if cliente.cpf == conta.cliente.cpf:
                        print(f"    Agência: {conta.agencia} C/C: {conta.numero}")

                opcao_conta = int(input("\nDigite o número da conta que você deseja acessar: "))

                numero_conta = verifica_conta(opcao_conta, contas, cliente)

                if(numero_conta == None):
                    print(f"\n@@@ Sr.(a) {conta.cliente.nome.title()}, você não é titular desta conta informada. Acesso negado! @@@")
                else:
                    menu_conta(numero_conta, contas, cliente)

        elif(opcao.upper() == "E"):
            print("\n")

            if not contas:
                print("@@@ Usuário não possui contas abertas! @@@")

            else:
                for conta in contas:
                    if cliente.cpf == conta.cliente.cpf:
                        print(f"    Agência: {conta.agencia} C/C: {conta.numero}")

                opcao_conta = int(input("\nDigite o número da conta que você deseja cancelar: "))

                numero_conta = verifica_conta(opcao_conta, contas, cliente)

                if(numero_conta != None):
                    possui_saldo = verifica_saldo(numero_conta, contas)

                    if(possui_saldo == None):
                        cancelar_conta(numero_conta, cliente, contas)
                    else:
                        print("\n@@@ Conta com saldo. Não pode ser cancelada! @@@")

                else:
                    print("\n@@@ FALHA! A conta informada não existe ou não é de sua titularidade! @@@")

        elif(opcao.upper() == "L"):
            listar_contas(contas, cliente)

        elif(opcao.upper() == "Q"):
            print("\n*** Retornando ao Menu Principal... ***\n")
            break

        else:
            print("\n@@@ FALHA! O valor informado é inválido. Digite um valor válido. @@@\n")

def menu_conta(numero_conta, contas, cliente):
    menu_conta = f'''
********************************************************
               BANCO DIO - MENU CONTA {numero_conta.numero}
********************************************************
    [D] DEPOSITAR
    [S] SACAR
    [T] TRANSFERÊNCIA
    [E] EXTRATO
    [Q] SAIR DO MENU
********************************************************
'''
    while True:
        print(menu_conta)
        opcao = input("Qual operação deseja realizar: ")

        if(opcao.upper() == "D"):
            valor_deposito = float(input("\nPor favor, informe o valor do depósito: "))
            transacao = Deposito(valor_deposito)
            cliente.realizar_transacao(numero_conta, transacao)

        elif(opcao.upper() == "S"):
            valor_saque = float(input("\nPor favor, informe o valor do saque: "))
            transacao = Saque(valor_saque)
            cliente.realizar_transacao(numero_conta, transacao)

        elif(opcao.upper() == "T"):
            opcao_titularidade = str(input("\nDeseja transferir para conta de mesma titularidade? S ou N: "))
            if(opcao_titularidade.upper() == "S"):
                print("\n")
                contador = 0
                for conta in contas:
                    if numero_conta.cliente.cpf == conta.cliente.cpf and numero_conta.numero != conta.numero:
                        print(f"    Agência: {conta.agencia} C/C: {conta.numero}")
                        contador += 1

                if(contador < 1):
                    print("@@@ Titular não possui mais contas abertas! @@@")
                    break

                opcao_conta_transferencia = int(input("\nDigite o número da conta que receberá a transferência: "))
                numero_conta_transferencia = verifica_conta(opcao_conta_transferencia, contas, cliente)
                if(numero_conta_transferencia == None):
                    print("\n@@@ FALHA! Conta não existe ou não é de sua titularidade. @@@")
                else:
                    if(numero_conta.numero == opcao_conta_transferencia):
                        print("\n@@@ OPERAÇÃO INVÁLIDA. Conta informada é a mesma que está logada! @@@")
                    else:
                        valor_transferencia = float(input("\nPor favor, informe o valor da transferência: "))
                        transacao = Transferencia(valor_transferencia)
                        cliente.realizar_transacao_transf(numero_conta, numero_conta_transferencia, transacao)

            else:
                opcao_conta_transferencia = int(input("\nDigite o número da conta que receberá a transferência: "))
                numero_conta_transferencia = verifica_conta_outra_titularidade(opcao_conta_transferencia, contas)

                if(numero_conta_transferencia != None):
                    if(numero_conta_transferencia.cliente.cpf == numero_conta.cliente.cpf):
                        print("\n@@@ OPERAÇÃO INVÁLIDA. Conta informada é de mesma titularidade da conta logada! @@@")
                    else:
                        valor_transferencia = float(input("\nPor favor, informe o valor da transferência: "))
                        while True:
                            opcao_transferencia = input(f"\nSerá transferido o valor de R$ {valor_transferencia:.2f} para a conta nº {numero_conta_transferencia.numero} em nome do(a) Sr.(a) {numero_conta_transferencia.cliente.nome.title()}. Confirma S ou N? ")
                            if(opcao_transferencia.upper() == "S"):
                                transacao = Transferencia(valor_transferencia)
                                cliente.realizar_transacao_transf(numero_conta, numero_conta_transferencia, transacao)
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
    clientes = []
    contas = []

    menu_principal(clientes,contas)

main()