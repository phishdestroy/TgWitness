FROM cgr.dev/chainguard/wolfi-base@sha256:be019c1c74fe69204a42c4e10bc4d886a49bf5403ffa74374ef7baa408fc9a26
LABEL org.opencontainers.image.title="TgWitness" \
      org.opencontainers.image.description="Self-hosted Telegram observation journal with signed exports" \
      org.opencontainers.image.licenses="MIT"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONUTF8=1 PIP_DISABLE_PIP_VERSION_CHECK=1 TGWITNESS_DATA=/data \
    TGWITNESS_STATE_DIR=/state PATH="/opt/venv/bin:$PATH"
COPY deploy/containers /usr/share/tgwitness-build/containers
RUN sh /usr/share/tgwitness-build/containers/install-packages.sh runtime \
    && python3.12 -m venv /opt/venv
WORKDIR /app
COPY pyproject.toml README.md LICENSE NOTICE ./
COPY deploy/build.lock deploy/requirements.lock ./
COPY tgwitness ./tgwitness
COPY tgwitness_capture ./tgwitness_capture
COPY tgwitness_analyzer ./tgwitness_analyzer
RUN pip install --no-cache-dir --require-hashes -r build.lock \
    && pip install --no-cache-dir --require-hashes --no-build-isolation -r requirements.lock \
    && pip install --no-cache-dir --no-deps --no-build-isolation . \
    && python -m pip check && python -m pip uninstall --yes pip \
    && addgroup -g 10001 collector && adduser -D -u 10001 -G collector -h /home/collector collector \
    && mkdir /data /witness /state && chown collector:collector /data /witness /state
USER collector
VOLUME ["/data"]
EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/', timeout=4)" || exit 1
CMD ["python", "-m", "tgwitness", "--host", "0.0.0.0"]
