# 📑 CHANGELOG

## [1.2.0] - 2025-12-19
### Funcionalidades
- Adicionados filtros completos em movimentações (usuário, tipo e período)
- Incluídos campos extras na tabela de movimentações:
  - Usuário (👑 admin / 👤 usuário)
  - Tipo (📥 Entrada / 📤 Saída)
  - Status (✔ Finalizado)
- Criada coluna **Histórico** com link para detalhes do item
- Implementado relatório com filtros de período e destinatário
- Adicionados botões padronizados para **Gerar**, **Exportar CSV** e **Imprimir resultado**
- Página de histórico detalhado de item criada com tabela de movimentações
- Mensagens claras quando não há dados ou item não encontrado

### Interface
- Padronização completa dos botões (verde, vermelho, azul, cinza) com variáveis CSS
- Ícones visuais aplicados em movimentações (👑, 👤, 📥, 📤, ✔)
- Feedback visual implementado:
  - Destaque em linhas recém-adicionadas/atualizadas
  - Mensagens de "Nenhum dado exibido" e "Nenhuma movimentação registrada"
- Responsividade aplicada com media queries para telas menores (768px e 480px)

### Segurança
- Autenticação por níveis (admin, usuário comum) consolidada
- Logs de auditoria registrando quem fez cada ação
- Backup automático do banco implementado com `backup.py` e agendamento via cron

### Documentação
- README atualizado com guia rápido de uso (fluxo: cadastrar → saída → relatório)
- Instruções de backup automático adicionadas ao README
- RELATORIO.md consolidado com todas as melhorias
- CHANGELOG.md atualizado para versão 1.2.0

---

## [1.1.0] - 2025-12-15
### Funcionalidades
- Filtros básicos em movimentações
- Exibição inicial de campos adicionais

### Interface
- Padronização inicial de botões
- Ícones visuais aplicados em movimentações

### Documentação
- CHANGELOG.md inicial criado
