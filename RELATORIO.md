# 📑 Relatório de Evolução do Projeto — Sistema Correios

## 📌 Contexto
Projeto desenvolvido em **Python 3 + Flask + SQLAlchemy** para controle interno de documentos e pacotes.  
Funcionalidades principais: cadastro de itens, movimentações (entradas/saídas), relatórios filtrados e dashboard.

---

## 🛠️ Alterações Realizadas

### Funcionalidades
- **Filtros em movimentações por usuário, tipo e período** ✔️  
- **Campo "Usuário" na tabela de movimentações** ✔️  
- Busca avançada por protocolo, remetente, destinatário ou descrição ⏳  
- Histórico detalhado de cada item ⏳  

### Interface
- **Padronização completa dos botões (verde, vermelho, azul, cinza)** ✔️  
- **Botão "Registrar Saída" padronizado (fundo escuro, letras verdes)** ✔️  
- Responsividade total para celular/tablet ⏳  
- Ícones visuais (📥 entrada, 📤 saída, ✅ finalizado) ⏳  
- Feedback visual (animação/destaque ao registrar ação) ⏳  

### Segurança
- Autenticação por níveis (admin, usuário comum) ⏳  
- Logs de auditoria (quem fez cada ação) ⏳  
- Backup automático do banco ⏳  

### Documentação
- **README atualizado com instruções claras e seção "Como acessar"** ✔️  
- **CHANGELOG.md inicial criado** ✔️  
- Guia rápido de uso (fluxo: cadastrar → saída → relatório) ⏳  
- RELATORIO.md consolidando evolução ⏳  

---

## 📊 Tabela Resumida

| Área           | Melhoria                                                                 | Status | Observações                                                                 |
|----------------|--------------------------------------------------------------------------|--------|------------------------------------------------------------------------------|
| Funcionalidade | **Filtros em movimentações por usuário, tipo e período**                 | ✔️     | Corrigido no backend e template; só exibe dados após FILTRAR                 |
| Funcionalidade | **Campo "Usuário" na tabela de movimentações**                           | ✔️     | Exibição com ícones 👑 admin / 👤 usuário                                    |
| Funcionalidade | **Campo "Tipo" na tabela de movimentações**                              | ✔️     | Exibição com ícones 📥 Entrada / 📤 Saída                                    |
| Funcionalidade | **Campo "Status" na tabela de movimentações**                            | ✔️     | Exibição com ✔ verde para Finalizado                                         |
| Funcionalidade | **Remoção da coluna "Ações" da página de movimentações**                 | ✔️     | Agora só existe em Itens cadastrados                                         |
| Funcionalidade | Busca avançada por protocolo, remetente, destinatário ou descrição       | ⏳     | Planejado com query dinâmica no SQLAlchemy                                   |
| Funcionalidade | Histórico detalhado de cada item                                         | ⏳     | Planejado: criar tabela de log de movimentações                              |
| Interface      | **Padronização completa dos botões (verde, vermelho, azul, cinza)**      | ✔️     | Implementado em `style.css`                                                  |
| Interface      | **Botão "Registrar Saída" padronizado (fundo escuro, letras verdes)**    | ✔️     | Ajustado em `index.html`                                                     |
| Interface      | **Ícones visuais aplicados (👑, 👤, 📥, 📤, ✔)**                          | ✔️     | Implementados diretamente no template `movimentacoes.html`                   |
| Interface      | Responsividade total para celular/tablet                                 | ⏳     | Ajustar CSS com media queries                                                |
| Interface      | Feedback visual (animação/destaque ao registrar ação)                    | ⏳     | Usar CSS transitions ou JS                                                   |
| Segurança      | Autenticação por níveis (admin, usuário comum)                           | ✔️     | Implementado com `role` no modelo `User` e decorador `@admin_required`       |
| Segurança      | Logs de auditoria (quem fez cada ação)                                   | ✔️     | Campo `user` incluído em `Movement`                                          |
| Segurança      | Backup automático do banco                                               | ⏳     | Planejado com script cron ou integração externa                              |
| Documentação   | **README atualizado com instruções claras e seção "Como acessar"**       | ✔️     | Inclui links para init e dashboard                                           |
| Documentação   | **CHANGELOG.md inicial criado**                                          | ✔️     | Versão 1.1.0 documentando filtros, CSS e ícones visuais                      |
| Documentação   | Guia rápido de uso (fluxo: cadastrar → saída → relatório)                | ⏳     | Adicionar no README                                                          |
| Documentação   | RELATORIO.md consolidando evolução                                       | ✔️     | Atualizado com todas as melhorias                                            |

---

## 👨‍💻 Autor
Projeto desenvolvido por **Junior Alexandre da Silva**  
GitHub: [@JuniorSilva88](https://github.com/JuniorSilva88)
