@echo off
cd /d "c:\Users\Capybaro75\Desktop\Proyecto hospital"
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install Flask==2.3.3 mysql-connector-python==8.0.33 python-dotenv==1.0.0 pytest==7.4.0 pytest-cov==4.1.0
echo ✓ Entorno configurado exitosamente
pause
