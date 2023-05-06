source .env

docker-compose -f docker-compose.yml up --build --remove-orphans --detach dbt_runtime

echo "Local Environment UP"