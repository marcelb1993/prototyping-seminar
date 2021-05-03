# Pull and run linux os with python
FROM python:3.9

# install the required python packages on to the os
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy all files from current directory into the root directory 
COPY . .

# expost the container to the the localhost on port 8000: Access this container under http://localhost:8000/, the swagger api under http://localhost:8000/docs
EXPOSE 8001

# run this command to start the uvicorn server on the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]