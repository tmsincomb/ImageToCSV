from __future__ import annotations


def fix_common_mistakes(line: str):
    if not line:
        return ""

    line = line.strip()

    # Zero is a problem child. Needs special handling.
    if line.lower() in ["00", "o0", "oo", "0o", "o", "o°", "°o", "fe", "°"]:
        return "0"

    line = line.replace("@", "")
    line = line.replace("#", "")
    line = line.replace(",", "")

    if not line:
        return ""

    if line[-1] == "%" and "." not in line:
        line = line[:-3] + "." + line[len(line) - 3 :]

    return line
