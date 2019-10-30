FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /notes_project
WORKDIR /notes_project
COPY requirements.txt /notes_project/
RUN pip install -r requirements.txt
COPY . /notes_project/
WORKDIR /notes_project