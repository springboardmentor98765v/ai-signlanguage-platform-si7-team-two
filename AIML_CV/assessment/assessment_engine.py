from assessment.question_generator import get_random_letter

from assessment.score_manager import ScoreManager
from assessment.question_generator import get_random_letter


class AssessmentEngine:

    def __init__(self):

        self.current_letter = get_random_letter()

    def next_question(self):

        self.current_letter = get_random_letter()

        return self.current_letter

    def evaluate(self, prediction):

        return prediction == self.current_letter
if __name__ == "__main__":

    engine = AssessmentEngine()

    print("Target Letter:", engine.current_letter)

    prediction = input("Enter Prediction: ")

    result = engine.evaluate(prediction)

    if result:
        print("Correct")
    else:
        print("Incorrect")

    print(engine.score_manager.get_score())

    print(engine.score_manager.accuracy())