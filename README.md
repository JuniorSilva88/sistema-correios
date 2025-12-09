📬 Sistema Correios
Aplicação desenvolvida em Python 3 + Flask + SQLAlchemy para controle interno de documentos e pacotes.
Permite cadastrar itens, acompanhar movimentações, registrar saídas e gerar relatórios filtrados por datas e seções.

🚀 Como rodar o projeto


Clone o repositório:
git clone https://github.com/JuniorSilva88/sistema-correios.gitcd sistema-correios


Crie e ative o ambiente virtual:
python3 -m venv venvsource venv/bin/activate


Instale as dependências:
pip install flask flask_sqlalchemy


Inicie o servidor:
``bash
python3 app.py


Abra no navegador:
Inicializar banco: http://127.0.0.1:5000/init
Dashboard: http://127.0.0.1:5000/


📂 Estrutura do projeto
 
  Sistema Correios/
 ├── app.py                # Código principal Flask
 ├── templates/            # Templates HTML
 │   ├── base.html
 │   ├── index.html
 │   ├── new_item.html
 │   ├── movements.html
 │   ├── exit_item.html 
 │   └── report.html
 └── static/               # Arquivos estáticos (CSS, imagens)
    └── style.css

✨ Funcionalidades
Dashboard: lista todos os itens cadastrados com status e ações.

Cadastro de itens: gera protocolo automático e registra entrada.

Movimentações: histórico de entradas e saídas de cada item.

Saída de itens: marca como entregue e fecha protocolo.

Relatórios: filtro por datas e seções, exportação em CSV.

👨‍💻 Autor
Projeto desenvolvido por Júnior Alexandre da Silva GitHub: @JuniorSilva88
