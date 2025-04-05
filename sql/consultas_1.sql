SELECT 
    ano,
    SUM(CASE WHEN tipo_publicacao = 'Artigo' THEN 1 ELSE 0 END) AS artigos,
    SUM(CASE WHEN tipo_publicacao = 'Capítulo de livro' THEN 1 ELSE 0 END) AS capitulos_livros,
    SUM(CASE WHEN tipo_publicacao = 'Livro' THEN 1 ELSE 0 END) AS livros,
    SUM(CASE WHEN tipo_publicacao = 'Revisão' THEN 1 ELSE 0 END) AS revisoes
FROM data_tcc
GROUP BY ano
ORDER BY ano;



DELETE FROM data_tcc
WHERE tipo_publicacao NOT IN ('Artigo', 'Capítulo de livro', 'Livro', 'Revisão');


SELECT producao_nacional, tipo_publicacao, COUNT(*) AS quantidade 
FROM data_tcc
WHERE producao_nacional = 'sim'
GROUP BY producao_nacional, tipo_publicacao
ORDER BY quantidade DESC;




SELECT * from data_tcc
limit 15;


SELECT *
FROM data_tcc
WHERE tipo_publicacao IS NULL;


copy (SELECT * FROM data_tcc) TO 'C:\Temp\output.csv' WITH CSV HEADER;
