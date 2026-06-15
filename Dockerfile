FROM python:3.8-alpine

# Install build dependencies
RUN apk add --no-cache make gcc musl-dev libffi-dev postgresql-dev

# working directory
WORKDIR /app

# requirements and Makefile
COPY requirements.txt Makefile ./

# venv and dependencies
RUN make venv && make install

# main code
COPY . .

# script permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# port
EXPOSE 5000

# entrypoint
ENTRYPOINT ["/entrypoint.sh"]
