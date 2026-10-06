-- Top 10 categorias de produto por receita (nome em inglês).
SELECT
  COALESCE(t.product_category_name_english, p.product_category_name, 'sem_categoria') AS categoria,
  COUNT(*)                AS itens_vendidos,
  ROUND(SUM(i.price), 2)  AS receita
FROM `extreme-hull-449521-e8.olist_ecommerce.order_items` AS i
JOIN `extreme-hull-449521-e8.olist_ecommerce.products` AS p USING (product_id)
LEFT JOIN `extreme-hull-449521-e8.olist_ecommerce.product_category_name_translation` AS t USING (product_category_name)
GROUP BY categoria
ORDER BY receita DESC
LIMIT 10;
