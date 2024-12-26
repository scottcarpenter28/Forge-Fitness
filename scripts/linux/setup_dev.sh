# !/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${DIR}/../../.venv"
PROJECT="${DIR}/../../src"
ENV="${DIR}/../../docker/.env"

echo "Setting up virtual environment."
python -m venv "${VENV}"
source "${VENV}/bin/activate"

echo "Installing dependencies."
pip install -e "${PROJECT}"[development]

source "${ENV}"
source "${DIR}/make_dev_db.sh"
source "${DIR}/migrate.sh"

export PG_DATABASE_NAME="${PG_DATABASE_NAME}"
export PG_HOST="${PG_HOST}"
export PG_PORT="${PG_PORT}"
export PG_USER="${PG_USER}"
export PGPASSWORD="${PG_USER_PASSWORD}"

make_dev_database
create_and_run_migrations

unset PG_DATABASE_NAME
unset PG_HOST
unset PG_PORT
unset PG_USER
unset PGPASSWORD