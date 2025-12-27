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

# 📊 Relatório de Evolução — Sistema Correios

## Tabela Resumida

| Área            | Melhoria                                                   | Status | Observações                                                                 |
|-----------------|------------------------------------------------------------|--------|------------------------------------------------------------------------------|
| Funcionalidade  | Filtros em movimentações por usuário, tipo e período        | ✔️     | Implementados no formulário de filtros (usuario, tipo, data início/fim)      |
| Funcionalidade  | Campo "Usuário" na tabela de movimentações                  | ✔️     | Exibição com ícones 👑 admin / 👤 usuário                                    |
| Funcionalidade  | Campo "Tipo" na tabela de movimentações                     | ✔️     | Exibição com ícones 📥 Entrada / 📤 Saída                                    |
| Funcionalidade  | Campo "Status" na tabela de movimentações                   | ✔️     | Exibição com ✔ verde para Finalizado                                         |
| Funcionalidade  | Coluna "Histórico" adicionada                              | ✔️     | Link para detalhes do item em nova página                                    |
| Funcionalidade  | Remoção da coluna "Ações" da página de movimentações        | ✔️     | Agora só existe em Itens cadastrados                                         |
| Funcionalidade  | Relatório com filtros de período e destinatário             | ✔️     | Exportação CSV e impressão via botão                                         |
| Funcionalidade  | Histórico detalhado de cada item                           | ✔️     | Página dedicada mostrando movimentações e detalhes                           |
| Funcionalidade  | Etiqueta com botão Voltar                                  | ✔️     | Agora usa window.history.back() para retornar ao relatório com filtros       |
| Funcionalidade  | Etiqueta pronta para impressão                             | ✔️     | CSS @media print exibindo apenas a etiqueta, centralizada na página          |
| Interface       | Padronização completa dos botões (verde, vermelho, azul, cinza) | ✔️  | Implementado em style.css com variáveis CSS                                  |
| Interface       | Ícones visuais aplicados (👑, 👤, 📥, 📤, ✔)                | ✔️     | Implementados diretamente nos templates                                      |
| Interface       | Feedback visual (mensagens claras quando não há dados)      | ✔️     | Mensagens de "Nenhum dado exibido" e "Nenhuma movimentação registrada"       |
| Segurança       | Autenticação por níveis (admin, usuário comum)              | ✔️     | Implementado no backend com role e decorador @admin_required                 |
| Segurança       | Logs de auditoria (quem fez cada ação)                      | ✔️     | Campo user incluído em Movement                                              |
| Segurança       | Backup automático do banco                                 | ✔️     | Implementado com backup.py e agendamento via cron                            |
| Documentação    | README atualizado com guia rápido de uso                    | ✔️     | Inclui fluxo cadastrar → saída → relatório                                   |
| Documentação    | CHANGELOG.md inicial criado                                | ✔️     | Versão 1.1.0 documentando filtros, CSS e ícones visuais                      |
| Documentação    | RELATORIO.md consolidando evolução                         | ✔️     | Atualizado com todas as melhorias                                            |
| Funcionalidade  | Cadastro com status pendente/ativo/inativo                  | ✔️     | Implementado no modelo User e rotas /register e /validate_users              |
| Segurança       | Usuário define senha no cadastro                            | ✔️     | Campo senha incluído em register.html e rota /register                       |
| Funcionalidade  | Gestão de usuários com status e redefinição de senha        | ✔️     | Implementado em edit_user.html e create_user.html                            |
| Funcionalidade  | Relatório de usuários com status                           | ✔️     | Implementado em /users_report e template users_report.html                   |
| Funcionalidade  | 📊 Dashboard de estatísticas                                | 🚧     | Gráficos de movimentações por período, status e usuários (planejado v1.2.0)  |
| Funcionalidade  | 🔍 Busca avançada                                          | 🚧     | Pesquisa por múltiplos campos (remetente, destinatário, descrição)           |
| Funcionalidade  | 🗂️ Relatórios gráficos                                     | 🚧     | Visualização de entradas/saídas em formato de gráfico de barras/linhas       |
| Funcionalidade  | 🔔 Alertas automáticos                                     | 🚧     | Notificações para itens próximos do prazo de saída                           |
| Interface       | 🌐 Melhorias na interface                                  | 🚧     | Responsividade total para dispositivos móveis                                |
| Segurança       | 🛡️ Segurança extra                                         | 🚧     | Autenticação em dois fatores (2FA) para administradores                      |

---

## 📌 Observações finais
- As melhorias de **cadastro com status**, **senha definida pelo usuário**, **gestão de usuários com status** e **relatório de usuários** já estão implementadas, mas não estavam refletidas na versão anterior da tabela.  
- Próxima versão planejada (**v1.2.0**) deve focar em **dashboard estatístico**, **busca avançada**, **relatórios gráficos**, **alertas automáticos**, **responsividade mobile** e **2FA para administradores**.


---

## 👨‍💻 Autor
Projeto desenvolvido por **Junior Alexandre da Silva**  
GitHub: [@JuniorSilva88](https://github.com/JuniorSilva88)
