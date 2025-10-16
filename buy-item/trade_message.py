template = "WTBuy any T15-16 Waystone. Paying 1 exalt for every waystone."
tradeChannel = '/trade '

import pyautogui
pyautogui.PAUSE = 0.43
msg = input("Message: ")
if (msg == 'a'): msg = template
i = int(input('Starting trade channel: '))
msgCounter = 0

# focus the game
pyautogui.click(1800, 1000)

while i < 256:
  msgCounter += 1
  if msgCounter % 3 == 0:
    pyautogui.countdown(1)
    
  pyautogui.press('enter')
  pyautogui.typewrite(tradeChannel + str(i))
  pyautogui.press('enter')
  pyautogui.press('enter')
  pyautogui.typewrite("$" + msg)
  pyautogui.press('enter')
  i += 1