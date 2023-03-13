SELECT
id_marca,
marca,
YEAR(data_venda) as sale_year,
MONTH(data_venda) as sale_month,
sum(qtd_venda) as sum_qtd_venda
FROM sales_report
group by 1,2,3,4;