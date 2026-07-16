import math


# ==========================================================
# Utility Functions
# ==========================================================

def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )
def palm_width(lm):
    """
    Distance between index MCP and pinky MCP.
    Used for normalization.
    """
    return distance(lm[5], lm[17])
def normalized_distance(p1, p2, lm):
    """
    Distance normalized by palm width.
    """
    pw = palm_width(lm)

    if pw == 0:
        return 0

    return distance(p1, p2) / pw
def fingers_are_close(index_tip, middle_tip, lm):

    ratio = normalized_distance(
        index_tip,
        middle_tip,
        lm
    )

    return ratio < 0.20


def fingers_are_wide(index_tip, middle_tip, lm):

    ratio = normalized_distance(
        index_tip,
        middle_tip,
        lm
    )

    return ratio > 0.70

def thumb_extended(thumb_tip, index_mcp, lm):

    ratio = normalized_distance(
        thumb_tip,
        index_mcp,
        lm
    )

    return ratio > 1.3

# ==========================================================
# Letter Rules
# ==========================================================

def check_A(lm):

    thumb_tip = lm[4]
    index_tip = lm[8]
    index_mcp = lm[5]
    middle_mcp = lm[9]

    if thumb_extended(thumb_tip, index_mcp):
        return "Fold your thumb outside the fist."

    if index_tip.y < middle_mcp.y:
        return "Fold your fingers to form a fist."

    return "Good 'A' hand shape."


def check_B(lm):

    thumb_tip = lm[4]
    index_tip = lm[8]
    middle_tip = lm[12]
    index_mcp = lm[5]

    if fingers_are_wide(index_tip, middle_tip):
        return "Keep your fingers together."

    if thumb_extended(thumb_tip, index_mcp):
        return "Fold your thumb across the palm."

    return "Good 'B' hand shape."


def check_C(lm):

    thumb_tip = lm[4]
    index_tip = lm[8]

    if distance(index_tip, thumb_tip) > 0.45:
        return "Curve your fingers more to form a 'C'."

    return "Good 'C' hand shape."


def check_D(lm):

    index_tip = lm[8]
    middle_tip = lm[12]

    if index_tip.y > middle_tip.y:
        return "Raise your index finger."

    return "Good 'D' hand shape."


def check_E(lm):

    thumb_tip = lm[4]
    index_mcp = lm[5]

    if thumb_extended(thumb_tip, index_mcp):
        return "Bring your thumb closer to your palm."

    return "Good 'E' hand shape."
# ==========================================================
# Letter F
# ==========================================================

def check_F(lm):

    return (
        "Touch your thumb to your index finger while "
        "keeping the middle, ring, and little fingers straight."
    )


# ==========================================================
# Letter G
# ==========================================================

def check_G(lm):

    return (
        "Keep your index finger and thumb extended "
        "parallel to each other."
    )


# ==========================================================
# Letter H
# ==========================================================

def check_H(lm):

    return (
        "Extend your index and middle fingers together "
        "while folding the remaining fingers."
    )


# ==========================================================
# Letter I
# ==========================================================

def check_I(lm):

    return (
        "Raise your little finger and keep "
        "the remaining fingers folded."
    )


# ==========================================================
# Letter J
# ==========================================================

def check_J(lm):

    return (
        "Start with the 'I' handshape and draw "
        "a small 'J' movement."
    )
# ==========================================================
# Letter K
# ==========================================================

def check_K(lm):

    return (
        "Keep your index and middle fingers raised in a 'V' shape "
        "with your thumb between them."
    )


# ==========================================================
# Letter L
# ==========================================================

def check_L(lm):

    return (
        "Extend your thumb and index finger to form an 'L' "
        "while folding the remaining fingers."
    )


# ==========================================================
# Letter M
# ==========================================================

def check_M(lm):

    return (
        "Tuck your thumb underneath your index, middle, "
        "and ring fingers."
    )


# ==========================================================
# Letter N
# ==========================================================

def check_N(lm):

    return (
        "Keep your thumb underneath your index and middle fingers "
        "while folding the remaining fingers."
    )


# ==========================================================
# Letter O
# ==========================================================

def check_O(lm):

    return (
        "Curve all your fingers and thumb together "
        "to form a rounded 'O' shape."
    )