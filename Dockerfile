FROM python:3.7-alpine


# App user
RUN adduser -D appuser

# Work Directory
WORKDIR /home/evite

# Copy python dependency list
COPY requirements.txt requirements.txt

# Install required dependecies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app files
COPY . .

RUN chown -R appuser:appuser ./

USER appuser

RUN ls -lrth

CMD python app.py