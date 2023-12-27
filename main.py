from tkinter import ttk
import cv2
import mediapipe as mp
from tkinter import *
import handTracker as hT

def openCamera():

    if selected_camera_index is not None:
        print("Камера вмикається !")
        pass
    else:
        print("Камера не обрана!!!")
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_SETTINGS, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    tracker = hT.handTracker()

    while True:
        success, image = cap.read()
        image = tracker.handsFinder(image)
        #lmList = tracker.positionFinder(image)
        #if len(lmList) != 0:
            #print(lmList[4])

        cv2.imshow("Video", image)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def get_connected_cameras():
    # Получаем список всех доступных камер
    connected_cameras = []
    for i in range(10):  # Попробуем первые 10 камер (можно изменить диапазон по необходимости)
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            connected_cameras.append(f"Camera {i}")
            cap.release()
    return connected_cameras

def on_combobox_change(event, combobox, label_result):
    global selected_camera_index
    selected_camera_index = combobox.get()[1]  # Получаем индекс из кортежа (название, индекс)
    selected_value = combobox.get()
    label_result.config(text=f'Обрана камера: {selected_value}')

def createWindow():
    win = Tk()
    win.title("Аналізатор")
    win.geometry("400x300")
    win.resizable(width=False, height=False)

    button = Button(win, text="Ввімкнути камеру", font=40, command=openCamera)
    button.pack(side=BOTTOM, pady=40)

    label = Label(win, text="Виберіть камеру:")
    label.pack(pady=10)

    connected_cameras = get_connected_cameras()

    global  combobox
    combobox = ttk.Combobox(win, values=connected_cameras)
    combobox.pack(pady=10)
    if connected_cameras:
        combobox.set("Не обрана")
    else:
        combobox.set("Камери не виявлено")

    combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_change(event, combobox, label_result))

    # Создание метки для вывода выбранного значения
    label_result = Label(win, text="Обрана камера: ")
    label_result.pack(pady=10)

    return win

def main():
    win = createWindow()
    win.mainloop()






if __name__ == "__main__":
    main()