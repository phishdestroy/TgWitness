# Установка TgWitness для экспорта чатов Telegram

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/start/

Сначала осмотритесь в демо, потом подключите свой аккаунт.

## Ознакомьтесь с сайтом без регистрации

Скачайте проект, поставьте **Python 3.11 или новее** и запустите демо. Остальное лаунчер сделает сам.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

В браузере откроется пространство с выдуманными сообщениями. Откройте чат, сравните правку, загляните в экспорт. Telegram не участвует.

![Вид диалога в TgWitness с примерами сообщений](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Пример рабочей области. Ваш собственный журнал создаётся отдельно.

## Создайте собственное рабочее пространство

Закройте демо, затем:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Откройте адрес, который покажет лаунчер, и вставьте **токен доступа к панели** из указанного файла. Это токен для TgWitness, а не для Telegram.

## Сохраните своё первое сообщение

1. [Подключите специальный аккаунт в Telegram.](https://phishdestroy.github.io/TgWitness/ru/docs/accounts/)
2. Выберите группу или канал и запустите наблюдение.
3. Отправьте сообщение в тестовую группу и посмотрите, как оно появится в журнале.

Для установки на сервере следуйте инструкциям в разделе [«Обеспечение непрерывной работы](https://phishdestroy.github.io/TgWitness/ru/docs/server/)».
