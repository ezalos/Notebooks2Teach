# Drive Me Crazy: downloads the data and executes the four notebooks headless on the GPU.
#   docker build -t drive-me-crazy .
#   docker run --rm --gpus all -v "$PWD:/app" drive-me-crazy               # smoke: 1 epoch on PeMS08 (~1 min + data download)
#   docker run --rm --gpus all -v "$PWD:/app" -e DMC_EPOCHS=0 -e DMC_DATASETS= drive-me-crazy   # full run (~2 h)
#   docker run --rm --gpus all -p 8888:8888 -v "$PWD:/app" drive-me-crazy \
#       jupyter lab --ip 0.0.0.0 --allow-root --no-browser                # interactive
# Needs the NVIDIA Container Toolkit on the host; torch's wheels bundle CUDA, so no CUDA base image.
# On a rate-capped line, pre-fetch wheels first (see ../wheelhouse.py) and build with
#   --build-arg UV_ARGS="--no-index --find-links /wheelhouse"
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/
# The venv lives outside /app so a host bind-mount of the project never shadows it.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never \
    PATH=/opt/venv/bin:$PATH \
    DMC_EPOCHS=1 DMC_DATASETS=PEMS08
WORKDIR /app
COPY pyproject.toml uv.lock ./
ARG UV_ARGS=""
RUN --mount=type=bind,source=wheelhouse,target=/wheelhouse uv sync --frozen --no-cache $UV_ARGS
COPY . .
CMD ["sh", "-c", "python get_data.py && for nb in dataset_analysis drive_me_crazy_tradi drive_me_crazy_pdformer dashboard; do jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 $nb.ipynb || exit 1; done"]
