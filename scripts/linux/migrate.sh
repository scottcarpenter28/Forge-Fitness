# !/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${DIR}/../../.venv"
PROJECT="${DIR}/../../src"
ENV="${DIR}/../../docker/.env"


create_and_run_migrations() {
  echo "Running database migrations"
  source "${VENV}/bin/activate"
  python "${PROJECT}/project/manage.py" makemigrations
  python "${PROJECT}/project/manage.py" migrate
}
