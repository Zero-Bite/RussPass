## Сайт на Django с интеграцией LLM для RussPass

## Описание проекта:
Этот проект представляет собой веб-приложение на Django, разработанное для повышения конверсии сервисов **RussPass** за счет интеграции **LLM-модели (GigaChat)**. Проект был создан в рамках хакатона **RussPass**, организованного Сбером, и стал финалистом (топ 7). Основная цель — улучшить пользовательский опыт, предоставляя персонализированные рекомендации по путешествиям и достопримечательностям городов России.

## Основные функции:
1. **Персонализированные рекомендации**:
   - Пользователь вводит название города, а система предоставляет информацию о популярных достопримечательностях, отелях и интересных фактах.
   - Поддерживаются города Золотого кольца России (Москва, Сергиев Посад, Переславль-Залесский, Ростов, Ярославль, Кострома, Иваново, Суздаль, Владимир), а также Санкт-Петербург и Камчатка.

2. **Интеграция с LLM (GigaChat)**:
   - Модель GigaChat используется для генерации текстовых ответов на запросы пользователей.
   - Ответы включают рекомендации по туристическим местам, отелям и ссылки на дополнительные ресурсы, такие как [Russpass](https://russpass.ru).

3. **Интерактивное взаимодействие**:
   - Пользователь может задавать вопросы и получать подробные ответы в реальном времени.
   - Система запоминает контекст разговора для более персонализированных рекомендаций.

4. **Простота использования**:
   - Удобный интерфейс с возможностью ввода текста и получения мгновенных ответов.

## Используемые технологии:
- **Django** — фреймворк для создания веб-приложения.
- **GigaChat API** — для генерации текстовых ответов с использованием LLM.
- **Requests** — для работы с HTTP-запросами к API GigaChat.
- **JSON** — для обработки данных.
- **HTML/CSS/JavaScript** — для создания пользовательского интерфейса.

## Как работает приложение:
1. **Запуск приложения**:
   - Пользователь заходит на сайт и видит интерфейс для ввода запроса.
   - Вводит название города или задает вопрос о путешествиях.

2. **Генерация ответа**:
   - Запрос отправляется на сервер, где обрабатывается с использованием LLM-модели GigaChat.
   - Система возвращает персонализированные рекомендации по достопримечательностям, отелям и интересным местам.

3. **Дополнительные вопросы**:
   - Пользователь может задавать уточняющие вопросы, например, о конкретных местах или мероприятиях.
   - Система предоставляет подробные ответы и ссылки на дополнительные ресурсы.

