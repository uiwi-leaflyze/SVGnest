# 설치 및 서버 실행
```bash
# Install dependencies
poetry install

# Start the server
poetry run gunicorn --workers 4 --bind 0.0.0.0:8124 server:app
```