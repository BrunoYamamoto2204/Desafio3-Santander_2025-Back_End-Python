# 💰 Desafio 3 - Sistema Bancário com POO em Python

Este é o terceiro desafio do **Bootcamp Santander 2025 - Back-End com Python**, e tem como objetivo aplicar os conceitos de **Programação Orientada a Objetos (POO)** em um sistema bancário. Nesta versão, o sistema foi modularizado em classes, usando herança, polimorfismo, abstração e composição.

---

## ⚙️ Funcionalidades Implementadas

### 📌 Funcionalidades Gerais

- **Depósito**: Adiciona saldo na conta do cliente, validando valores positivos.
- **Saque**: Permite sacar valores respeitando o limite diário de saques e o limite máximo por saque.
- **Extrato**: Lista todas as movimentações (depósitos e saques) realizadas com data e hora.
- **Criação de Usuário**: Permite cadastrar clientes com CPF, nome, data de nascimento e endereço, impedindo duplicações.
- **Criação de Conta**: Cria uma conta corrente para um cliente existente, permitindo múltiplas contas por cliente.
- **Listagem de Usuários e Contas**: Exibe informações dos clientes e suas contas bancárias.

---

## 🔄 Atualizações do Desafio 3

O código foi **refatorado completamente com Programação Orientada a Objetos**, organizando as responsabilidades em diversas classes:

### 🧱 Novas Estruturas Criadas

| Classe         | Descrição |
|----------------|-----------|
| `Cliente`      | Classe base para qualquer cliente. Armazena endereço e lista de contas. |
| `PessoaFisica` | Herda de `Cliente`, adiciona CPF, nome e data de nascimento. |
| `Conta`        | Classe base de contas. Gerencia saldo, saque, depósito e histórico. |
| `ContaCorrente`| Herda de `Conta`, com regras específicas de limite de saque e número máximo de saques. |
| `Historico`    | Armazena todas as transações feitas por uma conta. |
| `Transacao`    | Classe abstrata que define a interface para `Deposito` e `Saque`. |
| `Deposito`     | Representa uma transação de depósito. |
| `Saque`        | Representa uma transação de saque. |

### 🧠 Conceitos de POO Utilizados

- **Herança**: Ex: `PessoaFisica` herda de `Cliente`, `ContaCorrente` herda de `Conta`.
- **Polimorfismo**: O método `registrar()` é sobrescrito nas transações.
- **Abstração**: A classe `Transacao` é abstrata e exige que `registrar()` seja implementado nas subclasses.
- **Composição**: `Conta` possui (`tem um`) `Historico`.

---

## 🚀 Como Executar

1. Certifique-se de ter o **Python** instalado.
2. Salve o código Python em um arquivo, por exemplo `sistema_bancario.py`.
3. Execute no terminal com:

```bash
python sistema_bancario.py
```

4. Use o menu interativo para operar o sistema.
---
### 🛠 Tecnologias Utilizadas
- Python: A linguagem de programação principal utilizada para desenvolver o sistema.
