from services.recognizer import SignLanguageRecognizer

recognizer = SignLanguageRecognizer()


def predict_frame(rgb_frame):

    return recognizer.predict(rgb_frame)