import cv2

from services.recognizer import SignLanguageRecognizer

recognizer = SignLanguageRecognizer()

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = recognizer.predict(rgb)

    if result:

        print(result["prediction"], result["confidence"])

    cv2.imshow("Test", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()