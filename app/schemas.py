source_tables = {
    "sales_report": """
        CREATE TABLE IF NOT EXISTS sales_report (
        id int NOT NULL AUTO_INCREMENT,
        id_marca int NOT NULL,
        id_linha int NOT NULL,
        data_venda DATE NOT NULL,
        qtd_venda int NOT NULL,
        marca VARCHAR(100) NOT NULL,
        linha VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
}

target_tables = {
    "sales_by_year_month": """
        CREATE TABLE IF NOT EXISTS sales_by_year_month (
        id int NOT NULL AUTO_INCREMENT,
        sale_year YEAR NOT NULL,
        sale_month VARCHAR(2) NOT NULL,
        sum_qtd_venda int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    "sales_by_brand_category": """
        CREATE TABLE IF NOT EXISTS sales_by_brand_category (
        id int NOT NULL AUTO_INCREMENT,
        id_marca int NOT NULL,
        id_linha int NOT NULL,
        marca VARCHAR(100) NOT NULL,
        linha VARCHAR(100) NOT NULL,
        sum_qtd_venda int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    "sales_by_brand_year_month": """
        CREATE TABLE IF NOT EXISTS sales_by_brand_year_month (
        id int NOT NULL AUTO_INCREMENT,
        id_marca int NOT NULL,
        sale_year YEAR NOT NULL,
        sale_month VARCHAR(2) NOT NULL,
        marca VARCHAR(100) NOT NULL,
        sum_qtd_venda int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    "sales_by_category_year_month": """
        CREATE TABLE IF NOT EXISTS sales_by_category_year_month (
        id int NOT NULL AUTO_INCREMENT,
        id_linha int NOT NULL,
        sale_year YEAR NOT NULL,
        sale_month VARCHAR(2) NOT NULL,
        linha VARCHAR(100) NOT NULL,
        sum_qtd_venda int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
}


spotify_tables = {
    "spotify_podcast": """
        CREATE TABLE IF NOT EXISTS spotify_podcast (
        id VARCHAR(100) NOT NULL,
        name VARCHAR(150) NOT NULL,
        description TEXT NOT NULL,
        total_episodes int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    "spotify_podcast_episodes": """
        CREATE TABLE IF NOT EXISTS spotify_podcast_episodes (
        id VARCHAR(100) NOT NULL,
        podcast_id VARCHAR(100) NOT NULL,
        name VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        release_date DATE NOT NULL,
        duration_ms INT NOT NULL,
        language VARCHAR(50) NOT NULL,
        explicit BOOLEAN NOT NULL,
        type VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    "spotify_gb_podcast_episodes": """
        CREATE TABLE IF NOT EXISTS spotify_gb_podcast_episodes (
        id VARCHAR(100) NOT NULL,
        podcast_id VARCHAR(100) NOT NULL,
        name VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        release_date DATE NOT NULL,
        duration_ms INT NOT NULL,
        language VARCHAR(50) NOT NULL,
        explicit BOOLEAN NOT NULL,
        type VARCHAR(50) NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
}
