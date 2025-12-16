📄 README.md ajustado

# 📬 Sistema Correios

Aplicação desenvolvida em **Python 3 + Flask + SQLAlchemy** para controle interno de documentos e pacotes.  
Permite cadastrar itens, acompanhar movimentações, registrar saídas e gerar relatórios filtrados por datas e seções.

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/JuniorSilva88/sistema-correios.git
cd sistema-correios

2. Crie e ative o ambiente virtual

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Instale as dependências

pip install flask flask_sqlalchemy

4. Inicie o servidor

python3 app.py

🌐 Como acessar

Após iniciar o servidor, abra o navegador e acesse:

Inicializar banco de dados:http://127.0.0.1:5000/init

Dashboard principal:http://127.0.0.1:5000/

📂 Estrutura do projeto

Sistema Correios/
 ├── app.py                # Código principal Flask
 ├── templates/            # Templates HTML
 │   ├── base.html
 │   ├── index.html
 │   ├── new_item.html
 │   ├── movimentacoes.html
 │   ├── exit_item.html 
 │   └── report.html
 └── static/               # Arquivos estáticos (CSS, imagens)
     └── style.css

✨ Funcionalidades

Dashboard: lista todos os itens cadastrados com status e ações.

Cadastro de itens: gera protocolo automático e registra entrada.

Movimentações: histórico de entradas e saídas de cada item, com filtros por usuário, tipo e período.

Saída de itens: marca como entregue e fecha protocolo.

Relatórios: filtro por datas e seções, exportação em CSV.

👨‍💻 Autor

Projeto desenvolvido por Júnior Alexandre da SilvaGitHub: @JuniorSilva88


---

## 🎯 O que mudou
- Corrigi os blocos de código para ficarem consistentes (`bash`).  
- Adicionei instruções para ativar o ambiente virtual tanto em Linux/Mac quanto em Windows.  
- Padronizei o nome do template `movimentacoes.html`.  
- Criei a seção **Como acessar**, com links diretos para inicializar o banco e abrir o dashboard.  
- Atualizei a lista de funcionalidades para incluir os filtros que implementamos.  

---