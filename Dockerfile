FROM python:3.10

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY *.py /usr/src/app/
COPY src/* /usr/src/app/src/

EXPOSE 5000

CMD ["python", "/usr/src/app/docker_app.py"]