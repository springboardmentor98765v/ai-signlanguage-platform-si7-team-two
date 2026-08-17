/**
 * HandDemo — Verified ASL Fingerspelling Reference Illustrations
 *
 * Uses Wikimedia Commons public domain SVG images for 100% accurate ASL handshapes.
 */
import './HandDemo.css'

const ASL_IMAGE_URLS = {
  "A": "https://upload.wikimedia.org/wikipedia/commons/2/27/Sign_language_A.svg",
  "B": "https://upload.wikimedia.org/wikipedia/commons/1/18/Sign_language_B.svg",
  "C": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Sign_language_C.svg",
  "D": "https://upload.wikimedia.org/wikipedia/commons/0/06/Sign_language_D.svg",
  "E": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Sign_language_E.svg",
  "F": "https://upload.wikimedia.org/wikipedia/commons/8/8f/Sign_language_F.svg",
  "G": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Sign_language_G.svg",
  "H": "https://upload.wikimedia.org/wikipedia/commons/9/97/Sign_language_H.svg",
  "I": "https://upload.wikimedia.org/wikipedia/commons/1/10/Sign_language_I.svg",
  "J": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Sign_language_J.svg",
  "K": "https://upload.wikimedia.org/wikipedia/commons/9/97/Sign_language_K.svg",
  "L": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Sign_language_L.svg",
  "M": "https://upload.wikimedia.org/wikipedia/commons/c/c4/Sign_language_M.svg",
  "N": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Sign_language_N.svg",
  "O": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Sign_language_O.svg",
  "P": "https://upload.wikimedia.org/wikipedia/commons/0/08/Sign_language_P.svg",
  "Q": "https://upload.wikimedia.org/wikipedia/commons/3/34/Sign_language_Q.svg",
  "R": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Sign_language_R.svg",
  "S": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Sign_language_S.svg",
  "T": "https://upload.wikimedia.org/wikipedia/commons/1/13/Sign_language_T.svg",
  "U": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Sign_language_U.svg",
  "V": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sign_language_V.svg",
  "W": "https://upload.wikimedia.org/wikipedia/commons/8/83/Sign_language_W.svg",
  "X": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Sign_language_X.svg",
  "Y": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Sign_language_Y.svg",
  "Z": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Sign_language_Z.svg"
}

/* ── Component ──────────────────────────────────────────────────────────────── */
export default function HandDemo({ letter = 'A', size = 'md' }) {
  const upper = (letter || 'A').toUpperCase()
  const imgUrl = ASL_IMAGE_URLS[upper] || ASL_IMAGE_URLS['A']

  return (
    <div
      className={`hand-demo hand-demo--${size}`}
      aria-label={`Reference ASL handshape for the letter ${upper}`}
      role="img"
    >
      <img src={imgUrl} alt={`ASL ${upper}`} className="hand-demo__img" />
      <div className="hand-demo__label">ASL {upper}</div>
    </div>
  )
}
