# loki
## Урок 3. Взламываем электронный дневник

Программа, предназначенныя для исправления плохих оценок в электронном дневнике. А так же удаление замечаний учителей и добавление хвалебных записей.

## Запуск

Для запуска программы требуется файл БД и развернутый сайт электронного днеевника.

- Развернуть у себя на комьютере сайт из [репозитория](https://github.com/devmanorg/e-diary)
- Скачать базу данных (в данном репозитории не предоставляется) и поместить в корневую папку электронного дневника на сервере рядом с файлом `manage.py`.
- Скачать и поместить файл `scripts.py` в корневую папку.
- Для исправления плохих оценок запустить скрипт командой:
```
python3 scripts.py mark -n [Фамилия Имя]
```
- Для удаления замечаний:
```
python3 scripts.py amnesty -n [Фамилия Имя]
```
- Для добавления записи с похвалой учителя необходимо указать предмет:
```
python3 scripts.py praise -n [Фамилия Имя] -s [Предмет]
```

## Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
