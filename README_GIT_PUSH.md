# Инструкция: как отправить проект в Git (коротко)

1) Подготовка
- Убедитесь, что в корне проекта есть `.gitignore` и не добавляйте в репозиторий: `venv/`, `__pycache__/`, `db.sqlite3`, `.env`, `*.pyc`.
- Создайте (если нужно): `git init` или клонируйте существующий репозиторий `git clone <url>`.

2) Порядок действий (новый проект)
- git add .
- git commit -m "Initial commit"
- git branch -M main
- git remote add origin <git-remote-url>
- git push -u origin main

3) Рабочий процесс (ежедневно)
- git checkout -b feature/short-description
- Работаете и коммитите: `git add <files>` && `git commit -m "Kраткое сообщение"`
- Когда закончено: `git push origin feature/short-description` и создаёте Pull Request (или Merge Request) в GitHub/GitLab.

4) Хорошие практики
- Пишите понятные сообщения коммитов и создавайте маленькие PR.
- Не храните секреты в репозитории (API ключи, пароли). Используйте `.env` и CI secrets.
- Если добавлены зависимости, обновите `requirements.txt`: `pip freeze > requirements.txt` (а затем коммит).

5) Пример: быстрое добавление изменений
- git add .
- git commit -m "Добавлен экспорт XLSX для установок и делегированный JS для AJAX-форм"
- git push origin feature/export-install

6) Удаленный доступ
- HTTPS: `git remote add origin https://github.com/username/repo.git`
- SSH: `git remote add origin git@github.com:username/repo.git`

Если нужно — могу сгенерировать готовый `.gitignore` и проверить/добавить `requirements.txt` в репозиторий (включая `openpyxl`).