from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

sales_by_year_month = Table(
    "sales_by_year_month",
    meta,
    Column("id", Integer, primary_key=True),
    Column("sale_year", String, nullable=True),
    Column("sale_month", String, nullable=False),
    Column("sum_qtd_venda", Integer, nullable=False),
)
