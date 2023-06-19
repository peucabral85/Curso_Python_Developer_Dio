## **Projeto 3 - Modelando o Projeto de Sistema Bancário em POO** 🏦

Iniciar a modelagem do sistema bancário em POO. Adicionar classes para cliente e as operações bancárias: depósito e saque.

## **Instruções de Entrega do Desafio:**

- Atualizar a implementação do sistema bancário armazenando os dados de clientes e contas bancárias em objetos ao invés de dicionários. O código deve seguir o modelo de classes UML a seguir:

  ![](https://github.com/peucabral85/Curso_Python_Developer_Dio/assets/94022011/49e38a4c-dcb4-48b9-9169-080d6b8a65b1)

⚠Nesta versão, utilizamos o conhecimento de estruturação em classes e armazenando os dados em objetos, ao contrário da versão anterior que foram utilizados dicionários. Realizei algumas mudanças no modelo proposto para poder adaptar a classe Transferência, já que além da conta, necessitamos também da informação da conta de destino. Sendo assim, na Interface Transação, realizei a alteração no método registrar, que passou a receber conta e conta_destino. Mesmo que para as operações de depósito e saque a conta destino seja a mesma conta da operação, para poder manter a estrutura da Interface e poder trabalhar com a classe Transferência na Interface Transação, optei por realizar esta alteração. Também criei o método cancelar_conta na classe Cliente e cancela_conta na classe Conta, para trabalharmos com o Cancelamento de Contas.

Link para o Código:

[Sistema Bancário v3](https://github.com/peucabral85/Curso_Python_Developer_Dio/blob/master/3%20-%20Modelando_o_Sistema_Bancario_em_POO_com_Python/Desafio_v3.py)
