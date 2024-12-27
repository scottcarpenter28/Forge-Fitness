make_dev_database() {
    echo "Checking if database '${PG_DATABASE_NAME}' exists."
    db_exists=$(psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -tAc \
        "SELECT 1 FROM pg_database WHERE datname='${PG_DATABASE_NAME}'")

    if [ "${db_exists}" == "1" ]; then
        echo "Database '${PG_DATABASE_NAME}' already exists."
    else
        echo "Creating database '${PG_DATABASE_NAME}'."
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -c \
            "CREATE DATABASE ${PG_DATABASE_NAME};"
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

    echo "Granting all privileges on database '${PG_DATABASE_NAME}' to user '${PG_USER}'."
    psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -c \
        "GRANT ALL PRIVILEGES ON DATABASE ${PG_DATABASE_NAME} TO ${PG_USER};"

    psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_ADMIN}" -c \
            "ALTER USER ${PG_USER} CREATEDB;"

}