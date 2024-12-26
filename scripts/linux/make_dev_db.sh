make_dev_database() {
    DB_NAME="${PG_DATABASE_NAME}"

    echo "Checking if database '${DB_NAME}' exists."
    db_exists=$(psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -tAc \
        "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'")

    if [ "${db_exists}" == "1" ]; then
        echo "Database '${DB_NAME}' already exists."
    else
        echo "Creating database '${DB_NAME}'."
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -c \
            "CREATE DATABASE ${DB_NAME};"
    fi

    echo "Checking if user '${PG_USER}' exists."
    user_exists=$(psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -tAc \
        "SELECT 1 FROM pg_roles WHERE rolname='${PG_USER}'")

    if [ "${user_exists}" == "1" ]; then
        echo "User '${PG_USER}' already exists."
    else
        echo "Creating user '${PG_USER}'."
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -c \
            "CREATE USER ${PG_USER} WITH PASSWORD '${PG_USER_PASSWORD}';"
    fi

    echo "Granting all privileges on database '${DB_NAME}' to user '${PG_USER}'."
    psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -c \
        "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${PG_USER};"

}