FROM python:3.12-slim as app
ENV PYTHONPATH "${PYTHONPATH}:/RMH/main"
WORKDIR /RMH
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /RMH/start.sh
CMD [ "./start.sh" ]