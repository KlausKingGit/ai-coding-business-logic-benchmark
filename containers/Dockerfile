FROM python:3.12.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=0 \
    PYTEST_ADDOPTS="-p no:cacheprovider" \
    HOME=/tmp

WORKDIR /benchmark

COPY requirements.lock /benchmark/requirements.lock
RUN python -m pip install --no-cache-dir -r requirements.lock \
    && python -m pip check

COPY benchmark.json pyproject.toml fixture_expectations.json /benchmark/
COPY evaluator /benchmark/evaluator
COPY shared /benchmark/shared
COPY tasks /benchmark/tasks

ENTRYPOINT ["python", "evaluator/runner.py"]
