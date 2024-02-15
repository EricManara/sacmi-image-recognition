FROM python:3.11.8

RUN apt-get -y update
RUN apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR sacmi_recognition
COPY poetry.lock pyproject.toml /sacmi_recognition/
RUN POETRY_VIRTUALENVS_CREATE=false /root/.local/bin/poetry install
COPY . /sacmi_recognition/
CMD ["uvicorn", "fastapi_serverless_starter.main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000