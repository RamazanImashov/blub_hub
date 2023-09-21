# BlubHub_final-hackathon
1 Установить Python 3.11    |      
2 Создать интерпритатор Python в дериктории файли manage.py -- $ python3 -m venv venv    |   
3 Активировать интерпритатор Python  -- $ . venv/bin/activate           |
4 Установить зависимости из файла requierments.txt -- $ pip3 install -r requierments.txt      |    
5 Установить PostgresQL --      |      
5.1      $ brew install postgresql      |      
5.2      $ brew services start postgresql # or "brew services run postgresql" to have it not restart at boot time      |      
5.3      $ CREATE USER <psql_user> WITH PASSWORD 'psql_user_password'; (пароль не обязательно)      |      
6 Создать базу данных в PostgresQL --      |      
6.1      открыть PostgresQL -- $ psql postgres      |    
6.2      $ CREATE DATABASE <db_name>;      |      
6.3      $ \q (что бы выйти)      |      
7 Создать пароль отправки сообщений      |      
7.1 Октрайте панель управления аккаунтом      |      
7.2 Перейдите в безопасность      |      
7.3 Нажмите на двухэтапную аудентификацию      |      
7.4 Введите почту и пароль      |      
7.5 Перейдите в самый низ и нажмите на (Пароли приложений)      |      
7.6 Создайте приложение с названем (QDPro) и сохраните пароль (позже нельзя будет его найти)      |      
8 Создайте файл .env       |    
8.1 Запишите в него это --       |      
DEBUG = False      |      
DB_NAME = <db_name>        |      
DB_USER = <psql_user>      |      
DB_PASS = <psql_user_password>      |      
DB_HOST = localhost      |      
        |      
EMAIL_HOST_USER = email почта      |      
EMAIL_HOST_PASSWORD = Пароль из гугл      |      
9 Проведите миграцию -- ./manage.py migrate       |      
10 Запустите сервер -- ./manage.py runserver      |      
(если надо создать новое приложение) -- ./manage.py startapp <django app name>      |        
После изменений в models.py создайте и проведите миграцию        |      
./manage.py makemigrations      |      
./manage.py migrate         |        
