FROM python:3.9

RUN useradd --create-home userapi
WORKDIR /REstFullAPI

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN pip install -U pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system
COPY ./ .
RUN chown -R userapi:userapi ./
USER userapi

EXPOSE 8000 
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app