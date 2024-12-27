# !/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${DIR}/../../.venv"
PROJECT="${DIR}/../../src"
ENV="${DIR}/../../docker/.env"


source "${VENV}/bin/activate"
source "${ENV}"

export PG_DATABASE_NAME="${PG_DATABASE_NAME}"
export PG_HOST="${PG_HOST}"
export PG_PORT="${PG_PORT}"
export PG_USER="${PG_USER}"
export PGPASSWORD="${PG_USER_PASSWORD}"

python "${PROJECT}/project/manage.py" "$@"

unset PG_DATABASE_NAME
unset PG_HOST
unset PG_PORT
unset PG_USER
unset PGPASSWORD