import smtplib
import os

login = os.environ["LOGIN"]
password = os.environ["PASSWORD"]
sender = os.environ["SENDER"]
receiver = os.environ["RECEIVER"]
subject = 'Приглашение на курс'
content_type = 'text/plain; charset="UTF-8";'
friend_name = 'Joseph'
my_name = 'Alex'
website = 'https://dvmn.org/referrals/FoqtjaNyhQToWO38Un8mT8Ve9rbjzwvENJnbomTy/'

replace = {
    '%friend_name%': friend_name,
    '%my_name%': my_name,
    '%website%': website
}

letter = """From: {0}
To: {1}
Subject: {2}
Content-Type: {3}

Привет, %friend_name%! %my_name% приглашает тебя на сайт %website%!

%website% — это новая версия онлайн-курса по программированию. 
Изучаем Python и не только. Решаем задачи. Получаем ревью от преподавателя. 

Как будет проходить ваше обучение на %website%? 

→ Попрактикуешься на реальных кейсах. 
Задачи от тимлидов со стажем от 10 лет в программировании.
→ Будешь учиться без стресса и бессонных ночей. 
Задачи не «сгорят» и не уйдут к другому. Занимайся в удобное время и ровно столько, сколько можешь.
→ Подготовишь крепкое резюме.
Все проекты — они же решение наших задачек — можно разместить на твоём GitHub. Работодатели такое оценят. 

Регистрируйся → %website%  
На курсы, которые еще не вышли, можно подписаться и получить уведомление о релизе сразу на имейл.""".format(
    sender, receiver, subject, content_type)

for old, new in replace.items():
  letter = letter.replace(old, new)

letter = letter.encode("UTF-8")

server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
server.login(login, password)
server.sendmail(sender, receiver, letter)
server.quit()
