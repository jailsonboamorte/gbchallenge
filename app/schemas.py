tables = {
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
