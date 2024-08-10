import urwid


def has_digit(password):
  return any(letter.isdigit() for letter in password)


def has_letters(password):
  return any(letter.isalpha() for letter in password)


def has_upper_letters(password):
  return any(letter.isupper() for letter in password)


def has_lower_letters(password):
  return any(letter.islower() for letter in password)


def has_symbols(password):
  return any(not c.isdigit() and not c.isalpha() for c in password)


def is_very_long(password):
  return len(password) > 12


def rate_password(input, score):
  return score + 2 if input else score


def main():
  functions_list = [
      has_digit, 
      has_letters, 
      has_upper_letters, 
      has_lower_letters,
      has_symbols, 
      is_very_long
  ]

  def on_ask_change(edit, new_edit_text):
    score = 0
    for function in functions_list:
      score = rate_password(function(new_edit_text), score)
    reply.set_text("Рейтинг пароля: %s" % score)

  ask = urwid.Edit('Введите пароль: ', mask='*')
  reply = urwid.Text("")
  menu = urwid.Pile([ask, reply])
  menu = urwid.Filler(menu, valign='top')
  urwid.connect_signal(ask, 'change', on_ask_change)
  urwid.MainLoop(menu).run()


if __name__ == '__main__':
  main()
