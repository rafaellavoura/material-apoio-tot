# Exercicio 03 - API Livros com SQS

1. Suba o ambiente local com o Floci usando: `docker compose up -d --build`
2. Inicie o servidor da API com: `uv run uvicorn app.main:app --reload`
3. Acesse a documentação interativa em: `http://localhost:8000/docs`
4. Para rodar os testes, execute: `uv run pytest`
5. Para verificar o estilo do código, execute: `uv run ruff check .`

# Solutions 3

1. Docker:
q
![image](../img/Ex-03-1.png)

1. Filas SQS FIFO:

![image](../img/Ex-03-2.png)