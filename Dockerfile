# pull official base image
FROM python:3.6

# set environmet variables
ENV PYTHONUNBUFFERED 1

# create project directories
RUN mkdir /notes_project
WORKDIR /notes_project

# install dependencies
COPY requirements.txt /notes_project/
RUN pip install -r requirements.txt

# copy project
COPY . /notes_project/

# cd project directory
WORKDIR /notes_project