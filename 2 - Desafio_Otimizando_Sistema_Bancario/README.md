## **Projeto 2 - Otimizando Projeto de Sistema Bancário** 🏦

Otimizar o código do sistema bancário, separando as funções existentes de saque, depósito e extrato em funções, além de criar as funções cadastrar usuário (cliente) e cadastrar conta bancária.

## **Instruções de Entrega do Desafio:**

- Modularizar o código criando funções para as operações: sacar, depositar e visualizar histórico.
- Para esta versão, criar duas novas funções: criar usuário (cliente do banco) e criar conta corrente (vincular com o usuário).
- Deve-se criar funções para todas as operações do sistema, sendo que cada função terá uma regra na passagem de argumentos.
- A função saque deve receber argumentos apenas por nome (keyword only).
- A função depósito deve receber os argumentos apenas por posição (positional only).
- A função extrato deve receber os argumentos por posição e nome (positional only e keyword only).
- A função Criar Usuário deve armazenar os usuários em uma lista. Um usuário é composto por nome, data de nascimento, cpf e endereço. O endereço é uma string com o formato: logradouro, nro - bairro - cidade/sigla estado. Deve ser armazenado somente os números do CPF. Não pode ser aceito dois usuários com o mesmo CPF.
- A função Criar Conta deve armazenar contas em uma lista, onde uma conta é composta por: agência, número da conta e usuário. O número da conta é sequencial, iniciando em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence a somente um usuário.

⚠Nesta versão, já utilizamos o conhecimento de funções, estruturas de dados e outros conhecimentos básicos de Python. O código possui transição de Menus conforme indicação do usuário. Foram criados os Menus: Principal (onde o usuário possui as opção de cadastro ou de login), Usuário (onde há opções de criar conta, acessar conta, cancelar conta, listar contas e voltar ao menu principal) e Conta (onde há opções de depósito, saque, transferência entre contas de mesma titularidade ou não, e voltar ao menu de Usuário). Como citado acima, adicionei a função de Transferência entre contas e também de Cancelamento de Conta, onde uma conta só poderá ser cancelada se não tiver saldo.

Link para o código:

[Sistema Bancário v2](https://github.com/peucabral85/Curso_Python_Developer_Dio/blob/master/2%20-%20Desafio_Otimizando_Sistema_Bancario/DioBank_v2.py)