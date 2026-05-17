# LPOO - 2026-1 - Locadora de Veículos

Este é o projeto base utilizado na disciplina de **Linguagem de Programação Orientada a Objetos (LPOO)** do curso de Ciência da Computação, semestre **2026-1**, ministrada pela **Professora Vanessa**.

O objetivo deste projeto é servir como base prática para a aplicação de conceitos de Orientação a Objetos e Padrões de Projeto estudados em sala de aula.

## Funcionalidades Desenvolvidas

O projeto possui cadastro de veículos e funcionalidades de locação de veículos usando Python, Tkinter, MVC, DAO e PostgreSQL.

Foram implementadas telas para:

- Cadastro, edição, remoção e consulta de veículos.
- Cadastro administrativo de locações.
- Tela operacional para reservar, locar, devolver, cancelar e visualizar detalhes de locações.
- Busca de veículos disponíveis por categoria e período.

## Detalhamento de Aprendizado (Dificuldade e Soluções)

- Durante o desenvolvimento, uma das principais dificuldades foi trazer dados de veículos para dentro da funcionalidade de locação. Foi necessário buscar as placas dos veículos cadastrados no banco e exibi-las no campo de seleção da tela `Cadastro -> Locações -> Novo`, mantendo o fluxo correto entre View, Controller e DAO.

- Implementação da tela `Ação -> Locar Veículo -> Nova Reserva`. Nessa parte, foi necessário criar a lógica de `buscar_veiculos_disponiveis`, considerando categoria, data de início, data de fim e as locações já registradas no banco.

- Também foi necessário implementar a verificação de conflito de locações. Um veículo não pode aparecer como disponível quando já possui uma locação ativa no mesmo período. Para isso, foram considerados como ativos os status `reservado` e `locado`.

- No Tkinter, organizar a `JanelaPrincipal` e o método `criar_menu`. A aplicação precisa ter apenas uma instância de `tk.Tk`, enquanto as demais janelas devem ser `tk.Toplevel`. Além disso, nas telas que abrem cadastro ou edição, foi usado `wait_window` para aguardar o fechamento da janela filha e depois chamar `carregar_dados`, atualizando a tabela.

- Houve dificuldade na implementação dos fluxos de abrir edição e remoção. Esse ajuste foi feito tanto em Veículos quanto em Locações.

- As dificuldades foram resolvidas com revisão das aulas, testes no sistema, análise das mensagens exibidas no terminal e apoio guiado por ferramentas de IA.

***O principal aprendizado foi compreender melhor a separação do projeto em MVC e DAO. Essa organização reduz a mistura de responsabilidades, facilita a manutenção e deixa o código mais compreensível.***

## Declaração de Uso de IA

_(Prática comum de transparência acadêmica e profissional no GitHub)_

- [ ] **Nenhuma IA foi utilizada** na elaboração deste código.
- [x] **Utilizei IA** como ferramenta de apoio.
- **Ferramenta(s):** ChatGPT e Claude Opus 4.6.
- **Finalidade:** apoio na organização do código, revisão de lógica, implementação guiada das telas e  auxílio na identificação de erros durante os testes.
- **Validação:** Declaro que todo o código gerado foi lido, testado e compreendido.
