-- Receita mensal e ticket médio dos pedidos entregues.
-- Receita = soma de price dos itens (sem frete).
SELECT
  FORMAT_TIMESTAMP('%Y-%m', o.order_purchase_timestamp) AS mes,
  COUNT(DISTINCT o.order_id)                            AS pedidos,
  ROUND(SUM(i.price), 2)                                AS receita,
  ROUND(SUM(i.price) / COUNT(DISTINCT o.order_id), 2)   AS ticket_medio
FROM `extreme-hull-449521-e8.olist_ecommerce.orders` AS o
JOIN `extreme-hull-449521-e8.olist_ecommerce.order_items` AS i USING (order_id)
WHERE o.order_status = 'delivered'
GROUP BY mes
ORDER BY mes;
