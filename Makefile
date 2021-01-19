create_database: _create_database
execute_ddl: _execute_ddl

CURRENT_DIR_PATH:=`pwd`
CURRENT_DIR_NAME:=`pwd | xargs basename`


_create_my_net:
	( \
    docker network create mynet; \
    )

_create_database: 
	( \
    docker run -p 5432:5432 -d \
    --net mynet \
    -e POSTGRES_PASSWORD=admin1234 \
    -e POSTGRES_USER=conscious \
    -e POSTGRES_DB=conscious_db \
    -v $(CURRENT_DIR_PATH)/data:/var/lib/postgresql/data \
    --name postgres_docker \
    postgres; \
    )

_create_schema:
	( \
    docker run -p 5432:5432 -d \
    -e POSTGRES_PASSWORD=admin1234 \
    -e POSTGRES_USER=conscious \
    -e POSTGRES_DB=conscious_db \
    -v $(CURRENT_DIR_PATH)/data:/var/lib/postgresql/data \
    --name postgres_docker \
    postgres; \
    )

_execute_ddl:
	( \
    docker run -i \
    --net mynet
	-w /$(CURRENT_DIR_NAME) \
	-v `pwd`:/$(CURRENT_DIR_NAME) \
    python:3 \
    /bin/bash -c "python3 scripts/execute_ddl.py" \
    )

_try:
	( \
    docker run \
    --net mynet \
	-w /$(CURRENT_DIR_NAME) \
	-v `pwd`:/$(CURRENT_DIR_NAME) \
    python:3 \
    /bin/bash -c "pip install -r requirements.txt && python3 main.py" \
    )

_start_cluster:
	( \
	docker-compose up -d postgres; \
	echo Starting postgres database; \
	sleep 30; \
	echo Starting Airflow; \
	docker-compose up initdb; \
	sleep 20; \
	docker-compose up webserver scheduler; \
	)


_create_postgres_connetion:
	( \
	docker-compose exec webserver airflow connections -a --conn_id postgres_airflow --conn_type postgres --conn_host postgres --conn_login airflow --conn_password airflow --conn_port 5432; \
	)