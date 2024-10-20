FROM python:3.9-slim

WORKDIR /work

COPY ./forecasting /work/forecasting
COPY ./components/preprocess /work/components/preprocess

RUN pip install --no-cache-dir -r /work/components/preprocess/runtime-requirements.txt

# Python PATH
ENV PYTHONPATH="/work:${PYTHONPATH}"

# Exec command for component
ENTRYPOINT ["python", "/work/components/preprocess/preprocess.py"]
