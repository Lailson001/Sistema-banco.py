# Função para exibir o menu de opções
def menu():
    return """\n
    ======== MENU ======== 
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    [q] Sair
    """


# Função para realizar um depósito
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print('Depósito realizado com sucesso!')
    else:
        print('Operação falhou! O valor informado é inválido.')

    return saldo, extrato


# Função para realizar um saque
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('Operação falhou! Você não tem saldo suficiente.')
    elif excedeu_limite:
        print('Operação falhou! O valor do saque excede o limite.')
    elif excedeu_saques:
        print('Operação falhou! Número máximo de saques excedido.')
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1  
        print('Saque realizado com sucesso!')
    else:
        print('Operação falhou! O valor informado é inválido.')

    return saldo, extrato, numero_saques


# Função para exibir o extrato bancário
def exibir_extrato(saldo, /, *, extrato):
    print("\n=== Extrato ===")
    print("Saldo: R$", saldo)
    print("\n=== Movimentações ===")
    print(extrato if extrato else "Nenhuma movimentação registrada.")


# Função para buscar um usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    """Verifica se um usuário já está cadastrado pelo CPF."""
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Digite o CPF do usuário (apenas números): ").strip()

    if not cpf.isdigit() or len(cpf) != 11:
        print("Erro: CPF inválido! Digite apenas números e com 11 dígitos.")
        return

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuário já cadastrado.")
        return

    nome = input("Digite o nome do usuário: ").strip()
    data_nascimento = input("Digite a data de nascimento do usuário (DD/MM/AAAA): ").strip()
    endereco = input("Digite o endereço do usuário (Logradouro, Número, Bairro - Cidade/UF): ").strip()

    novo_usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }

    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")


# Função para criar uma nova conta bancária
def criar_conta(agencia, numero_conta, saldo, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "saldo": saldo, "titular": usuario["nome"]}

    print("Usuário não cadastrado, processo de criação de conta encerrado!")
    return None


# Função para listar todas as contas cadastradas
def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    print("\n===== LISTA DE CONTAS =====")
    for conta in contas:
        linha = f"""\
Agência: {conta['agencia']}
Número da conta: {conta['numero_conta']}
Titular: {conta['titular']}
Saldo: R$ {conta.get('saldo', 0.00):.2f}
---------------------------"""
        print(linha)


# Função principal para executar o programa
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        print(menu())
        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, saldo, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por utilizar nosso sistema bancário. Até mais!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


# Executar o programa
main()


                
          
        

