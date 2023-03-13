SELECT
id_marca,marca,id_linha,linha,sum(qtd_venda) as sum_qtd_venda
FROM sales_report
group by 1,2,3,4;
