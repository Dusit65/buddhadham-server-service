.env
```
PORT = 0000
DATABASE_URL = "sqlserver://127.0.0.1:0000;initial catalog=DBName;user=Username;password=passw0rd;trustServerCertificate=true;charset=utf8mb4"
conn_str= "mssql+pyodbc://Username:passw0rd@127.0.0.1:0000/DBName?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
DB_SERVER = "127.0.0.1"
DB_PORT = "0000"
DB_USER = "Username"
DB_PASSWORD = "passw0rd"
DB_NAME = "DBName"
DB_DRIVER = "ODBC Driver 18 for SQL Server"
```

sqlcmd -S <ServerIP> -U <Username> -P <Password>
npx prisma migrate reset --force
npx prisma migrate dev --name init

git rm --cached config.json

python buddhamAI_cli.py ""

pip install faiss-cpu
pip install numpy
pip install ollama

#note
- embed_tb

"vercel-build": "npx prisma generate",
"postinstall": "prisma generate"