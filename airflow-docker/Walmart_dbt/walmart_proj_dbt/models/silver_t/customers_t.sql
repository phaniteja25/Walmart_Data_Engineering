{{ config(materialized='incremental',
    unique_key='customer_id') 


}}


select *, current_timestamp() as processed_at

from 

{{ source('walmart_dbt', 'customers') }}


{% if is_incremental() %}

    WHERE updated_timestamp > COALESCE((select max(updated_timestamp) from {{ this }}), '1900-01-01')

{%endif%}





