# Telegram · Почніть за лічені хвилини

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/start/

Спершу роздивіться демо, потім підключіть свій акаунт.

## Ознайомтеся з сайтом без реєстрації

Завантажте проєкт, встановіть **Python 3.11 або новіший** і запустіть демо. Решту лаунчер зробить сам.

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

У браузері відкриється простір з вигаданими повідомленнями. Відкрийте чат, порівняйте правку, загляньте в експорт. Telegram не задіяний.

![Вигляд діалогу в TgWitness із прикладами повідомлень](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Приклад робочого простору. Ваш власний журнал створюється окремо.

## Створіть власний робочий простір

Закрийте демо, потім:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Відкрийте адресу, яку покаже лаунчер, і вставте **токен доступу до панелі** з указаного файлу. Це токен для TgWitness, а не для Telegram.

## Збережіть своє перше повідомлення

1. [Підключіть спеціальний обліковий запис Telegram.](https://phishdestroy.github.io/TgWitness/uk/docs/accounts/)
2. Оберіть групу чи канал і запустіть спостереження.
3. Надішліть повідомлення в тестову групу й подивіться, як воно з'явиться в журналі.

Для встановлення на сервер дотримуйтесь інструкцій у розділі [«Keep it running](https://phishdestroy.github.io/TgWitness/uk/docs/server/)».
