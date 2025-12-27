# 📌 CHANGELOG — Sistema Correios

## [1.1.0] — 24/12/2025
### Adicionado
- Campo `status` no modelo **User** (`pendente`, `ativo`, `inativo`).
- Rota `/register` para cadastro de novos usuários.
- Rota `/validate_users` para validação de usuários pendentes.
- Bloqueio de login para usuários não validados (`status != "ativo"`).
- Template `register.html` com campos Nome, Telefone, Email.
- Botão "Criar Conta" em `login.html`.
- Template `validate_users.html` para validação de usuários.
- Rota `/edit_user` para edição de email, função e senha.
- Rota `/delete_user` para exclusão de usuários (exceto o próprio ADM).
- Relatório `/report` com filtros de período e destinatário.
- Exportação CSV em `/report_csv`.
- Histórico detalhado de cada item em página dedicada.
- Etiqueta pronta para impressão com CSS `@media print`.
- Backup automático do banco via `backup.py`.
- Documentação inicial em `README.md`, `CHANGELOG.md` e `RELATORIO.md`.

### Alterado
- Usuários antigos migrados para `status="ativo"`.
- Mensagens de feedback claras quando não há dados.
- Padronização completa dos botões (verde, vermelho, azul, cinza).
- Ícones visuais aplicados (👑, 👤, 📥, 📤, ✔).

---

## [1.2.0] — Em andamento
### Planejado
- 📊 Dashboard de estatísticas (gráficos de movimentações por período, status e usuários).
- 🔍 Busca avançada (remetente, destinatário, descrição).
- 🗂️ Relatórios gráficos (entradas/saídas em barras/linhas).
- 🔔 Alertas automáticos (notificações para itens próximos do prazo de saída).
- 🌐 Melhorias na interface (responsividade total para dispositivos móveis).
- 🛡️ Segurança extra (autenticação em dois fatores — 2FA — para administradores).
- Inclusão de links no menu lateral para `/users_report` e `/validate_users`.

---

## 📌 Observações
- Versão **1.1.0** consolidou segurança e gestão de usuários com status.  
- Versão **1.2.0** será focada em relatórios gráficos, estatísticas e segurança avançada.  
