# Visa For Lisa: runs the tests and executes the notebook headless.
#   docker build -t visa-for-lisa .
#   docker run --rm -v "$PWD:/app" visa-for-lisa                 # tests + executed notebook back on the host
#   docker run --rm -p 8888:8888 -v "$PWD:/app" visa-for-lisa \
#       jupyter lab --ip 0.0.0.0 --allow-root --no-browser         # interactive
# On a rate-capped line, pre-fetch wheels first (see ../wheelhouse.py) and build with
#   --build-arg UV_ARGS="--no-index --find-links /wheelhouse"
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/
# The venv lives outside /app so a host bind-mount of the project never shadows it.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never \
    PATH=/opt/venv/bin:$PATH
WORKDIR /app
COPY pyproject.toml uv.lock ./
ARG UV_ARGS=""
RUN --mount=type=bind,source=wheelhouse,target=/wheelhouse uv sync --frozen --no-cache $UV_ARGS
COPY . .
CMD ["sh", "-c", "pytest -q && jupyter nbconvert --to notebook --execute --inplace visa_for_lisa.ipynb"]
