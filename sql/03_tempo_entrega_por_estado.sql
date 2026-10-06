-- Tempo médio de entrega (dias) e % de atrasos por estado do cliente.
SELECT
  c.customer_state AS estado,
  COUNT(*)         AS pedidos,
  ROUND(AVG(TIMESTAMP_DIFF(o.order_delivered_customer_date, o.order_purchase_timestamp, HOUR)) / 24, 1) AS dias_medios_entrega,
  ROUND(100 * COUNTIF(o.order_delivered_customer_date > o.order_estimated_delivery_date) / COUNT(*), 1) AS pct_atrasados
FROM `extreme-hull-449521-e8.olist_ecommerce.orders` AS o
JOIN `extreme-hull-449521-e8.olist_ecommerce.customers` AS c USING (customer_id)
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY estado
ORDER BY dias_medios_entrega DESC;
