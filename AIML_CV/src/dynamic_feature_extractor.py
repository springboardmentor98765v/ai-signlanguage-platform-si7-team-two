import numpy as np


# ============================================================
# FEATURE CONFIGURATION
#
# Total = 285
# Raw landmarks = 218
# Angles = 41
# Distances = 26
# ============================================================


def _landmark_values(landmarks, count, values_per_landmark):
    """
    Extract landmark coordinates.

    Missing landmarks are represented with zeros.
    """

    features = []

    if landmarks is None:
        return [0.0] * (count * values_per_landmark)

    for i in range(count):
        if i < len(landmarks.landmark):
            lm = landmarks.landmark[i]

            if values_per_landmark == 4:
                visibility = getattr(lm, "visibility", 1.0)

                features.extend([
                    lm.x,
                    lm.y,
                    lm.z,
                    visibility
                ])

            else:
                features.extend([
                    lm.x,
                    lm.y,
                    lm.z
                ])

        else:
            features.extend([0.0] * values_per_landmark)

    return features


def _point_from_landmarks(landmarks, index):
    """
    Return x, y, z for a landmark.
    """

    if landmarks is None:
        return None

    if index >= len(landmarks.landmark):
        return None

    lm = landmarks.landmark[index]

    return np.array(
        [lm.x, lm.y, lm.z],
        dtype=np.float32
    )


def _calculate_angle(a, b, c):
    """
    Calculate normalized cosine angle between:
    A -> B and C -> B.

    Output range approximately [-1, 1].
    """

    if a is None or b is None or c is None:
        return 0.0

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba < 1e-6 or norm_bc < 1e-6:
        return 0.0

    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)

    return float(
        np.clip(cosine, -1.0, 1.0)
    )


def _calculate_distance(a, b):
    """
    Euclidean distance.
    """

    if a is None or b is None:
        return 0.0

    return float(np.linalg.norm(a - b))


# ============================================================
# SELECTED RAW LANDMARKS
#
# Pose:
# 29 landmarks × 4 = 116
#
# Left Hand:
# 17 landmarks × 3 = 51
#
# Right Hand:
# 17 landmarks × 3 = 51
#
# TOTAL:
# 116 + 51 + 51 = 218
# ============================================================


POSE_INDICES = [
    0, 1, 2, 3, 4,
    5, 6, 7, 8, 9,
    10,
    11, 12,
    13, 14,
    15, 16,
    17, 18,
    19, 20, 21, 22,
    23, 24,
    25, 26,
    27, 28
]

HAND_INDICES = [
    0, 1, 2, 3,
    4, 5, 6, 7,
    8, 9, 10, 11,
    12, 13, 14,
    15, 16
]


# ============================================================
# ANGLE CONFIGURATION
# ============================================================

# 15 pose angles

POSE_ANGLE_TRIPLETS = [
    (11, 13, 15),
    (12, 14, 16),
    (13, 11, 12),
    (14, 12, 11),
    (11, 12, 24),
    (12, 11, 23),
    (23, 11, 13),
    (24, 12, 14),
    (11, 23, 25),
    (12, 24, 26),
    (23, 25, 27),
    (24, 26, 28),
    (13, 15, 17),
    (14, 16, 18),
    (11, 0, 12)
]


# 13 left-hand angles
HAND_ANGLE_TRIPLETS = [
    (0, 1, 2),
    (1, 2, 3),
    (2, 3, 4),

    (0, 5, 6),
    (5, 6, 7),
    (6, 7, 8),

    (0, 9, 10),
    (9, 10, 11),
    (10, 11, 12),

    (0, 13, 14),
    (13, 14, 15),
    (14, 15, 16),

    (0, 17, 18)
]

# 13 left + 13 right + 15 pose = 41


# ============================================================
# DISTANCE CONFIGURATION
# ============================================================

POSE_DISTANCE_PAIRS = [
    (11, 12),
    (11, 13),
    (12, 14),
    (13, 15),
    (14, 16),
    (15, 16),
    (11, 23),
    (12, 24)
]

HAND_DISTANCE_PAIRS = [
    (0, 4),
    (0, 8),
    (0, 12),
    (0, 16),
    (0, 20),
    (4, 8),
    (8, 12),
    (12, 16),
    (16, 20)
]

# Pose = 8
# Left hand = 9
# Right hand = 9
# TOTAL = 26


# ============================================================
# MAIN FEATURE EXTRACTION
# ============================================================

def extract_dynamic_features(results):
    """
    Extract exactly 285 features from MediaPipe Holistic results.

    Returns:
        numpy.ndarray shape (285,)
    """

    features = []

    pose = results.pose_landmarks
    left_hand = results.left_hand_landmarks
    right_hand = results.right_hand_landmarks

    # --------------------------------------------------------
    # RAW FEATURES = 218
    # --------------------------------------------------------

    # Pose
    if pose is None:

        features.extend([0.0] * 116)

    else:

        for index in POSE_INDICES:

            point = _point_from_landmarks(
                pose,
                index
            )

            lm = pose.landmark[index]

            features.extend([
                point[0],
                point[1],
                point[2],
                getattr(lm, "visibility", 1.0)
            ])

    # Left Hand

    if left_hand is None:

        features.extend([0.0] * 51)

    else:

        for index in HAND_INDICES:

            point = _point_from_landmarks(
                left_hand,
                index
            )

            features.extend([
                point[0],
                point[1],
                point[2]
            ])

    # Right Hand

    if right_hand is None:

        features.extend([0.0] * 51)

    else:

        for index in HAND_INDICES:

            point = _point_from_landmarks(
                right_hand,
                index
            )

            features.extend([
                point[0],
                point[1],
                point[2]
            ])

    # --------------------------------------------------------
    # ANGLES = 41
    # --------------------------------------------------------

    # Pose angles

    for a_idx, b_idx, c_idx in POSE_ANGLE_TRIPLETS:

        a = _point_from_landmarks(pose, a_idx)
        b = _point_from_landmarks(pose, b_idx)
        c = _point_from_landmarks(pose, c_idx)

        features.append(
            _calculate_angle(a, b, c)
        )

    # Left hand angles

    for a_idx, b_idx, c_idx in HAND_ANGLE_TRIPLETS:

        a = _point_from_landmarks(left_hand, a_idx)
        b = _point_from_landmarks(left_hand, b_idx)
        c = _point_from_landmarks(left_hand, c_idx)

        features.append(
            _calculate_angle(a, b, c)
        )

    # Right hand angles

    for a_idx, b_idx, c_idx in HAND_ANGLE_TRIPLETS:

        a = _point_from_landmarks(right_hand, a_idx)
        b = _point_from_landmarks(right_hand, b_idx)
        c = _point_from_landmarks(right_hand, c_idx)

        features.append(
            _calculate_angle(a, b, c)
        )

    # --------------------------------------------------------
    # DISTANCES = 26
    # --------------------------------------------------------

    # Pose distances

    for a_idx, b_idx in POSE_DISTANCE_PAIRS:

        a = _point_from_landmarks(pose, a_idx)
        b = _point_from_landmarks(pose, b_idx)

        features.append(
            _calculate_distance(a, b)
        )

    # Left hand distances

    for a_idx, b_idx in HAND_DISTANCE_PAIRS:

        a = _point_from_landmarks(left_hand, a_idx)
        b = _point_from_landmarks(left_hand, b_idx)

        features.append(
            _calculate_distance(a, b)
        )

    # Right hand distances

    for a_idx, b_idx in HAND_DISTANCE_PAIRS:

        a = _point_from_landmarks(right_hand, a_idx)
        b = _point_from_landmarks(right_hand, b_idx)

        features.append(
            _calculate_distance(a, b)
        )

    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    features = np.array(
        features,
        dtype=np.float32
    )

    if features.shape[0] != 285:

        raise ValueError(
            f"Expected 285 features, "
            f"but got {features.shape[0]}"
        )

    return features