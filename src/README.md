# Forge-Fitness


## First time development setup:
1. Copy the `example.env` file within the `./docker` directory, naming it just `.env`. Set the values as you want
2. Start up the dev container.
3. Once inside the dev container, run the `./scripts/linux/setup_dev.sh` to build the venv, install requirements, make migrations as well as run the migrations.
```shell
cp ./docker/example.env ./docker/.env
nano ./docker/.env
# Once inside the dev container
./scripts/linux/setup_dev.sh
```

---

## Running tests and migrations
You can use either `./scripts/linux/manage.sh` or `./src/project/manage.py` to run the django commands. Both ways require an
env file placed in `/workspace/docker/.env`.
```shell
./scripts/linux/manage.sh makemigrations
./scripts/linux/manage.sh migrate
./scripts/linux/manage.sh test
```
OR
```shell
./src/project/manage.py makemigrations
./src/project/manage.py migrate
./src/project/manage.py test
```