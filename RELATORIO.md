# 📑 Relatório de Evolução do Projeto — Sistema Correios

## 📌 Contexto
Projeto desenvolvido em **Python 3 + Flask + SQLAlchemy** para controle interno de documentos e pacotes.  
Funcionalidades principais: cadastro de itens, movimentações (entradas/saídas), relatórios filtrados e dashboard.

---

## 🛠️ Alterações Realizadas

### Funcionalidades
- **Filtros em movimentações por usuário, tipo e período** ✅  
- **Campo "Usuário" na tabela de movimentações** ✅  
- Busca avançada por protocolo, remetente, destinatário ou descrição ⏳  
- Exportação em PDF além de CSV ⏳  
- Notificações visuais/sonoras ao mudar status ⏳  
- Histórico detalhado de cada item ⏳  

### Interface
- **Padronização completa dos botões (verde, vermelho, azul, cinza)** ✅  
- **Botão "Registrar Saída" padronizado (fundo escuro, letras verdes)** ✅  
- Responsividade total para celular/tablet ⏳  
- Ícones visuais (📥 entrada, 📤 saída, ✅ finalizado) ⏳  
- Feedback visual (animação/destaque ao registrar ação) ⏳  

### Segurança
- Autenticação por níveis (admin, usuário comum) ⏳  
- Logs de auditoria (quem fez cada ação) ⏳  
- Backup automático do banco ⏳  

### Documentação
- **README atualizado com instruções claras e seção "Como acessar"** ✅  
- **CHANGELOG.md inicial criado** ✅  
- Guia rápido de uso (fluxo: cadastrar → saída → relatório) ⏳  
- RELATORIO.md consolidando evolução ⏳  

---

## 📊 Tabela Resumida

| Área           | Melhoria                                                                 | Status      | Observações                                                                 |
|----------------|--------------------------------------------------------------------------|-------------|------------------------------------------------------------------------------|
| Funcionalidade | **Filtros em movimentações por usuário, tipo e período**                 | **Feito**   | Implementado no template `movimentacoes.html`                                |
| Funcionalidade | **Campo "Usuário" na tabela de movimentações**                           | **Feito**   | Agora aparece junto às entradas/saídas                                       |
| Funcionalidade | Busca avançada por protocolo, remetente, destinatário ou descrição       | Pendente    | Pode ser implementada com query dinâmica no SQLAlchemy                       |
| Funcionalidade | Exportação em PDF além de CSV                                            | Pendente    | Usar biblioteca como ReportLab ou WeasyPrint                                 |
| Funcionalidade | Notificações visuais/sonoras ao mudar status                             | Pendente    | Pode ser feito com JavaScript + alertas                                      |
| Funcionalidade | Histórico detalhado de cada item                                         | Pendente    | Criar tabela de log de movimentações                                         |
| Interface      | **Padronização completa dos botões (verde, vermelho, azul, cinza)**      | **Feito**   | Implementado em `style.css`                                                  |
| Interface      | **Botão "Registrar Saída" padronizado (fundo escuro, letras verdes)**    | **Feito**   | Ajustado em `index.html`                                                     |
| Interface      | Responsividade total para celular/tablet                                 | Pendente    | Ajustar CSS com media queries                                                |
| Interface      | Ícones visuais (📥 entrada, 📤 saída, ✅ finalizado)                      | Pendente    | Adicionar ícones FontAwesome ou similares                                    |
| Interface      | Feedback visual (animação/destaque ao registrar ação)                    | Pendente    | Usar CSS transitions ou JS                                                   |
| Segurança      | Autenticação por níveis (admin, usuário comum)                           | Pendente    | Implementar roles no Flask-Login                                             |
| Segurança      | Logs de auditoria (quem fez cada ação)                                   | Pendente    | Criar tabela de auditoria                                                    |
| Segurança      | Backup automático do banco                                               | Pendente    | Script cron ou integração com ferramenta externa                             |
| Documentação   | **README atualizado com instruções claras e seção "Como acessar"**       | **Feito**   | Inclui links para init e dashboard                                           |
| Documentação   | **CHANGELOG.md inicial criado**                                          | **Feito**   | Versão 1.1.0 documentando filtros e CSS                                      |
| Documentação   | Guia rápido de uso (fluxo: cadastrar → saída → relatório)                | Pendente    | Adicionar no README                                                          |
| Documentação   | RELATORIO.md consolidando evolução                                       | Pendente    | Pode ser criado para histórico textual                                       |

---

## 👨‍💻 Autor
Projeto desenvolvido por **Junior Alexandre da Silva**  
GitHub: [@JuniorSilva88](https://github.com/JuniorSilva88)
