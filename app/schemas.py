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
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    """,
}

target_tables = {
    "sales_by_year_month": """
        CREATE TABLE IF NOT EXISTS sales_by_year_month (
        id int NOT NULL AUTO_INCREMENT,        
        year YEAR NOT NULL,
        month VARCHAR(2) NOT NULL,
        sum_qtd_venda int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
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
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    """,
    "sales_by_brand_year_month": """
        CREATE TABLE IF NOT EXISTS sales_by_brand_year_month (
        id int NOT NULL AUTO_INCREMENT,        
        id_marca int NOT NULL,
        year YEAR NOT NULL,
        month VARCHAR(2) NOT NULL,
        marca VARCHAR(100) NOT NULL,        
        sum_qtd_venda int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    """,
    "sales_by_category_year_month": """
        CREATE TABLE IF NOT EXISTS sales_by_category_year_month (
        id int NOT NULL AUTO_INCREMENT,        
        id_linha int NOT NULL,
        year YEAR NOT NULL,
        month VARCHAR(2) NOT NULL,
        linha VARCHAR(100) NOT NULL,        
        sum_qtd_venda int NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    """,
}
