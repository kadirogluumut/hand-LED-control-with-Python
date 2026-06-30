import argparse
import time

import cv2
import mediapipe as mp
import serial


FINGER_NAMES = ["Thumb", "Index", "Middle", "Ring", "Pinky"]


def get_finger_states(hand_landmarks, handedness_label):
    landmarks = hand_landmarks.landmark

    # Thumb logic depends on whether MediaPipe sees a left or right hand.
    if handedness_label == "Right":
        thumb_open = landmarks[4].x < landmarks[3].x
    else:
        thumb_open = landmarks[4].x > landmarks[3].x

    index_open = landmarks[8].y < landmarks[6].y
    middle_open = landmarks[12].y < landmarks[10].y
    ring_open = landmarks[16].y < landmarks[14].y
    pinky_open = landmarks[20].y < landmarks[18].y

    return [thumb_open, index_open, middle_open, ring_open, pinky_open]


def draw_status(frame, finger_states, serial_message, connected):
    status_color = (0, 220, 0) if connected else (0, 0, 255)
    status_text = "Arduino connected" if connected else "Arduino not connected"

    cv2.rectangle(frame, (10, 10), (430, 165), (20, 20, 20), -1)
    cv2.putText(frame, status_text, (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    cv2.putText(frame, f"Serial: {serial_message}", (25, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    for index, name in enumerate(FINGER_NAMES):
      state = "ON" if finger_states[index] else "OFF"
      color = (0, 255, 0) if finger_states[index] else (120, 120, 120)
      cv2.putText(frame, f"{name}: {state}", (25, 105 + index * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.62, color, 2)


def main():
    parser = argparse.ArgumentParser(description="Control 5 Arduino LEDs with hand detection.")
    parser.add_argument("--port", default="/dev/tty.usbmodem1101", help="Arduino serial port")
    parser.add_argument("--baud", type=int, default=9600, help="Serial baud rate")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    args = parser.parse_args()

    arduino = None
    try:
        arduino = serial.Serial(args.port, args.baud, timeout=1)
        time.sleep(2)
        print(f"Connected to Arduino on {args.port}")
    except serial.SerialException:
        print("Arduino connection failed. The camera demo will still run.")

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(args.camera)
    previous_message = ""

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            finger_states = [False, False, False, False, False]
            serial_message = "00000"

            if result.multi_hand_landmarks and result.multi_handedness:
                hand_landmarks = result.multi_hand_landmarks[0]
                handedness_label = result.multi_handedness[0].classification[0].label

                finger_states = get_finger_states(hand_landmarks, handedness_label)
                serial_message = "".join("1" if state else "0" for state in finger_states)

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if arduino and serial_message != previous_message:
                arduino.write((serial_message + "\n").encode("utf-8"))
                previous_message = serial_message

            draw_status(frame, finger_states, serial_message, arduino is not None)

            cv2.imshow("Hand Detection LED Control", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    if arduino:
        arduino.write(b"00000\n")
        arduino.close()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
