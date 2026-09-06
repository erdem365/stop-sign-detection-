"""
synthetic_scenarios.py
------------------------
Gerçek dataset olmadiığı durumlarda pipeline'ın farklı zorluk senaryolarına
karşı davranışını incelemek için SENTETIK görüntü üreten yardımcı fonksiyonlar.

ONEMLI: Bu senaryolar gerçek fotoğrafların yerini TUTMAZ. Amaç, algoritmanın
kod seviyesinde makul davrandığını (crash etmiyor, aşırı sıkılaştırılmış
filtreler yüzünden her şeyi eleyip durmuyor, açık biçimde false-positive
üretmiyor) önceden gözlemlemektir. Gerçek doğruluk ölçümü için gerçek
dataset gereklidir (bkz. README "Results").
"""

from typing import Optional, Tuple

import cv2
import numpy as np


def _octagon_points(cx: int, cy: int, r: int) -> np.ndarray:
    pts = []
    for i in range(8):
        angle = np.pi / 8 + i * np.pi / 4
        pts.append([int(cx + r * np.cos(angle)), int(cy + r * np.sin(angle))])
    return np.array(pts, dtype=np.int32)


def make_clean_sign(size=(480, 640), center=(300, 240), radius=90, red_bgr=(0, 0, 200)):
    """Temiz, tam görünür, iyi aydınlatılmış STOP tabelası (referans senaryo)."""
    img = np.full((*size, 3), (120, 120, 120), dtype=np.uint8)
    pts = _octagon_points(*center, radius)
    cv2.fillPoly(img, [pts], red_bgr)
    return img, center


def make_dark_shadowed_sign(size=(480, 640), center=(300, 240), radius=90):
    """Gölgeli / düşük aydınlatma altında koyulaştırılmış kırmızı tabela."""
    dark_red = (0, 0, 90)  # normal (0,0,200)'e gore cok daha koyu
    img = np.full((*size, 3), (40, 40, 40), dtype=np.uint8)  # karanlik sahne
    pts = _octagon_points(*center, radius)
    cv2.fillPoly(img, [pts], dark_red)
    return img, center


def make_partially_occluded_sign(size=(480, 640), center=(300, 240), radius=90):
    """Tabelanin bir kısmı başka bir nesne (yeşil dikdörtgen) tarafından kapatılmış."""
    img = np.full((*size, 3), (120, 120, 120), dtype=np.uint8)
    pts = _octagon_points(*center, radius)
    cv2.fillPoly(img, [pts], (0, 0, 200))
    # Tabelanin alt yarisini kapatan bir "yaprak/dal" benzetimi (yesil blok)
    cv2.rectangle(img, (center[0] - radius, center[1]), (center[0] + radius, center[1] + radius + 20), (30, 90, 30), -1)
    return img, center


def make_small_far_sign(size=(480, 640), center=(400, 150), radius=18):
    """Uzak mesafeden görünen, küçük boyutlu tabela."""
    img = np.full((*size, 3), (130, 130, 130), dtype=np.uint8)
    pts = _octagon_points(*center, radius)
    cv2.fillPoly(img, [pts], (0, 0, 200))
    return img, center


def make_sign_with_distractor(size=(480, 640), center=(280, 260), radius=85):
    """
    Ana STOP tabelası + arka planda baska kırmızı nesneler (araç, tabela vb.
    benzetimi). Algoritmanın en büyük/en uygun konturu seçmesi beklenir.
    """
    img = np.full((*size, 3), (125, 125, 125), dtype=np.uint8)
    pts = _octagon_points(*center, radius)
    cv2.fillPoly(img, [pts], (0, 0, 200))

    # Dikkat dağıtıcı 1: küçük kırmızı daire (uzak ışık/far benzetimi)
    cv2.circle(img, (560, 90), 10, (0, 0, 210), -1)
    # Dikkat dağıtıcı 2: ince kırmızı dikdortgen (arac gövdesi benzetimi,
    # aspect-ratio filtresine takılması beklenir)
    cv2.rectangle(img, (50, 380), (250, 410), (0, 0, 190), -1)
    return img, center


def make_no_sign_image(size=(480, 640)):
    """Hiç kırmızı STOP tabelası içermeyen, notr bir görüntü (true negative)."""
    img = np.full((*size, 3), (110, 130, 110), dtype=np.uint8)  # yesilimsi (bitki/cim benzetimi)
    cv2.rectangle(img, (100, 100), (300, 300), (150, 120, 90), -1)  # mavimsi-gri bina benzetimi (kirmizi degil)
    return img, None


def make_only_distractor_image(size=(480, 640)):
    """
    Kırmızı içerir ama STOP tabelası YOK; yalnızca aspect-ratio/extent
    filtrelerine takılması beklenen dikkat dağıtıcılar var (true negative,
    false-positive testi).
    """
    img = np.full((*size, 3), (120, 120, 120), dtype=np.uint8)
    cv2.rectangle(img, (80, 300), (400, 340), (0, 0, 200), -1)   # uzun ince kırmızı erit
    cv2.circle(img, (500, 80), 6, (0, 0, 210), -1)                 # küçük kırmızı nokta
    return img, None


SCENARIOS = {
    "clean": make_clean_sign,
    "dark_shadowed": make_dark_shadowed_sign,
    "partially_occluded": make_partially_occluded_sign,
    "small_far": make_small_far_sign,
    "with_distractor": make_sign_with_distractor,
    "no_sign": make_no_sign_image,
    "only_distractor": make_only_distractor_image,
}
