FROM python:3.11

ARG PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=500 \
    POETRY_VERSION=1.2.2

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install --upgrade pip
RUN python -m pip install "poetry==$POETRY_VERSION"


WORKDIR $APP_ROOT/src
COPY . ./

# Disable scl_enable (lol)
ENV BASH_ENV= \
    ENV= \
    PROMPT_COMMAND=
# Set poetry virtual env
ENV VIRTUAL_ENV=$APP_ROOT/src/.venv \
    PATH=$APP_ROOT/src/.venv/bin:$PATH

RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi --without dev

# TODO: change app.main:app if ASGI is in different location
CMD ["poetry", "run", "uvicorn", "app.api.main:bootstrap", \
    "--factory", \
    "--port", "8080", \
    "--host", "0.0.0.0"]
