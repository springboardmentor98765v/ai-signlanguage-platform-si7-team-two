class ScoreManager:

    def __init__(self):

        self.correct = 0
        self.total = 0

    def update(self, is_correct):

        self.total += 1

        if is_correct:
            self.correct += 1

    def get_score(self):

        return self.correct, self.total

    def get_accuracy(self):

        if self.total == 0:
            return 0.0

        return (self.correct / self.total) * 100

    def reset(self):

        self.correct = 0
        self.total = 0