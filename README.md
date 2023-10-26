<h1 align="center">
  <br>

</h1>

<div class="flex-container" align="center">
    <a href="https://github.com/jwillis0720/template-repo/commits/master">
    <a href="https://img.shields.io/badge/Python-3.%7C3.8%7C3.9%7C3.10-blue">
    <img src="https://img.shields.io/badge/Python-3.7%7C3.8%7C3.9%7C3.10%7C3.11-blue"
        alt="Python Version">
    <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg"
        alt="Format Version">
    <a href="https://codecov.io/gh/jwillis0720/template-repo">
    <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"
        alt="pre commit">
    </br>
    <a href="https://tesseract-ocr.github.io/tessdoc/Installation.html">
    <img src="https://img.shields.io/badge/Tesseract-5.2.0-teal.svg" alt="Tesseract">
    <a href="https://poppler.freedesktop.org/">
    <img src="https://img.shields.io/badge/Poppler-22.11.0-teal.svg" alt="Tesseract">
    </br>
    <img src="https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0"
        alt="MacOS">
    <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black"
        alt="Linux">
    <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white"
        alt="Windows">
</div>

<p align="center" style="color:green">
  <a href="#about">About</a> •
  <a href="#installation">Install</a> •
  <a href="#terminal">Terminal</a> •
  <a href="#python">Python</a> •
  <a href="#license">License</a>
</p>

# About

Converts an Image to a CSV. This exists because Chorus 3.0 is bat-shit and only shows images for vital metadata.
<img src="https://raw.githubusercontent.com/tmsincomb/ImageToCSV/v0.2.0/docs/images/convert.png" width="1025"/>

# Prerequisites

## Anaconda

I am partial towards [miniforge](https://github.com/conda-forge/miniforge), but you can replace these commands with your favorite conda distribution.

### Windows Miniforge Installation

Special walkthrough for Windows users since Windows is awful.

```bash
curl -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
start /wait "" Miniforge3-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniforge3
# Follow the prompts.
```

# Bugs

## Linux using Python 3.7

Conda does not install all needed packages for Python 3.7 so you need to install the following to get ImageToCSV to work properly.

```bash
sudo apt install --yes build-essential libpoppler-cpp-dev pkg-config tesseract-ocr libtesseract-dev
```

# Installation MacOS

```bash
conda create -n imagetocsv pip python=3.11.6
conda activate imagetocsv
conda install -y -c conda-forge clang_osx-64 clangxx_osx-64 poppler==22.11.0 tesseract==5.2.0
pip install imagetocsv
```

# Installation Linux

```bash
conda create -n imagetocsv pip python=3.11.6
conda activate imagetocsv
conda install -y -c conda-forge gcc gxx poppler==22.11.0 tesseract==5.2.0
pip install imagetocsv
```

# Installation Windows 10/11

### Note that this is untested and may not work if you do not have a C++ compiler installed.

```bash
conda create -n imagetocsv pip python=3.11.6
conda activate imagetocsv
conda install -y -c conda-forge poppler==22.11.0 tesseract==5.2.0
pip install imagetocsv
```

# Development

## Pip install cloned repo

```bash
pip install -e ".[dev]"
```

## Testing

```bash
cd ImageToCSV
pytest -svvv tests
```

## Preconfiguring Index/Column Names

If you have a lot of images to convert, you can preconfigure the index and column names to save time in the hardcoded_options.py file [here](https://github.com/tmsincomb/ImageToCSV/blob/main/imagetocsv/hardcoded_options.py). Each option will need a format of ``dict[str, tuple[str, list[str], list[str]]]`` aka slug -> (name, indexes, columns).

```bash
imagetocsv -p myslug myimage.png
```

# Usage

## Terminal Help Message

[CSV_PATH] means that it is a stdout (printed on the terminal) if output is not specified.

```bash
Usage: imagetocsv [OPTIONS] IMAGE_PATH [CSV_PATH]

  Console script for imagetocsv.

Options:
  --version                 Show the version and exit.
  -v, --verbose             Vebosity level, ex. -vvvvv for debug level logging
  -n, --index_name TEXT     Index Name for the CSV file
  -i, --index TEXT          Index for the CSV file
  -c, --column_header TEXT  Columns for the CSV file
  -p, --preconfigured-options TEXT

  --help                    Show this message and exit.
```

## Terminal

```bash
# Convert an image to a CSV
imagetocsv myimage.png output.csv
```

```bash
# Convert an image to a stdout (printed on the terminal) TSV
imagetocsv myimage.png
```

|      |      0 | 1      | 2       | 3         | 4      | 5         | 6      |
| ---: | -----: | :----- | :------ | :-------- | :----- | :-------- | :----- |
|    0 | 598150 |        | 100.00% | 123428.50 | 57.53% | 130689.00 | 50.55% |
|    1 | 237987 | 39.79% | 39.79%  | 134356.00 | 14.45% | 102556.00 | 30.89% |
|    2 | 228000 | 95.80% | 38.12%  | 433804.00 | 13.96% | 100917.00 | 29.64% |
|    3 | 222453 | 97.57% | 37.19%  | 133307.00 | 13.63% | 100091.00 | 29.09% |
|    4 | 212474 | 95.51% | 35.52%  | 134238.00 | 12.97% | 9700.00   | 29.27% |
|    5 |  55885 | 26.30% | 9.34%   | 131386.00 | 13.34% | 93086.00  | 27.69% |
|    6 |  34745 | 56.80% | 5.31%   | 127549.00 | 10.25% | 88501.00  | 24.60% |
|    7 |  22496 | 40.25% | 3.76%   | 14152450  | 15.79% | 102606.00 | 30.31% |
|    8 |  17409 | 77.39% | 2.91%   | 144624.00 | 14.88% | 107966.00 | 28.93% |
|    9 |   2663 | 15.30% | 0.45%   | 163750.00 | 11.93% | 130908.00 | 26.18% |
|   10 |      5 | 0.03%  | 0.00%   | 166073.00 | 5.07%  | 160211.00 | 6.57%  |
|   11 |  14736 | 84.65% | 2.46%   | 14126450  | 14.20% | 103995.00 | 28.13% |
|   12 |      5 | 0.03%  | 0.00%   | 162803.00 | 6.04%  | 156540.00 | 9.02%  |
|   13 |      0 | 0.00%  | 0.00%   |           |        |           |        |
|   14 |   8888 | 39.51% | 1.49%   | 431473.00 | 15.37% | 90965.50  | 28.65% |
|   15 |   1806 | 8.03%  | 0.30%   | 153347.00 | 12.19% | 121119.50 | 24.60% |
|   16 |   4896 | 21.76% | 0.82%   | 141244.00 | 16.41% | 101527.00 | 30.63% |
|   17 |   6906 | 30.70% | 1.15%   | 147753.00 | 12.13% | 113108.50 | 25.94% |

```bash
# Used for Chorus 3.0 to auto header and index names.
imagetocsv -p chorus myimage.png
```

| Population      | Events  | % Parent | % Total | FSC-A Median | FSC-A %rCV | SSC-A Median | SSC-A %rCV |
| :-------------- | :------ | :------- | :------ | :----------- | :--------- | :----------- | :--------- |
| All Events      | 598,150 |          | 100.00% | 123428.50    | 57.53%     | 130689.00    | 50.55%     |
| Lymphocytes     | 237,987 | 39.79%   | 39.79%  | 134356.00    | 14.45%     | 102556.00    | 30.89%     |
| Single cells... | 228,000 | 95.80%   | 38.12%  | 433804.00    | 13.96%     | 100917.00    | 29.64%     |
| Single cells... | 222,453 | 97.57%   | 37.19%  | 133307.00    | 13.63%     | 100091.00    | 29.09%     |
| Live/Dead       | 212,474 | 95.51%   | 35.52%  | 134238.00    | 12.97%     | 9700.00      | 29.27%     |
| CD19+ Dump-     | 55,885  | 26.30%   | 9.34%   | 131386.00    | 13.34%     | 93086.00     | 27.69%     |
| Naive gD+       | 34,745  | 56.80%   | 5.31%   | 127549.00    | 10.25%     | 88501.00     | 24.60%     |
| Memory IgD-     | 22,496  | 40.25%   | 3.76%   | 14152450     | 15.79%     | 102606.00    | 30.31%     |
| IgD- KO-        | 17,409  | 77.39%   | 2.91%   | 144624.00    | 14.88%     | 107966.00    | 28.93%     |
| P15-1           | 2,663   | 15.30%   | 0.45%   | 163750.00    | 11.93%     | 130908.00    | 26.18%     |
| P15-2           | 5       | 0.03%    | 0.00%   | 166073.00    | 5.07%      | 160211.00    | 6.57%      |
| P15-3           | 14,736  | 84.65%   | 2.46%   | 14126450     | 14.20%     | 103995.00    | 28.13%     |
| P15-4           | 5       | 0.03%    | 0.00%   | 162803.00    | 6.04%      | 156540.00    | 9.02%      |
| MARIO WT++      | 0       | 0.00%    | 0.00%   |              |            |              |            |
| P14-1           | 8,888   | 39.51%   | 1.49%   | 431473.00    | 15.37%     | 90965.50     | 28.65%     |
| P14-2           | 1,806   | 8.03%    | 0.30%   | 153347.00    | 12.19%     | 121119.50    | 24.60%     |
| P14-3           | 4896    | 21.76%   | 0.82%   | 141244.00    | 16.41%     | 101527.00    | 30.63%     |
| P14-4           | 6,906   | 30.70%   | 1.15%   | 147753.00    | 12.13%     | 113108.50    | 25.94%     |

## Terminal Advanced

Adding Index Name, Index, and Column Header. They need to match the deminsions of the matrix! This may be more trouble than its worth so, this is just to show you can do it. No pressure.

```bash
imagetocsv myimage.jpg \
  --index_name "Population" \
  --index "All Events,Lymphocytes,Single cells...,Single cells...,Live/Dead,CD19+ Dump-,Naive gD+,Memory IgD-,IgD- KO-,P15-1,P15-2,P15-3,P15-4,MARIO WT++,P14-1,P14-2,P14-3,P14-4" \
  --column_header "Events,%Parent,%Total,FSC-A Median,FSC-A %rCV,SSC-A Median,SSC-A %rCV"
```

| Population      | Events  | % Parent | % Total | FSC-A Median | FSC-A %rCV | SSC-A Median | SSC-A %rCV |
| :-------------- | :------ | :------- | :------ | :----------- | :--------- | :----------- | :--------- |
| All Events      | 598,150 |          | 100.00% | 123428.50    | 57.53%     | 130689.00    | 50.55%     |
| Lymphocytes     | 237,987 | 39.79%   | 39.79%  | 134356.00    | 14.45%     | 102556.00    | 30.89%     |
| Single cells... | 228,000 | 95.80%   | 38.12%  | 433804.00    | 13.96%     | 100917.00    | 29.64%     |
| Single cells... | 222,453 | 97.57%   | 37.19%  | 133307.00    | 13.63%     | 100091.00    | 29.09%     |
| Live/Dead       | 212,474 | 95.51%   | 35.52%  | 134238.00    | 12.97%     | 9700.00      | 29.27%     |
| CD19+ Dump-     | 55,885  | 26.30%   | 9.34%   | 131386.00    | 13.34%     | 93086.00     | 27.69%     |
| Naive gD+       | 34,745  | 56.80%   | 5.31%   | 127549.00    | 10.25%     | 88501.00     | 24.60%     |
| Memory IgD-     | 22,496  | 40.25%   | 3.76%   | 14152450     | 15.79%     | 102606.00    | 30.31%     |
| IgD- KO-        | 17,409  | 77.39%   | 2.91%   | 144624.00    | 14.88%     | 107966.00    | 28.93%     |
| P15-1           | 2,663   | 15.30%   | 0.45%   | 163750.00    | 11.93%     | 130908.00    | 26.18%     |
| P15-2           | 5       | 0.03%    | 0.00%   | 166073.00    | 5.07%      | 160211.00    | 6.57%      |
| P15-3           | 14,736  | 84.65%   | 2.46%   | 14126450     | 14.20%     | 103995.00    | 28.13%     |
| P15-4           | 5       | 0.03%    | 0.00%   | 162803.00    | 6.04%      | 156540.00    | 9.02%      |
| MARIO WT++      | 0       | 0.00%    | 0.00%   |              |            |              |            |
| P14-1           | 8,888   | 39.51%   | 1.49%   | 431473.00    | 15.37%     | 90965.50     | 28.65%     |
| P14-2           | 1,806   | 8.03%    | 0.30%   | 153347.00    | 12.19%     | 121119.50    | 24.60%     |
| P14-3           | 4896    | 21.76%   | 0.82%   | 141244.00    | 16.41%     | 101527.00    | 30.63%     |
| P14-4           | 6,906   | 30.70%   | 1.15%   | 147753.00    | 12.13%     | 113108.50    | 25.94%     |

## Python

```python
from imagetocsv import imagetocsv
from imagetocsv.examples import no_grid_example


df = imagetocsv(no_grid_example)
print(df.to_markdown())

```

|      |      0 | 1      | 2       | 3         | 4      | 5         | 6      |
| ---: | -----: | :----- | :------ | :-------- | :----- | :-------- | :----- |
|    0 | 598150 |        | 100.00% | 123428.50 | 57.53% | 130689.00 | 50.55% |
|    1 | 237987 | 39.79% | 39.79%  | 134356.00 | 14.45% | 102556.00 | 30.89% |
|    2 | 228000 | 95.80% | 38.12%  | 433804.00 | 13.96% | 100917.00 | 29.64% |
|    3 | 222453 | 97.57% | 37.19%  | 133307.00 | 13.63% | 100091.00 | 29.09% |
|    4 | 212474 | 95.51% | 35.52%  | 134238.00 | 12.97% | 9700.00   | 29.27% |
|    5 |  55885 | 26.30% | 9.34%   | 131386.00 | 13.34% | 93086.00  | 27.69% |
|    6 |  34745 | 56.80% | 5.31%   | 127549.00 | 10.25% | 88501.00  | 24.60% |
|    7 |  22496 | 40.25% | 3.76%   | 14152450  | 15.79% | 102606.00 | 30.31% |
|    8 |  17409 | 77.39% | 2.91%   | 144624.00 | 14.88% | 107966.00 | 28.93% |
|    9 |   2663 | 15.30% | 0.45%   | 163750.00 | 11.93% | 130908.00 | 26.18% |
|   10 |      5 | 0.03%  | 0.00%   | 166073.00 | 5.07%  | 160211.00 | 6.57%  |
|   11 |  14736 | 84.65% | 2.46%   | 14126450  | 14.20% | 103995.00 | 28.13% |
|   12 |      5 | 0.03%  | 0.00%   | 162803.00 | 6.04%  | 156540.00 | 9.02%  |
|   13 |      0 | 0.00%  | 0.00%   |           |        |           |        |
|   14 |   8888 | 39.51% | 1.49%   | 431473.00 | 15.37% | 90965.50  | 28.65% |
|   15 |   1806 | 8.03%  | 0.30%   | 153347.00 | 12.19% | 121119.50 | 24.60% |
|   16 |   4896 | 21.76% | 0.82%   | 141244.00 | 16.41% | 101527.00 | 30.63% |
|   17 |   6906 | 30.70% | 1.15%   | 147753.00 | 12.13% | 113108.50 | 25.94% |

## Python Advanced

```python
from imagetocsv import imagetocsv
from imagetocsv.examples import no_grid_example


df = imagetocsv(
        no_grid_example,
        index_name="Population",
        index=[
                "All Events",
                "Lymphocytes",
                "Single cells...",
                "Single cells...",
                "Live/Dead",
                "CD19+ Dump-",
                "Naive gD+",
                "Memory IgD-",
                "IgD- KO-",
                "P15-1",
                "P15-2",
                "P15-3",
                "P15-4",
                "MARIO WT++",
                "P14-1",
                "P14-2",
                "P14-3",
                "P14-4",
        ],
        column_header=["Events", "% Parent", "% Total", "FSC-A Median", "FSC-A %rCV", "SSC-A Median", "SSC-A %rCV"],
)
print(df.to_markdown())
```

| Population      | Events  | % Parent | % Total | FSC-A Median | FSC-A %rCV | SSC-A Median | SSC-A %rCV |
| :-------------- | :------ | :------- | :------ | :----------- | :--------- | :----------- | :--------- |
| All Events      | 598,150 |          | 100.00% | 123428.50    | 57.53%     | 130689.00    | 50.55%     |
| Lymphocytes     | 237,987 | 39.79%   | 39.79%  | 134356.00    | 14.45%     | 102556.00    | 30.89%     |
| Single cells... | 228,000 | 95.80%   | 38.12%  | 433804.00    | 13.96%     | 100917.00    | 29.64%     |
| Single cells... | 222,453 | 97.57%   | 37.19%  | 133307.00    | 13.63%     | 100091.00    | 29.09%     |
| Live/Dead       | 212,474 | 95.51%   | 35.52%  | 134238.00    | 12.97%     | 9700.00      | 29.27%     |
| CD19+ Dump-     | 55,885  | 26.30%   | 9.34%   | 131386.00    | 13.34%     | 93086.00     | 27.69%     |
| Naive gD+       | 34,745  | 56.80%   | 5.31%   | 127549.00    | 10.25%     | 88501.00     | 24.60%     |
| Memory IgD-     | 22,496  | 40.25%   | 3.76%   | 14152450     | 15.79%     | 102606.00    | 30.31%     |
| IgD- KO-        | 17,409  | 77.39%   | 2.91%   | 144624.00    | 14.88%     | 107966.00    | 28.93%     |
| P15-1           | 2,663   | 15.30%   | 0.45%   | 163750.00    | 11.93%     | 130908.00    | 26.18%     |
| P15-2           | 5       | 0.03%    | 0.00%   | 166073.00    | 5.07%      | 160211.00    | 6.57%      |
| P15-3           | 14,736  | 84.65%   | 2.46%   | 14126450     | 14.20%     | 103995.00    | 28.13%     |
| P15-4           | 5       | 0.03%    | 0.00%   | 162803.00    | 6.04%      | 156540.00    | 9.02%      |
| MARIO WT++      | 0       | 0.00%    | 0.00%   |              |            |              |            |
| P14-1           | 8,888   | 39.51%   | 1.49%   | 431473.00    | 15.37%     | 90965.50     | 28.65%     |
| P14-2           | 1,806   | 8.03%    | 0.30%   | 153347.00    | 12.19%     | 121119.50    | 24.60%     |
| P14-3           | 4896    | 21.76%   | 0.82%   | 141244.00    | 16.41%     | 101527.00    | 30.63%     |
| P14-4           | 6,906   | 30.70%   | 1.15%   | 147753.00    | 12.13%     | 113108.50    | 25.94%     |

## License

[![License](https://img.shields.io/github/license/tmsincomb/ImageToCSV)](https://opensource.org/licenses/MIT)

- Copyright © Troy M. Sincomb
