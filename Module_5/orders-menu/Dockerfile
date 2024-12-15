FROM public.ecr.aws/docker/library/python:3.9.17-slim-bullseye

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000 

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]