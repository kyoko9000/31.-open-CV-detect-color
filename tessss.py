import time
import cv2
import pyautogui as pyautogui
import win32gui
import numpy as np
import torch

def get_screeshot():
    # hwnd = win32gui.FindWindow(None, 'Albion Online Client')
    # window_rect = win32gui.GetWindowRect(hwnd)
    # print(window_rect)

    screenshot = pyautogui.screenshot()  # region=(window_rect)
    # or: screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    # screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
model.classes = 0, 3
# model.conf = 0.25  # NMS confidence threshold
# model.iou = 0.45  # NMS IoU threshold
# model.multi_label = False  # NMS multiple labels per box
model = model.autoshape()

def run():
    while(True):
        time.sleep(0.5)
        print("frame")
        screenshot = get_screeshot()
        result = model(screenshot)
        result.show()

        results = result.pandas().xyxy[0].to_dict(orient="records")
        x = np.array(results)
        # print(x)

        # filter
        for result in results:
            x1 = int(result['xmin'])
            y1 = int(result['ymin'])
            x2 = int(result['xmax'])
            y2 = int(result['ymax'])
            # print(x1, y1, x2, y2)

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
run()