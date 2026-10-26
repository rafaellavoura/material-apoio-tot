CREATE TABLE IF NOT EXISTS livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano INTEGER NOT NULL
);

INSERT INTO livros (titulo, autor, ano) VALUES ('O Senhor dos Anéis', 'J.R.R. Tolkien', 1954);
INSERT INTO livros (titulo, autor, ano) VALUES ('Dom Casmurro', 'Machado de Assis', 1899);

SELECT * FROM livros;
