import os
import re

# Grab total energy dan free energy correction from ORCA output that ran by run.py
# Free energy corrections are taken from result.log
# SPC for B3LYP and PBE0 are taken from B3LYPsp.property.txt and PBE0sp.property.txt

output_file = "energy.dat"

with open(output_file, "w") as out:
    out.write(f"{'Folder':<8} {'G-E(el)_Eh':>20} {'B3LYP_E':>20} {'PBE0_E':>20}\n")

    for i in range(1, 41):
        folder = str(i)
        path = os.path.join(os.getcwd(), folder)

        # Inisialisasi
        ge_el = b3lyp_energy = pbe0_energy = "NaN"

        # result.log
        result_path = os.path.join(path, "result.log")
        if os.path.exists(result_path):
            with open(result_path, "r") as f:
                for line in f:
                    if "G-E(el)" in line:
                        match = re.search(r"G-E\(el\).*?([+-]?\d*\.\d+)\s+Eh", line)
                        if match:
                            ge_el = float(match.group(1))
                            break

        # B3LYPsp.property.txt
        b3lyp_path = os.path.join(path, "B3LYPsp.property.txt")
        if os.path.exists(b3lyp_path):
            with open(b3lyp_path, "r") as f:
                for line in f:
                    if "&TOTALENERGY [&Type \"Double\"]" in line:
                        match = re.search(r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", line)
                        if match:
                            b3lyp_energy = float(match.group(1))
                            break

        # PBE0sp.property.txt
        pbe0_path = os.path.join(path, "PBE0sp.property.txt")
        if os.path.exists(pbe0_path):
            with open(pbe0_path, "r") as f:
                for line in f:
                    if "&TOTALENERGY [&Type \"Double\"]" in line:
                        match = re.search(r"([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", line)
                        if match:
                            pbe0_energy = float(match.group(1))
                            break

        # Tulis ke file
        out.write(f"{folder:<8} {ge_el:>20} {b3lyp_energy:>20} {pbe0_energy:>20}\n")
