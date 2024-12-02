# Конфигурационное управление

## Домашнее задание №2

**Вариант №29**

Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя.

Зависимости определяются по имени пакета платформы .NET (nupkg). Для описания графа зависимостей используется представление Mermaid. Визуализатор должен выводить результат в виде сообщения об успешном выполнении и сохранять граф в файле формата png.

Ключами командной строки задаются:
* Путь к программе для визуализации графов.
* Имя анализируемого пакета.
* Путь к файлу с изображением графа зависимостей.
* URL-адрес репозитория.

Все функции визуализатора зависимостей должны быть покрыты тестами.

## Зависимости
```
pip install -r requirements.txt
```

## Команда для запуска проекта
```
# Пример команды запуска для графа зависимостей Newtonsoft.Json

cd target_2
python visualizer.py --visualizer_path ./visualizer.py --package_name Newtonsoft.Json --output_png_path ./output/output_graph_1 --url https://www.nuget.org/api/v2/package/Newtonsoft.Json/13.0.3
```
## Команда для запуска юнит-тестов
```
cd target_2
python -m unittest ./tests/test_visualizer.py
```

## Результат юнит-тестов программы

![](https://github.com/FindTheRhythm/Homework-2-Configuration-management/blob/23cf9d79b694dc652a01a5a68ec613ce130b5f74/target_2/images/Screenshot%202024-12-02%20224423.png)

## Результат работы программы

![](https://github.com/FindTheRhythm/Homework-2-Configuration-management/blob/7d96a3a8611835da5c99ac4ff2f7624d73f9c3e7/target_2/output/output_graph_1.png)

