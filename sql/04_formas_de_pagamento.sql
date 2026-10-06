-- Participação de cada forma de pagamento no valor total e parcelamento médio.
SELECT
  payment_type                                         AS forma_pagamento,
  COUNT(DISTINCT order_id)                             AS pedidos,
  ROUND(SUM(payment_value), 2)                         AS valor_total,
  ROUND(100 * SUM(payment_value) / SUM(SUM(payment_value)) OVER (), 1) AS pct_do_valor,
  ROUND(AVG(payment_installments), 1)                  AS parcelas_medias
FROM `extreme-hull-449521-e8.olist_ecommerce.order_payments`
GROUP BY forma_pagamento
ORDER BY valor_total DESC;
