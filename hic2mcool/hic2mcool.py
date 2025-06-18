'''
MIT License

Copyright (c) 2025 Brydon Wall

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import numpy as np
import hicstraw
import os
import pandas as pd
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import tempfile
import cooler
import h5py
import shutil

def get_cool(
    cool_path,
    hic_path,
    data_type,
    normalization,
    resolution,
    temp_dir = None
) -> None:
    
    hic = hicstraw.HiCFile(hic_path)
    
    # First write the chromosome sizes:
    chr_sizes = pd.Series(
        {chromosome.name: chromosome.length for chromosome in hic.getChromosomes() if chromosome.name != "All"}
    )
    with tempfile.NamedTemporaryFile(mode='w', dir=temp_dir, delete=False) as genome_file:
        for chromosome in hic.getChromosomes():
            if chromosome.name != "All":
                genome_file.write(f"{chromosome.name}\t{chromosome.length}\n")
    
    # Then write the counts in text file:
    with tempfile.NamedTemporaryFile(mode='w', dir=temp_dir, delete=False) as cool_temp_file:
        for i in range(len(chr_sizes)):
            for j in range(i, len(chr_sizes)):
                chr_1 = chr_sizes.index[i]
                chr_2 = chr_sizes.index[j]
                result = hicstraw.straw(data_type, normalization, hic_path, chr_1, chr_2, 'BP', resolution)
                for k in range(len(result)):
                    start_1 = result[k].binX
                    start_2 = result[k].binY
                    value = result[k].counts
                    cool_temp_file.write(
                        f"{chr_1}\t{start_1}\t{start_1}\t{chr_2}\t{start_2}\t{start_2}\t{value}\n"
                    )

    # Run cooler to generate .cool file
    command = f'cooler load -f bg2 --count-as-float "{genome_file.name}:{resolution}" "{cool_temp_file.name}" "{cool_path}"'
    print(command)
    os.system(command)
    os.remove(genome_file.name)
    os.remove(cool_temp_file.name)

def main():
    parser = argparse.ArgumentParser(description="Convert .hic to .mcool format using hicstraw and cooler.")
    parser.add_argument('--hic_file', type=str, required=True, help='Input .hic file')
    parser.add_argument('--mcool_file', type=str, required=True, help='Output .mcool file')
    parser.add_argument('--data_type', type=str, default='observed', help='Type of data to extract ("observed", "oe"); default: "observed"')
    parser.add_argument('--normalization', type=str, default='NONE', help='Normalization method: NONE, VC, VC_SQRT, KR, SCALE, etc; default: "NONE"')
    parser.add_argument('--temp_dir', type=str, default=None, help='Specify a temporoary directory location, otherwise system default is used.')

    args = parser.parse_args()

    hic_path = args.hic_file
    mcool_file = args.mcool_file
    data_type = args.data_type
    normalization = args.normalization
    temp_path = args.temp_dir

    hic = hicstraw.HiCFile(hic_path)
    resolutions = [res for res in hic.getResolutions()]

    with tempfile.TemporaryDirectory(dir = temp_path) as temp_dir:
        with ProcessPoolExecutor() as executor:

            cool_paths = {}
            futures = []
            for resolution in resolutions:
                cool_path = f"{temp_dir}/cool_{resolution}.cool"
                cool_paths[resolution] = cool_path
                future = executor.submit(
                    get_cool,
                    cool_path=cool_path,
                    hic_path=hic_path,
                    data_type=data_type,
                    normalization=normalization,
                    resolution=resolution,
                    temp_dir=temp_dir
                )
                futures.append(future)

            # Collect results
            results = []
            for future in as_completed(futures):
                result = future.result()  # or handle exceptions with try/except
                results.append(result)

        # Copy the highest resolution file as the base
        shutil.copyfile(cool_paths[min(cool_paths.keys())], mcool_file)

        # Add the other resolutions into the .mcool file under /resolutions/{resolution}
        with h5py.File(mcool_file, 'a') as out:
            for res, path in cool_paths.items():
                if res == min(cool_paths.keys()):
                    continue  # already copied
                group = f'resolutions/{res}'
                out.copy(h5py.File(path, 'r')['/'], group)

if __name__ == "__main__":
    main()
