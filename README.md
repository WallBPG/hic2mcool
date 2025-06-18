# hic2mcool

A command-line utility for converting .hic to .mcool files.

# Installation

Install via pip:
```bash
pip install hic2mcool
```

# Usage

```
usage: hic2mcool [-h] --hic_file HIC_FILE --mcool_file MCOOL_FILE [--data_type DATA_TYPE] [--normalization NORMALIZATION] [--temp_dir TEMP_DIR]

Convert .hic to .mcool format using hicstraw and cooler.

optional arguments:
  -h, --help            show this help message and exit
  --hic_file HIC_FILE   Input .hic file
  --mcool_file MCOOL_FILE
                        Output .mcool file
  --data_type DATA_TYPE
                        Type of data to extract ("observed", "oe"); default: "observed"
  --normalization NORMALIZATION
                        Normalization method: NONE, VC, VC_SQRT, KR, SCALE, etc; default: "NONE"
  --temp_dir TEMP_DIR   Specify a temporoary directory location, otherwise system default is used.
```
