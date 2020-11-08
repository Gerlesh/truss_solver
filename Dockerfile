FROM python:3.8-alpine
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
COPY webapp.py .
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "py", "webapp.py" ]
COPY . .