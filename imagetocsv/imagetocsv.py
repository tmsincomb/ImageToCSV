"""Main module."""
from __future__ import annotations

import gc
import re
import subprocess

import cv2
import numpy as np
import numpy.typing as npt
import pandas as pd
import pdftotext

from imagetocsv.string_modifiers import fix_common_mistakes
from imagetocsv.tempfile import NamedTemporaryFile

# import pytesseract



def pdftocsv(file: str) -> list[list[str]]:
    """Convert a pdf file to a list of lists of strings. We do this to keep layout information.

    Parameters
    ----------
    file : str
        Path to the pdf file.

    Returns
    -------
    list[list[str]]
        List of lists of strings.
    """
    tmpchar = "*"
    special_chars = "%"
    all_positions: set[int] = set()

    # Find start positions of all columns
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f, physical=True)[0]
        for line in pdf.split("\n"):
            for special_char in special_chars.split():
                line = line.replace(f" {special_char}", f"{special_char} ")
                line = line.replace(f"  {special_char}", f"{special_char}  ")
            line = f" {line.strip()} "
            for word in line.split():
                if not word:
                    continue
                word = f" {word} "
                positions = [m.start() for m in re.finditer(word, line)]
                all_positions |= set(positions)
        ali_positions = sorted(list(all_positions))
        ali_positions = [p for p in ali_positions]
        ali_positions[0] = ali_positions[0]
        if len(ali_positions) > 1:
            ali_positions[-1] = ali_positions[-1]

        # Add special temp character to empty string to empty cell
        lines: list[str] = []
        for line in pdf.split("\n"):
            if not [v for v in line.strip()]:
                continue
            for special_char in special_chars.split():
                line: str = line.replace(f" {special_char}", f"{special_char} ")
                line: str = line.replace(f"  {special_char}", f"{special_char}  ")
            for pos in all_positions:
                try:
                    if not line[pos].strip():
                        line = line[:pos] + tmpchar + line[pos + 1 :]
                except IndexError:
                    line = line.ljust(pos, " ") + tmpchar
            lines.append(line)

        # 1. replace empty cells with special char with empty string
        # 2. fix any cells with common issues
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


def add_df_indexes_headers(df: pd.DataFrame, index_name: str, index: str, column_header: str) -> pd.DataFrame:
    """Add indexes and headers to a dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to add indexes and headers to.
    index_name : str, optional
        Name of the index, by default None
    index : list[str] | str, optional
        Index values, by default None
    column_header : list[str] | str, optional
        Column header values, by default None

    Returns
    -------
    pd.DataFrame
        The dataframe with indexes and headers.
    """
    if column_header:
        df.columns = column_header.split(",") if isinstance(column_header, str) else column_header
    if index:
        df.index = index.split(",") if isinstance(index, str) else index
    if index_name:
        df.index.name = index_name

    return df


def unsharp_mask(
    image: npt.NDArray[np.uint8],
    kernel_size: tuple[int, int] = (5, 5),
    sigma: float = 1.0,
    amount: float = 1.0,
    threshold: float = 0,
):
    """Return a sharpened version of the image, using an unsharp mask.

    Parameters
    ----------
    image : np.ndarray
        image - The image to be sharpened.
    kernel_size : tuple[int, int], optional
        kernel_size - The size of the Gaussian blur kernel, by default (5, 5)
    sigma : float, optional
        sigma - The standard deviation of the Gaussian blur, by default 1.0
    amount : float, optional
        amount - The strength of the sharpening, by default 1.0
    threshold : float, optional
        threshold - The threshold for the mask, by default 0

    Returns
    -------
    np.ndarray
        The sharpened image.
    """
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
    """Convert an image file to a pandas DataFrame.

    Parameters
    ----------
    file : str
        Path to the image file.
    index_name : str, optional
        Name of the index, by default None
    index : list[str] | str, optional
        Index values, by default None
    column_header : list[str] | str, optional
        Column header values, by default None

    Returns
    -------
    pd.DataFrame
    """
    file = str(file)

    img = cv2.imread(file)
    h, w, _ = img.shape
    img = cv2.resize(img, (w * 3, h * 3))
    img = unsharp_mask(img)
    grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    (_thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 180, 255, cv2.THRESH_BINARY)

    # TODO: see if we can use pytesseract to get the table for windows in version 0.3.0
    # custom_oem_psm_config = r"""
    #     --oem 3
    #     --psm 6
    #     -1 deu
    #     -c tessedit_char_whitelist=0123456789.,%
    #     -c preserve_interword_spaces=1
    #     -c tessedit_create_pdf=1
    # """
    # pdf: bytes = pytesseract.image_to_pdf_or_hocr(
    #     "blackAndWhiteImage.png", lang="eng", extension="pdf", config=custom_oem_psm_config
    # )

    tmp = NamedTemporaryFile(delete=False, mode=None)
    prefix: str = tmp.name
    # Tesseract cannot handle stdin so we need to write the image to a file first
    cv2.imwrite(prefix + ".png", blackAndWhiteImage)
    _ = subprocess.run(
        [
            "tesseract",
            "--oem",
            "3",
            "--psm",
            "6",
            "-l",
            "eng",
            "-c",
            "tessedit_char_whitelist=0123456789.,%",
            "-c",
            "preserve_interword_spaces=1",
            "-c",
            "tessedit_create_pdf=1",
            prefix + ".png",
            prefix,
            # "pdf",
        ],
        capture_output=True,
    )
    # pdftotext for layout analysis
    rows = pdftocsv(prefix + ".pdf")
    # remove the temporary files in garbage collection for windows to handle it
    del tmp
    gc.collect()

    df = pd.DataFrame(rows)
    df = add_df_indexes_headers(df, index_name, index, column_header)

    return df
