import cv2
import os
import time
from ffpyplayer.player import MediaPlayer
from colorama import init

init()

CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def convert_frame(frame, width=100):
    h, w, _ = frame.shape
    new_height = int((h / w) * width * 0.44)
    img = cv2.resize(frame, (width, new_height))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    output = ""
    for y in range(new_height):
        for x in range(width):
            b, g, r = img[y, x]
            brightness = img_gray[y, x]
            char = CHARS[brightness * (len(CHARS) - 1) // 255]
            output += f"\033[38;2;{r};{g};{b}m{char}"
        output += "\033[0m\n"
    return output

file_path = "video.mp4"
cap = cv2.VideoCapture(file_path)
player = MediaPlayer(file_path)


print("\033[?25l", end="")
os.system('cls' if os.name == 'nt' else 'clear')

start_time = time.time()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

       
        audio_time = player.get_pts()
        
        
        video_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        
       
        if video_time < audio_time:
            continue
            
      
        while video_time > player.get_pts() + 0.01:
            time.sleep(0.001)

        print("\033[H", end="")
      
        print(convert_frame(frame, width=100), end="")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    cap.release()
    player.close_player()
    print("\033[0m\033[?25h")