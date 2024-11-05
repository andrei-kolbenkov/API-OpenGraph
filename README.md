Этот проект на Django представляет собой REST API для управления ссылками (медиаресурсы), которые пользователь может добавлять, обновлять и организовывать в коллекции. При добавлении ссылки пользователь передает только url. Остальные данные сервис получает сам через OpenGraph разметку в HTML коде страницы.

This Django project is a REST API for managing links (media resources) that the user can add, update, and organize into collections. When adding a link, the user only passes the url. The service receives the rest of the data itself through OpenGraph markup in the HTML code of the page.

- Python 3.12.3
- Django 5.1.2
- OpenGraph
- DRF
- Docker


Инструкция по запуску проекта

1. Убедитесь, что Docker установлен и запущен на вашем компьютере. Запустите команду, чтобы проверить, работает ли Docker и доступен ли он:
docker info
2. Перейдите в корневую директорию вашего проекта, где находится docker-compose.yml.
3. Выполните команду:
docker-compose up --build
4. Дождитесь завершения процесса. Вы увидите логи, в которых будет указано, что контейнеры запущены.
5. Откройте браузер и перейдите по адресу: http://127.0.0.1:8000/, чтобы увидеть ваше приложение.
6. http://127.0.0.1:8000/swagger/
7. http://127.0.0.1:8000/redoc/
8. Чтобы остановить приложение, используйте комбинацию клавиш CTRL+C в терминале, где оно запущено, либо выполните команду: 
docker-compose down
9. Запуск контейнера: docker-compose up


Instructions for running the project

1. Make sure Docker is installed and running on your machine. Run the command to check if Docker is running and accessible:
docker info
2. Go to the root directory of your project, where docker-compose.yml is located.
3. Run the command:
docker-compose up --build
4. Wait for the process to complete. You will see logs indicating that the containers are running.
5. Open a browser and go to: http://127.0.0.1:8000/ to see your application.
6. http://127.0.0.1:8000/swagger/
7. http://127.0.0.1:8000/redoc/
8. To stop the application, use the keyboard shortcut CTRL+C in the terminal where it is running, or run the command:
docker-compose down
9. Starting the container: docker-compose up

Данные суперпользователя.
- Логин: admin 
- Пароль: 12345

Superuser data.
- Login: admin
- Password: 12345

