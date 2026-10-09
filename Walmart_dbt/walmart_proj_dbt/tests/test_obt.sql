{{config(severity='warn')}}


SELECT 1 
FROM 
    {{ref("obt_b")}} AS obt
WHERE
    obt.order_id is null
OR
    obt.product_id is null

or 
    obt.employee_id is null
or 
    obt.store_id is null
or 
    obt.customer_id is null
or 
    obt.order_item_id is null