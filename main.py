import os

from pytimeparse import parse

import ptbot

TG_TOKEN = os.environ["TG_TOKEN"]
TG_CHAT_ID = os.environ["TG_CHAT_ID"]


def handle_message(chat_id, message):
    delay = parse(message)

    if delay is None:
        warning = (
            "Пожалуйста, введите корректное количество времени (например, '5s', '2m')"
        )
        bot.send_message(chat_id, warning)
        return

    message_id = bot.send_message(chat_id, f"Осталось: {delay} секунд")
    bot.create_countdown(
        delay, notify_progress, chat_id=chat_id, message_id=message_id, delay=delay
    )


def notify_progress(secs_left, chat_id, message_id, delay):
    iteration = delay - secs_left
    progress_bar = render_progressbar(delay, iteration)
    bot.update_message(
        chat_id, message_id, f"Осталось: {secs_left} секунд\n{progress_bar}"
    )
    if secs_left == 0:
        send_delayed_message(chat_id, "Время вышло!")


def send_delayed_message(chat_id, message):
    bot.send_message(chat_id, message)


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def main():
    global bot
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(handle_message)
    bot.run_bot()


if __name__ == "__main__":
    main()
