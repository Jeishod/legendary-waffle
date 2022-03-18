# Makefile
format:
	make format-apps folder=api
	make format-apps folder=data

format-apps:
	isort ${folder}
	black ${folder}
	pflake8 ${folder}

start:
	uvicorn server.asgi:app --debug --reload --use-colors

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate
