from abc import ABC, abstractmethod
from datetime import datetime

# ----- Transações ----- #
class Historico:
    def __init__(self):
        self._transacoes = []

    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

# ----- Clientes ----- #
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = [] 

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    @classmethod
    def novo_cliente(cls, endereco, cpf, nome, data_nascimento):
       return cls(endereco, cpf, nome, data_nascimento)

# ----- Contas ----- #
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, numero, cliente):
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
        saldo_excedido = valor > saldo

        # Valor maior que o saldo 
        if saldo_excedido:
            print("\n[!] Saque falhou! Saldo insuficiente") 

        # Valor válido        
        elif valor > 0:
            self._saldo -= valor
            print(f"\n[+] Saque de R${valor} realizado com sucesso!")

            return True

        # Valor inválido
        else:
            print("\n[!] Saque falhou! Valor informado é inválido")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n[+] Depósito de R${valor} realizado com sucesso!")

            return True
        else:
            print("\n[!] Depósito falhou! Valor Inválido")

        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__( numero, cliente )
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        # Validação: Quantidade Limite de Saques
        num_saques = 1
        for transacao in self._historico._transacoes:
            if transacao["tipo"] == "Saque":
                num_saques += 1

        quantidade_excedida = num_saques > self._limite_saques

        # Validação: Valor Limite de Saque
        valor_excedido = valor > self._limite

        if quantidade_excedida:
            print("\n[!] Saque falhou! Número de saques diários atingido")

        elif valor_excedido:
            print("\n[!] Saque falhou! Valor limite atingido")

        else: 
            # Valição específica CC + Validação geral
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return  ( "\n" + f" CONTA {self._numero} ".center(30,"=") +
        f"\n\tAgência: {self._agencia}" +
        f"\n\tCPF: {self._cliente.cpf}" + 
        f"\n\tTitular: {self._cliente.nome}\n" + 
        f"{"=" * 30}")


# ----- Funções ----- #
def menu():
    menu = """ 
-- || Opções de operações || -- 

[0] Depositar
[1] Sacar
[2] Extrato
[3] Criar Usuário
[4] Criar Conta

[5] Listar Usuários
[6] Listar Contas
[7] Sair

Escolha: """

    opcao = input(menu)

    return opcao

def buscar_cliente (clientes, cpf):
    cliente = [cliente for cliente in clientes if cliente.cpf == cpf]
    if len(cliente) == 0: 
        print("\n[!] Não foi encontrado cliente com este CPF!")
        cliente = None
    else:
        cliente = cliente[0]

    return cliente

def obter_cliente_por_cpf(clientes):
    cpf = input("Informe o CPF do usuário: ")
    cliente = buscar_cliente (clientes, cpf)

    if cliente is None:
        return None

    return cliente

def deposito(clientes):
    cliente = obter_cliente_por_cpf(clientes)

    if cliente is None:
        return

    # Validar se o cliente tem conta
    if not cliente.contas:
        print("\n[-] Cliente não possui contas!")
        return 
    else:
        valor = float(input("Informe o valor do depósito: R$" ))
        transacao = Deposito(valor)

        conta = cliente.contas[0]
        cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cliente = obter_cliente_por_cpf(clientes)

    if cliente is None:
        return

    # Validar se o cliente tem conta
    if not cliente.contas:
        print("[-] Cliente não possui contas!")
        return 
    else:
        valor = float(input("Informe o valor do saque: R$" ))
        transacao = Saque(valor)

        conta = cliente.contas[0]
        cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes, saldo, extrato):
    cliente = obter_cliente_por_cpf(clientes)

    if cliente is None:
        return
    
    # Validar se o cliente tem conta
    if not cliente.contas:
        print("[-] Cliente não possui contas!")
        return 
    else:
        conta = cliente.contas[0]

    transacoes = conta.historico.transacoes()

    for transacao in transacoes:
        if transacao["tipo"] == "Saque":
            extrato += f"- [-] {transacao["tipo"]}: R${transacao["valor"]:.2f} [{transacao["data"]}]\n"
        else:
            extrato += f"- [+] {transacao["tipo"]}: R${transacao["valor"]:.2f} [{transacao["data"]}]\n"

    print("\n" + " EXTRATO ".center(30,"="))
    print("Não foram realiadas movimentações." if not extrato else extrato)
    print(f"\nSaldo Atual: R${conta.saldo:.2f}")
    print("=".center(30,"="))

def criarCliente(clientes):
    print("\n--- Cadastro de Novo Cliente ---")
    cpf = input("Informe o CPF do usuário: ")

    # Validar usuário
    for cliente_existente in clientes:
        if cpf == cliente_existente.cpf:
            print("\n[!] Usuário com esse CPF já existente!")
            return
    
    nome = input("Nome Completo: ")
    data_nascimento = input("Data de Nascimento(DD/MM/YYYY): ")
    endereco = input("Endereço(Logadouro, Nº - Bairro - Cidade/Sigla Estado): ")

    # Adiciona 
    cliente = PessoaFisica.novo_cliente(endereco, cpf, nome, data_nascimento)
    clientes.append(cliente)

    print("\n[+] Usuário Adicionado com Sucesso!")
    
def criarConta(contas, clientes, numero_conta):
    cliente = obter_cliente_por_cpf(clientes)

    if cliente is None:
        return

    conta = ContaCorrente.nova_conta(numero_conta, cliente)

    # Adiciona na lista de contas geral e do cliente 
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n[+] Conta Criada com Sucesso!")

def listarContas(contas):
    print("\n" + f" CONTAS ".center(50,"="))

    if len(contas) == 0:
        print("\tSem contas disponíveis")
    else:
        for conta in contas:
            print(conta)

    print("\n" + "=" * 50)

def listarUsuarios(clientes):
    print("\n" + f" USUÁRIOS ".center(50,"="))

    if len(clientes) == 0:
        print("\tSem usuários disponíveis")
    else:
        for cliente in clientes:
            print(f"CPF: {cliente.cpf}")
            print(f"Nome: {cliente.nome}")
            print(f"Data Nascimento: {cliente.data_nascimento}")
            print(f"Endereco: {cliente.endereco}")
            print("=" * 30)

    print("\n" + "=" * 50)

def main():
    clientes = []
    contas = []

    saldo = 0 
    extrato = ""
    num_conta = 1 

    while True:
        opcao = menu()

        # Depósito
        if opcao == "0":
            deposito(clientes)

        # Sacar
        elif opcao == "1":
            sacar(clientes)

        # Extrato
        elif opcao == "2":
            # Vinculo entre as listas, necessidade de return 
            exibir_extrato(clientes ,saldo, extrato)

        # Usuário
        elif opcao == "3":
            criarCliente(clientes)

        # Conta
        elif opcao == "4":
            criarConta(contas, clientes, num_conta)
            num_conta += 1

        #Listar Usuário
        elif opcao == "5":
            listarUsuarios(clientes)

        #Listar Usuário
        elif opcao == "6":
            listarContas(contas)
        
        # Sair
        elif opcao == "7":
            print("\n" + "APLICAÇÃO ENCERRADA".center(30,"-") + "\n")
            break

        else:
            print("[!] Operação inválida! Selecione novamente a operação desejada")

main()