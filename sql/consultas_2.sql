WITH SplitAuthors AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor
    FROM 
        data_tcc
)
SELECT 
    autor, 
    COUNT(*) AS quantidade
FROM 
    SplitAuthors
GROUP BY 
    autor
ORDER BY 
    quantidade DESC;



WITH SplitAuthors AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor,
        titulo_obra
    FROM 
        data_tcc
)
SELECT 
    autor, 
    COUNT(*) AS quantidade,
    STRING_AGG(titulo_obra, '; ') AS titulos
FROM 
    SplitAuthors
GROUP BY 
    autor
ORDER BY 
    quantidade DESC;


WITH SplitAuthors AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor
    FROM 
        data_tcc
    WHERE 
        producao_nacional = 'sim'
)
SELECT 
    autor, 
    COUNT(*) AS quantidade
FROM 
    SplitAuthors
GROUP BY 
    autor
ORDER BY 
    quantidade DESC;
	
	

DROP VIEW IF EXISTS publica_rankedbyREVISTA;

CREATE VIEW publica_rankedbyREVISTA AS
    SELECT 
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS RankingNumber,
        publicacao AS Revista,
        COUNT(*) AS "Total de Publicações"
    FROM 
        data_tcc
    WHERE 
        producao_nacional = 'sim' AND tipo_publicacao = 'Artigo'
    GROUP BY 
        publicacao;



SELECT * from publica_rankedbyrevista;



------ CODIGO QUE LISTA MAS HÁ NULLS V1 --------
WITH SplitAuthors AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor,
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(publicacao, ','))) AS revista
    FROM 
        data_tcc
    WHERE 
        producao_nacional = 'sim'
)
SELECT 
    autor, 
    revista,
    COUNT(*) AS quantidade
FROM 
    SplitAuthors
GROUP BY 
    autor, revista
ORDER BY 
    quantidade DESC;

------ CODIGO QUE LISTA MAS HÁ NULLS V2 --------
WITH SplitAuthors AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor,
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(publicacao, ','))) AS revista
    FROM 
        data_tcc
    WHERE 
        producao_nacional = 'sim'
)
SELECT 
    autor, 
    STRING_AGG(revista, '; ') AS publicacoes,
    COUNT(*) AS quantidade
FROM 
    SplitAuthors
GROUP BY 
    autor
ORDER BY 
    quantidade DESC;
----

--------------------------- SEI O QTD - MAS N SEI A REVISTA -------------------
WITH Separa_autor AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor
    FROM 
        data_tcc
    WHERE 
        producao_nacional = 'sim'
),
Conta_autor AS (
    SELECT 
        autor,
        COUNT(*) AS quantidade
    FROM 
        Separa_autor
    GROUP BY 
        autor
)
SELECT 
    autor,
    quantidade
FROM 
    Conta_autor
ORDER BY 
    quantidade DESC;




----------------------- LISTA QUE FUNCIONOU --------------
WITH SplitAuthors AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor,
        publicacao
    FROM 
        data_tcc
    WHERE 
        producao_nacional = 'sim'
),
AuthorCounts AS (
    SELECT 
        autor,
        publicacao,
        COUNT(*) AS quantidade
    FROM 
        SplitAuthors
    GROUP BY 
        autor, publicacao
),
AuthorPublicationSummary AS (
    SELECT 
        autor,
        STRING_AGG(publicacao || ' (' || quantidade || ')', ', ') AS publicacoes,
        SUM(quantidade) AS total_publicacoes
    FROM 
        AuthorCounts
    GROUP BY 
        autor
)
SELECT 
    autor,
    publicacoes,
    total_publicacoes
FROM 
    AuthorPublicationSummary
ORDER BY 
    total_publicacoes DESC;


-------------------------------------------
-- 1. dividir os autores
WITH DividirAutores AS (
    SELECT 
        TRIM(BOTH ' ' FROM UNNEST(STRING_TO_ARRAY(autores, ','))) AS autor,
        publicacao
    FROM 
        data_tcc
    WHERE 
        producao_nacional = 'sim'
),

-- 2. numero de ocorrencias em cada pub
ContarAutores AS (
    SELECT 
        autor,
        publicacao,
        COUNT(*) AS quantidade
    FROM 
        DividirAutores
    GROUP BY 
        autor, publicacao
),

-- 3. Ordenar as publicações por autor e pela quantidade de ocorrências (em ordem decrescente)
PublicacoesOrdenadas AS (
    SELECT 
        autor,
        publicacao,
        quantidade
    FROM 
        ContarAutores
    ORDER BY 
        autor, quantidade DESC
),

-- 4. Agregar as publicações em uma única string para cada autor - mantendo a ordem das quantidades
AgregacaoPublicacoes AS (
    SELECT 
        autor,
        STRING_AGG(publicacao || ' (' || quantidade || ')', ', ') AS publicacoes,
        SUM(quantidade) AS total_publicacoes
    FROM 
        PublicacoesOrdenadas
    GROUP BY 
        autor
)

-- 5. Selecionar o autor, as publicações e o total de publicações, e ordenar os autores pelo total de publicações
SELECT 
    autor,
    publicacoes,
    total_publicacoes
FROM 
    AgregacaoPublicacoes
ORDER BY 
    total_publicacoes DESC;
