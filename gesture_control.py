import cv2
import mediapipe as mp
import pyautogui
import time
import webbrowser

# -------------------------
# OPEN SUBWAY SURFERS LINK
# -------------------------
game_url = "https://poki.com/en/g/subway-surfers"

webbrowser.open(game_url)

print("Opening Subway Surfers...")
time.sleep(8)   # Wait for game to load

# -------------------------
# MEDIAPIPE SETUP
# -------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = 0
prev_y = 0
cooldown = 0

print("Gesture control started!")

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    h, w, c = img.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = int(hand_landmarks.landmark[8].x * w)
            y = int(hand_landmarks.landmark[8].y * h)

            cv2.circle(img, (x, y), 10, (255, 0, 255), cv2.FILLED)

            if cooldown == 0:

                if x - prev_x > 40:
                    pyautogui.press("right")
                    print("RIGHT")
                    cooldown = 10

                elif prev_x - x > 40:
                    pyautogui.press("left")
                    print("LEFT")
                    cooldown = 10

                elif prev_y - y > 40:
                    pyautogui.press("up")
                    print("JUMP")
                    cooldown = 10

                elif y - prev_y > 40:
                    pyautogui.press("down")
                    print("DOWN")
                    cooldown = 10

            prev_x = x
            prev_y = y

    if cooldown > 0:
        cooldown -= 1

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
