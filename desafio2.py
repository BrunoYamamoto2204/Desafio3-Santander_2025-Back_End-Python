
def menu():
    menu = """ 
-- || Opções de operações || -- 

[0] Depositar
[1] Sacar
[2] Extrato
[3] Criar Usuário
[4] Criar Conta

[5] Listar Contas
[6] Listar Usuários
[7] Sair

Escolha: """

    opcao = input(menu)

    return opcao

def deposito(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f" - [+] Depósito:  R${valor:.2f} \n"
    else:
        print("[!] Depósito falhou! Valor Inválido")

    return saldo, extrato

def sacar(*, valor, numero_saques, limite, extrato, saldo):

    # Limites de saque
    if numero_saques >= LIMITE_SAQUES:
        print("[!] Saque falhou! Número de saques diários atingido")

    # Valor inválido
    elif valor <= 0:
        print("[!] Saque falhou! Valor informado é inválido")

    # Valor saldo
    elif valor <= saldo:
        if valor <= limite:
            saldo -= valor
            numero_saques += 1
            extrato += f" - [-] Saque: R${valor:.2f}\n" 
        else:
            print("[!] Saque falhou! Valor limite atingido")
    
    # Valor passa do limite 
    else: 
        print("[!] Saque falhou! Saldo insuficiente")

    return saldo, numero_saques, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n" + " EXTRATO ".center(30,"="))
    print("Não foram realiadas movimentações." if not extrato else extrato)
    print(f"\nSaldo Atual: R${saldo:.2f}")
    print("=".center(30,"="))

def criarUsuario(usuarios):
    cpf = input("Informe seu CPF: ")

    # Validar usuário
    for usuario in usuarios:
        if cpf in usuario["cpf"]:
            print("\n[!] Usuário com esse CPF já existente!")
            return
    
    nome = input("Nome Completo: ")
    data_nascimento = input("Data de Nascimento(DD/MM/YYYY): ")
    endereco = input("Endereço(Logadouro, Nº - Bairro - Cidade/Sigla Estado): ")

    usuarios.append({ "cpf":cpf, "nome":nome,"data_nascimento":data_nascimento,"endereco":endereco })
    print("\n[+] Usuário Adicionado com Sucesso!")
    
def criarConta(usuarios, numero_conta):
    cpf = input("Informe seu CPF: ")

    # Procurar pelo usuário
    encontrou = False
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("\n[+] Conta Criada com Sucesso!")
            contas.append({"agencia": "0001","numero_conta": numero_conta, "conta": usuario})
            numero_conta += 1

            encontrou = True

    if not encontrou:
        print("\n[!] Não foi encontrado usuário com este CPF!")

    return contas, numero_conta

def listarContas(contas):
    print("\n" + f" CONTAS ".center(50,"="))

    if len(contas) == 0:
        print("\tSem contas disponíveis")
    else:
        for conta in contas:
            print("\n" + f" CONTA {conta["numero_conta"]} ".center(30,"="))
            print(f"\tAgência: {conta["agencia"]}")
            print(f"\tCPF: {conta["conta"]["cpf"]}")
            print(f"\tTitular: {conta["conta"]["nome"]}")
            print("=" * 30)

    print("\n" + "=" * 50)

def listarUsuarios(usuarios):
    print("\n" + f" USUÁRIOS ".center(50,"="))

    if len(usuarios) == 0:
        print("\tSem usuários disponíveis")
    else:
        for usuario in usuarios:
            print(f"CPF: {usuario["cpf"]}")
            print(f"Nome: {usuario["nome"]}")
            print(f"Data Nascimento: {usuario["data_nascimento"]}")
            print(f"Endereco: {usuario["endereco"]}")
            print("=" * 30)

    print("\n" + "=" * 50)

saldo = 0 
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []
num_conta = 1 

while True:
    opcao = menu()

    # Depósito
    if opcao == "0":
        valor = float(input("Informe o valor do depósito: R$"))
        saldo, extrato = deposito(valor, saldo, extrato)

    # Sacar
    elif opcao == "1":
        valor = float(input("Informe o valor do saque: R$"))
        saldo, numero_saques, extrato= sacar(
            valor = valor,
            numero_saques = numero_saques, 
            limite = LIMITE_SAQUES,
            extrato = extrato,
            saldo = saldo
        )

    # Extrato
    elif opcao == "2":
        # Vinculo entre as listas, necessidade de return 
        exibir_extrato(saldo, extrato=extrato)

    # Usuário
    elif opcao == "3":
        criarUsuario(usuarios)

    # Conta
    elif opcao == "4":
        contas, num_conta = criarConta(usuarios, num_conta)

    #Listar Usuário
    elif opcao == "5":
        listarContas(contas)

    #Listar Usuário
    elif opcao == "6":
        listarUsuarios(usuarios)

    # Sair
    elif opcao == "7":
        print("\n" + "APLICAÇÃO ENCERRADA".center(30,"-") + "\n")
        break

    else:
        print("[!] Operação inválida! Selecione novamente a operação desejada")