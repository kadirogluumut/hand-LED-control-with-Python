# Hand Detection 5 LED Arduino Project

This project controls 5 LEDs using hand detection with Python, MediaPipe, OpenCV, and Arduino.  
Each finger controls one LED. When a finger is open, its LED turns on. When the finger is closed, its LED turns off.

## Demo Idea

Show your hand to the camera and open or close your fingers one by one.  
Python detects the finger states and sends a 5-digit command to Arduino.

Example:

```text
10110
```

This means:

| Finger | Value | LED State |
|---|---:|---|
| Thumb | 1 | ON |
| Index | 0 | OFF |
| Middle | 1 | ON |
| Ring | 1 | ON |
| Pinky | 0 | OFF |

## Circuit Diagram

![Hand Detection 5 LED Arduino Diagram](assets/hand_detection_5_led_diagram.svg)

## Animated Demo

![Hand Detection 5 LED Demo](assets/hand_detection_demo.gif)

## Required Components

| Component | Quantity |
|---|---:|
| Arduino Uno or Arduino Nano | 1 |
| LEDs | 5 |
| 220 ohm resistors | 5 |
| Breadboard | 1 |
| Jumper wires | As needed |
| USB cable | 1 |
| Computer with camera | 1 |

## Software Requirements

- Python 3
- Arduino IDE
- OpenCV
- MediaPipe
- PySerial

Install the Python libraries:

```bash
pip install -r requirements.txt
```

## Finger to LED Mapping

| Finger | Arduino Pin |
|---|---|
| Thumb | D2 |
| Index | D3 |
| Middle | D4 |
| Ring | D5 |
| Pinky | D6 |

## LED Wiring

Each LED should be connected with a 220 ohm resistor.

```text
Arduino digital pin -> LED long leg (+)
LED short leg (-) -> 220 ohm resistor -> GND
```

## Arduino Code

Upload this file to your Arduino:

```text
arduino/hand_led_controller/hand_led_controller.ino
```

The Arduino receives a 5-digit message from Python:

```text
1 = LED ON
0 = LED OFF
```

## Python Code

Run this file on your computer:

```text
python/hand_led_control.py
```

Example command:

```bash
python python/hand_led_control.py --port /dev/tty.usbmodem1101
```

On Windows, the port may look like this:

```bash
python python/hand_led_control.py --port COM3
```

## How to Run

1. Connect the 5 LEDs to Arduino pins D2, D3, D4, D5, and D6.
2. Upload the Arduino code.
3. Install the Python requirements.
4. Connect the Arduino to the computer with USB.
5. Run the Python script.
6. Show your hand to the camera.
7. Open and close your fingers to control the LEDs.

## Troubleshooting

| Problem | Solution |
|---|---|
| Arduino does not connect | Check the serial port name. |
| Camera does not open | Try another camera index, such as `--camera 1`. |
| LEDs work in the wrong order | Check the LED wiring and pin mapping. |
| Thumb detection is reversed | Try using the other hand or adjust the thumb logic in Python. |
| LEDs flicker | Use better lighting and keep your hand clearly visible. |

## Project Explanation

MediaPipe tracks hand landmarks from the camera image.  
The Python code checks whether each finger is open or closed.  
Then Python sends a serial message to Arduino.  
Arduino reads the message and controls the LEDs.

This project is a simple example of computer vision controlling real electronic hardware.

## License

This project is free to use for learning and educational purposes.
