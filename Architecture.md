# Часть 1
## Тип приложения
Для всех устройств, имеющих доступ к сети Интернет.
## Стратегия развертывания
Распределённая с сохранением состояния (сообщения и данные пользователей хранятся в базе данных).
## Обоснование выбора технологий
Приложение разрабатывается в среде разработки Visual Studio Code на языке программирования Python 3.7, т.к. он содержит все необходимые инструменты для разработки приложения данного типа.
## Показатели качества
##### •	Простота
Бот должен выполнять только основные возложенные на него задачи.
##### •	Отстутствие собственного графического интерфейса
Должно значительно сократить потребление производительности в сравнении с использованием сторонних приложений.
##### •	Время
Бот должна экономить значительное количество времени пользователя при решении задач внутри мессенджера.
##### •	Кроссплатформенность
Бот будет взаимодействовать с пользователем на любом его устройстве.
##### •	Надёжность и скорость доставки сообщений
Должны работать в обе стороны взаимодейтсвия, благодаря использованию Telegram.
## Пути реализации сквозной функциональности
* Авторизация: при первом взаимодействии бот запрашивает для авторизации все необходимые данные.
* Аутентификация: осуществляется с помощью технологий Telegram для аутентификации пользователя.
* Кэширование: сообщения и данные пользователей хранятся в базе данных.

# Часть 2
## Анализ архитектуры разрабатываемого приложения
Тип архитектуры приложения: сервер. Логика приложения представлена обработкой запросов и сообщений от пользователя.
## Обобщенное представление архитектуры
![Image alt](https://github.com/Andrey-Zelinskiy/X-Man-project/blob/master/%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0.png)
## Диаграмма развёртывания
![Image alt](https://github.com/Andrey-Zelinskiy/X-Man-project/blob/master/deployment_diagram.png)
## Архитектура "As is"
### Диаграмма компонентов
![Image alt](https://github.com/Andrey-Zelinskiy/X-Man-project/blob/master/Software%20Component%20Diagram.png)
## Архитектура "To be"
### Диаграмма компонентов
![Image alt](https://github.com/Andrey-Zelinskiy/X-Man-project/blob/master/Software%20Component%20Diagram%20(1).png)
# Часть 3
 Модель AS-IS - это модель «как есть», т.е. модель уже существующего процесса/функции. 
 
 Найденные в модели AS-IS недостатки можно исправить при создании модели ТО-ВЕ, которая нужна для оценки последствий внедрения информационной системы и анализа альтернативных путей выполнения работы и документирования того, как система будет функционировать в будущем.
 
Для реализации лучшей функциональности приложения необходимо улучшить интерфейсы взаимодействия Python-модулей между собой и расширить базу данных ответов путём обучения диалогам. Это обеспечит более качественное взаимодействие с пользователем в диалоге и быстроту выполнения сопутствующих функциональностей.

В связи с вышеперичисленными причинами мы будем улучшать архитектуру согласно следующим принципам:
* Принцип DRY(Don't Repeat Yourself) - не повторяйся.
* Принцип минимального знания (минимальной информированности) - чем меньше происходит взаимодействие объектов, тем гибче система.
* Принцип IOC(Inversion of Control) - высокоуровневые компоненты не должны зависеть от низкоуровневых, те и другие должны зависеть от абстракции.
