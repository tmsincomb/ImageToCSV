def fix_common_mistakes(line: str):
    if not line:
        return ""
    line = line.replace("@", "")
    line = line.replace("#", "")
    line = line.replace(",", "")
    if not line:
        return ""
    if line[-1] == "%" and "." not in line:
        line = line[:-3] + "." + line[len(line) - 3 :]
    line = line.strip()
    return line
