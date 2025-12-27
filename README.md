## 📦 Sistema Correios Interno

```markdown

Aplicação Flask para controle de entrada e saída de correspondências internas, com geração de protocolos automáticos e relatórios.

---

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/JuniorSilva88/sistema-correios.git
   cd sistema-correios
   ```

2. Crie o ambiente virtual e instale as dependências:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   flask run
   ```

---

## 📖 Guia rápido de uso

Fluxo básico de utilização:

1. **Cadastrar novo item**
   - Menu *Cadastrar Novo Item*
   - Preencha descrição e destinatário
   - Sistema gera protocolo único

2. **Registrar saída**
   - Menu *Movimentações*
   - Localize item pelo protocolo ou descrição
   - Registre como *Saída* (📤)
   - Status atualizado para *Em trânsito* ou *Finalizado*

3. **Gerar relatório**
   - Menu *Gerar Relatório*
   - Defina período e destinatário
   - Clique em *Gerar*
   - Opções de *Exportar CSV* ou *Imprimir*

✅ Fluxo resumido:
```
Cadastrar → Saída → Relatório
```

Esse é o ciclo principal para acompanhar os itens dentro do sistema.

---

## 🛠️ Funcionalidades

- Cadastro de itens com protocolo automático  
- Registro de entradas e saídas  
- Relatórios filtrados por datas e seções  
- Exportação em CSV  
- Histórico de movimentações  
- Backup automático dos bancos SQLite (`backup.py` + cron)

---

## 💾 Backup automático

O sistema inclui o script `backup.py` para gerar cópias dos bancos SQLite (`correios.db` e `mailtrack.db`) na pasta `backups/`.

### Executar manualmente
```bash
python3 backup.py
```

### Configurar cron (Linux)
Edite o crontab:
```bash
crontab -e
```

Adicione a linha para rodar diariamente às 2h da manhã:
```bash
0 2 * * * /usr/bin/python3 /home/usuario/Documentos/GitHub/sistema-correios/backup.py
```

Os arquivos serão salvos em `backups/` com timestamp no nome.

---

## 👨‍💻 Autor

Projeto desenvolvido por **Junior Alexandre da Silva**  
GitHub: [@JuniorSilva88](https://github.com/JuniorSilva88)
```