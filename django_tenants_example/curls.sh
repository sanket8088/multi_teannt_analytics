curl --location 'http://abc.localhost:8000/api/sales/top_months/'

curl -X 'POST' \
  'http://abc.localhost:8000/api/sales/trends/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_id": 1,
  "start_date": "2024-01-01",
  "end_date": "2024-07-01"
}'



curl --location 'http://abc.localhost:8000/api/sales/max_sales_customer/?start_date=2024-01&end_date=2024-07'
