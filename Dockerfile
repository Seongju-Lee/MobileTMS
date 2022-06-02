FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./backend /app

RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
