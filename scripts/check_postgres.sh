if [ -z `docker ps -q --no-trunc | grep $(docker-compose -f postgres.yml ps -q db)` ]; then
  echo "No, postgres is not running. Starting postgres"
  docker-compose -f postgres.yml up --build -d
else
  echo "Yes, postgres running."
fi
