Start-Process powershell -ArgumentList 'ollama serve'
Start-Sleep -Seconds 2
python manage.py runserver
