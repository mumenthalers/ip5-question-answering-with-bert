FROM python

# Install pipenv
RUN pip install pipenv

WORKDIR /app

ADD Pipfile* /app/

RUN set -ex \
    && pipenv install --system --deploy --ignore-pipfile

ADD ./ /app/
