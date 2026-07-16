import math


def distance(p1, p2):
    """
    Euclidean distance between two MediaPipe landmarks.
    """
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


def detect_possible_issue(hand_landmarks):
    """
    Returns a simple rule-based feedback message.

    Input:
        hand_landmarks -> MediaPipe HandLandmark object

    Output:
        String
    """

    lm = hand_landmarks.landmark

    # -----------------------------
    # Landmark indices
    # -----------------------------

    wrist = lm[0]

    thumb_tip = lm[4]

    index_tip = lm[8]

    middle_tip = lm[12]

    ring_tip = lm[16]

    pinky_tip = lm[20]

    index_mcp = lm[5]

    middle_mcp = lm[9]

    # ---------------------------------------
    # Rule 1
    # Hand too low
    # ---------------------------------------

    if wrist.y > 0.90:
        return "Raise your hand slightly."

    # ---------------------------------------
    # Rule 2
    # Hand too high
    # ---------------------------------------

    if wrist.y < 0.10:
        return "Lower your hand slightly."

    # ---------------------------------------
    # Rule 3
    # Fingers too close
    # ---------------------------------------

    spread = distance(index_tip, middle_tip)

    if spread < 0.03:
        return "Spread your fingers slightly."

    # ---------------------------------------
    # Rule 4
    # Fingers too wide
    # ---------------------------------------

    if spread > 0.18:
        return "Keep your fingers closer together."

    # ---------------------------------------
    # Rule 5
    # Thumb too far away
    # ---------------------------------------

    thumb_distance = distance(
        thumb_tip,
        index_mcp
    )

    if thumb_distance > 0.35:
        return "Fold your thumb inward."

    # ---------------------------------------
    # Rule 6
    # Palm rotated
    # ---------------------------------------

    palm_width = abs(
        index_mcp.x -
        pinky_tip.x
    )

    if palm_width < 0.08:
        return "Keep your palm facing the camera."

    # ---------------------------------------
    # Rule 7
    # Fingers bent too much
    # ---------------------------------------

    if (
        index_tip.y > middle_mcp.y and
        middle_tip.y > middle_mcp.y
    ):
        return "Extend your fingers."

    return "No major issue detected."