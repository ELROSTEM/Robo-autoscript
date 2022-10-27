import pyautogui

pyautogui.sleep(3)
x, y = pyautogui.locateCenterOnScreen('robotc_start.png', confidence=0.9)
pyautogui.moveTo(x, y)
print(x, y)
pyautogui.click()
