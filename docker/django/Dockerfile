FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    postgresql-client gettext graphviz graphviz-dev\
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8000

ARG GID UID

RUN groupadd -g "${GID}" -r django \
    && useradd -g django -l -r -u "${UID}" django

USER django

COPY --chown=django:django . .

COPY --chown=django:django . /var/www

RUN python manage.py collectstatic

RUN python manage.py compilemessages 

ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]