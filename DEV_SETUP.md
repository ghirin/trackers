Краткая инструкция для разработчика (локально)

1) Установка зависимостей
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

2) Применение миграций
- python manage.py migrate

3) Создать суперпользователя (если нужно)
- python manage.py createsuperuser

4) Запуск локального сервера
- python manage.py runserver

5) Экспорт установок
- Войти в приложение → Отчёты → применить фильтры (при необходимости) → нажать кнопку "Экспорт XLSX"

6) Обновление списка локаций
- Список локаций представлен в модели Car.LOCATION_CHOICES. Чтобы добавить новую локацию:
  - Добавьте её в `LOCATION_CHOICES` в `tracker/models.py`.
  - Если хотите нормализовать существующие значения, создайте миграцию RunPython или вручную обновите данные.

7) Команды полезные
- git status / git add / git commit / git push
- pip freeze > requirements.txt

Если нужно — могу создать management command для быстрого seed'а локаций или интерфейс для редактирования списка локаций (как отдельную модель).