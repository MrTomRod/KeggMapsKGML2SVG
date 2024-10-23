FROM ghcr.io/astral-sh/uv:python3.12-alpine
# Inspiration: https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv,Z \
    --mount=type=bind,source=uv.lock,target=uv.lock,Z \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml,Z \
    uv sync --frozen --no-install-project --no-dev

# Add the project files and install the package in editable mode
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv,Z \
    uv pip install -e .

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Set environment variable for KEGG_MAP_WIZARD_DATA
ENV KEGG_MAP_WIZARD_DATA=/KEGG_MAP_WIZARD_DATA

# Set the working directory to /data
WORKDIR /data