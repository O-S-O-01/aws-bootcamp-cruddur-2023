FROM python:3.10-slim-bookworm

# inside container
# make a new folder inside container 
WORKDIR /backend-flask

#outside container -> inside container
# this contains the libraries we want to install to run the app
COPY requirements.txt requirements.txt

# inside container 
#install the python libraries used for the app
RUN pip3 install -r requirements.txt

# outside container -> inside container 
#  (.) means everything in the current directory
# firt period(. ) /backend-flask (outside the container)
# second period(. ) /backend-flask (inside the container)
COPY . .

#set environment variable inside the container and remain there
ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"] 
