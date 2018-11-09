FROM python:3.6
RUN pip3.6 install pipenv
WORKDIR /app/comments
ADD comments /app/comments/comments
COPY Pipfile /app/comments
RUN pipenv install
CMD pipenv run api