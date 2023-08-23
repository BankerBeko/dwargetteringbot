import tkinter as tk
import threading
import time
import pyautogui
from PIL import ImageGrab
import keyboard

running = False  # Döngü çalışma durumunu izlemek için bir değişken
previous_click_point = None  # Önceki tıklama noktasını saklamak için
target_image = "Kapat.png"

def is_close(point1, point2, tolerance=5):
    return abs(point1[0] - point2[0]) <= tolerance and abs(point1[1] - point2[1]) <= tolerance

def find_and_double_click_color_in_area(target_color, x_start, y_start, x_end, y_end, click_count=2):
    screen = ImageGrab.grab()  # Ekran görüntüsünü al

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            pixel_color = screen.getpixel((x, y))
            if pixel_color == target_color and (previous_click_point is None or not is_close(previous_click_point, (x, y))):
                pyautogui.click(x, y, clicks=click_count)
                return True  # Renk bulundu ve tıklama yapıldı

    return False  # Renk bulunamadı
def start_loop():
    global running, previous_click_point
    target_color = (183, 9, 6)  # deve dikeni
    #target_color = (236, 15, 125)  # yonca239, 37, 186
    restart_interval = 4

    start_time = time.time()

    while running:  # Döngüyü çalıştırma durumuna bağlı
        time.sleep(0.3)
        x_start, y_start, x_end, y_end = 1100, 147, 1900, 1000 #Hunt yarım ekran
        #x_start, y_start, x_end, y_end = 202, 139, 1722, 1019  #Hunt tam ekran

        found = find_and_double_click_color_in_area(target_color, x_start, y_start, x_end, y_end)

        if found:
            previous_click_point = pyautogui.position()  # Tıklama noktasını kaydet
            log_text.insert(tk.END, "Hedeflenen renk bulundu ve çift tıklama yapıldı.\n")
            time.sleep(20)
            
        else:
            log_text.insert(tk.END, "Hedeflenen renk bulunamadı. Yeniden başlatılıyor.\n")

            if time.time() - start_time > restart_interval:
                log_text.insert(tk.END, f"Döngü {restart_interval} saniye boyunca yeniden başlatılmadı. Yeniden başlatılıyor.\n")
                keyboard.press("F5")
                keyboard.release("F5")
                start_loop()
                start_time = time.time()

        log_text.see(tk.END)  # Text widget'ını en altta tut



    log_text.insert(tk.END, "Döngü durduruldu.\n")
    start_button.config(state=tk.NORMAL)  # Başlatma tuşunu tekrar etkinleştir
    stop_button.config(state=tk.DISABLED)  # Durdurma tuşunu devre dışı bırak

def start_button_clicked():
    global running, log_text
    running = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    threading.Thread(target=start_loop).start()

def stop_button_clicked():
    global running
    running = False

app = tk.Tk()
app.title("Renk Algılama ve Tıklama")
app.geometry("400x700")

log_text = tk.Text(app, wrap=tk.WORD)
log_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

start_button = tk.Button(app, text="Döngüyü Başlat", command=start_button_clicked)
start_button.pack(pady=10)

stop_button = tk.Button(app, text="Döngüyü Durdur", command=stop_button_clicked, state=tk.DISABLED)
stop_button.pack()

app.mainloop()