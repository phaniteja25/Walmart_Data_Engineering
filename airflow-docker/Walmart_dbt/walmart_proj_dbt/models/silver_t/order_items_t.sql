{{ config(materialized='incremental',
    unique_key='order_item_id') 


}}


select *, current_timestamp() as processed_at

from 

{{ source('walmart_dbt', 'order_items') }}



{% if is_incremental() %}

    where updated_timestamp > COALESCE((select max(updated_timestamp) from {{ this }}), '1900-01-01')

{%endif%}





