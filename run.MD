``` cd backend
pip install -r requirements.txt
# 先执行 data.sql 建表，或让 SQLAlchemy 自动建表

uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

