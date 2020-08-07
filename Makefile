DOMAIN := 127.0.0.1
SUBJ := "/C=/ST=/L=/O=/OU=/CN=$(DOMAIN)"

all:
	@echo 'Run "make build" for build Docker images by docker-composer.'

%.key:
	openssl genrsa -out $@ 2048
	# For access from Docker
	chmod uo+r $@

%.csr: %.key
	openssl req -new -key $< -out $@ -subj $(SUBJ)

%.crt: %.key %.csr
	openssl x509 -req -days 365 -in $(word 2,$^) -signkey $< -out $@

.PRECIOUS: %.crt %.csr %.key

show:
	openssl x509 -in server.crt -text -noout

start: build up migrate collectstatic loadfixtures
stop: down

build: server.crt
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

destroy:
	docker-compose down -v

migrate:
	docker-compose exec web python manage.py migrate --noinput

loadfixtures: migrate
	docker-compose exec web python manage.py loaddata users

collectstatic:
#	python ./src/manage.py collectstatic --noinput
	docker-compose exec web python manage.py collectstatic --noinput

prune:
	docker system prune

.PHONY: build show migrate collectstatic loadfixtures up down start stop destroy prune all
