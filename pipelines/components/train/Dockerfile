FROM python:3.9-slim

WORKDIR /work

COPY ./forecasting /work/forecasting
COPY ./components/train /work/components/train

RUN pip install --no-cache-dir -r /work/components/train/runtime-requirements.txt

# Python PATH
ENV PYTHONPATH="/work:${PYTHONPATH}"

# Exec command for component
ENTRYPOINT ["python", "/work/components/train/train.py"]
