from src.letter_rules import (
    check_A,
    check_B,
    check_C,
    check_D,
    check_E,
    check_F,
    check_G,
    check_H,
    check_I,
    check_J,
    check_K,
    check_L,
    check_M,
    check_N,
    check_O,
)

def detect_possible_issue(hand_landmarks, prediction):

    lm = hand_landmarks.landmark

    wrist = lm[0]
    index_mcp = lm[5]
    pinky_tip = lm[20]

    # ------------------------
    # Global Rules
    # ------------------------

    if wrist.y > 0.90:
        return "Raise your hand slightly."

    if wrist.y < 0.10:
        return "Lower your hand slightly."

    palm_width = abs(index_mcp.x - pinky_tip.x)

    if palm_width < 0.08:
        return "Keep your palm facing the camera."

    # ------------------------
    # Letter-specific Rules
    # ------------------------

    RULES = {
    "A": check_A,
    "B": check_B,
    "C": check_C,
    "D": check_D,
    "E": check_E,
    "F": check_F,
    "G": check_G,
    "H": check_H,
    "I": check_I,
    "J": check_J,
    "J": check_J,
    "K": check_K,
    "L": check_L,
    "M": check_M,
    "N": check_N,
    "O": check_O,
}

    if prediction in RULES:
        return RULES[prediction](lm)

    return "No major issue detected."