import cv2
import numpy as np
import tensorflow as tf
import serial
import time

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Label list
labels = ["Paper", "Rock", "Scissors","Normal"]

# Connect to Arduino
arduino = serial.Serial('COM7', 9600)  # Change COM port if needed
time.sleep(2)
print("Connected to Arduino.")

# Start camera
cap = cv2.VideoCapture(0)

while True:
    print("Loop running...")
    ret, frame = cap.read()
    if not ret:
        continue

    # Rotate the frame 180 degrees
    frame = cv2.flip(frame, 1)

    # Preprocess the frame
    img = cv2.resize(frame, (224, 224))  # Ensure this matches model input
    img = np.asarray(img, dtype=np.float32)
    img = (img / 127.5) - 1  # Normalize to [-1, 1]
    img = np.expand_dims(img, axis=0)

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], img)

    # Run inference
    interpreter.invoke()

    # Get output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    predicted_index = np.argmax(output_data)
    gesture = labels[predicted_index]

    # Show prediction on frame
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Gesture Recognition", frame)

    # Send to Arduino
    arduino.write((gesture + "\n").encode())
    time.sleep(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
