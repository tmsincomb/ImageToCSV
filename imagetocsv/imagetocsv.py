"""Main module."""
from __future__ import annotations

import gc
import re

import cv2
import numpy as np
import pandas as pd
import pdftotext
import pytesseract

from imagetocsv.string_modifiers import fix_common_mistakes
from imagetocsv.tempfile import NamedTemporaryFile


def pdftocsv(file: str):
    tmpchar = "*"
    special_chars = "%"
    all_positions = set()
    # file = '../tests/data/myimage.pdf'
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f, physical=True)[0]
        for line in pdf.split("\n"):
            for special_char in special_chars.split():
                line = line.replace(f" {special_char}", f"{special_char} ")
                line = line.replace(f"  {special_char}", f"{special_char}  ")
            line = f" {line.strip()} "
            for i, word in enumerate(line.split()):
                if not word:
                    continue
                word = f" {word} "
                # print(line)
                positions = [m.start() for m in re.finditer(word, line)]
                all_positions |= set(positions)

        all_positions = sorted(list(all_positions))
        all_positions = [p for p in all_positions]
        all_positions[0] = all_positions[0]
        if len(all_positions) > 1:
            all_positions[-1] = all_positions[-1]

        lines = []
        for line in pdf.split("\n"):
            # line = line.strip()
            # print(line)
            if not [v for v in line.strip()]:
                continue
            for special_char in special_chars.split():
                line = line.replace(f" {special_char}", f"{special_char} ")
                line = line.replace(f"  {special_char}", f"{special_char}  ")
            for pos in all_positions:
                try:
                    if not line[pos].strip():
                        line = line[:pos] + tmpchar + line[pos + 1 :]
                except IndexError:
                    line = line.ljust(pos, " ") + tmpchar
            lines.append(line)

        rows = []
        for line in lines:
            row = []
            for cell in line.split():
                if tmpchar == cell:
                    cell = ""
                cell = fix_common_mistakes(cell)
                row.append(cell)
            rows.append(row)

    return rows


def add_df_indexes_headers(df: pd.DataFrame, index_name: str, index: str, column_header: str):

    if column_header:
        df.columns = column_header.split(",") if isinstance(column_header, str) else column_header
    if index:
        df.index = index.split(",") if isinstance(index, str) else index
    if index_name:
        df.index.name = index_name

    return df


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def imagetocsv(
    file: str,
    index_name: str | None = None,
    index: list[str] | str | None = None,
    column_header: list[str] | str | None = None,
) -> pd.DataFrame:

    file = str(file)

    img = cv2.imread(file)
    h, w, _ = img.shape
    img = cv2.resize(img, (w * 3, h * 3))
    img = unsharp_mask(img)
    grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    (_thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 180, 255, cv2.THRESH_BINARY)

    custom_oem_psm_config = r"""
        --oem 3 --psm 6
        -c tessedit_char_whitelist=0123456789.,% -c preserve_interword_spaces=1
    """
    # string = pytesseract.image_to_string(blackAndWhiteImage, lang="eng", config=custom_oem_psm_config)
    # print()
    # print(string)
    cv2.imwrite("log.png", blackAndWhiteImage)
    # string = pytesseract.image_to_string(blackAndWhiteImage, lang="eng", config=custom_oem_psm_config)
    # print()
    # print(string)
    pdf: bytes = pytesseract.image_to_pdf_or_hocr(
        blackAndWhiteImage, lang="eng", extension="pdf", config=custom_oem_psm_config
    )

    tmp = NamedTemporaryFile(delete=False, suffix=".pdf", mode=None)
    pdfname = tmp.name
    with open(pdfname, "wb") as fp:
        fp.write(pdf)
    rows = pdftocsv(pdfname)
    del tmp
    gc.collect()

    df = pd.DataFrame(rows)
    # print(df.to_markdown())
    df = add_df_indexes_headers(df, index_name, index, column_header)

    return df
