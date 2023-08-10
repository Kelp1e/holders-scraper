FROM python:3.11.4-alpine

WORKDIR usr/src/app

ENV DB_HOST="localhost"
ENV DB_PORT=5432
ENV DB_NAME="hikuru_database"
ENV DB_USERNAME="postgres"
ENV DB_PASSWORD="root"
ENV EVM_API_KEYS="[\"2TALosinLGKtUvTQaUR5UjnSn3n\", \"2TKqh6mWbXWpCrg2kbyl1hy2rpu\"]"
ENV TRON_API_KEYS="[\"16ceae68-c739-4dbd-bf55-f70dce7ad940\"]"
ENV LIMITS="[800, 500, 250]"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]