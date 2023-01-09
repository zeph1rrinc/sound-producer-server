# SoundProducerClient

## Установка и запуск

- Скачать исходник как zip-архив и распаковать в любую удобную папку

![скрин](https://i.imgur.com/SCE4sLO.png)

- В любом удобном терминале(pycharm, cmd) перейти в папку с проектом
- Создать виртуальное окружение
```
python -m venv venv
```
- Активировать виртуальное окружение
```
venv\Scripts\activate
```
- Установить все зависимости в виртуальное окружение
```
python -m pip install -r requirements.txt
```
- Запустить код
```
python .\src\main.py
```

## Добавить диктора

- Создать папку input
- Положить в папку input json файл
- Выполнить команду
```
python main.py input\vera.json
```