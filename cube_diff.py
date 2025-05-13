import numpy as np

def read_cube_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    header = lines[:6]

    # Ambil info grid dan jumlah atom
    natoms_line = lines[2]
    natoms = abs(int(natoms_line.split()[0]))
    nx = int(lines[3].split()[0])
    ny = int(lines[4].split()[0])
    nz = int(lines[5].split()[0])

    # Ambil baris atom
    atom_lines = lines[6:6 + natoms]

    # Ambil data grid
    data_lines = lines[6 + natoms:]
    data_str = ' '.join(data_lines).split()
    data = np.array(data_str, dtype=float)

    total_grid = nx * ny * nz
    if len(data) > total_grid:
        print(f"Warning: trimming {len(data) - total_grid} extra data points.")
        data = data[:total_grid]
    elif len(data) < total_grid:
        raise ValueError(f"Data too short: only {len(data)} values for grid size {total_grid}")

    data = data.reshape((nx, ny, nz))
    return header, atom_lines, data

def write_cube_file(filename, header, atom_lines, data):
    with open(filename, 'w') as f:
        for line in header:
            f.write(line)
        
        for atom in atom_lines:
            f.write(atom)
        
        # Add the "1 putra" line before grid data
        f.write("1 8494\n")
        
        # Flatten and format: max 6 values per line
        flat_data = data.flatten()
        for i in range(0, len(flat_data), 6):
            line = ''.join(f"{val:13.5E}" for val in flat_data[i:i+6])
            f.write(line + '\n')

def validate_compatibility(header1, atoms1, data1, header2, atoms2, data2):
    if data1.shape != data2.shape:
        raise ValueError(f"Incompatible grid shapes: {data1.shape} vs {data2.shape}")

    if atoms1 != atoms2:
        raise ValueError("Atom definitions in cube files do not match.")

    if header1[:2] != header2[:2]:
        print("Warning: Cube file headers (comments) differ. Proceeding anyway.")

def main(file1, file2, output_file):
    print(f"Reading: {file1}")
    header1, atom_lines1, data1 = read_cube_file(file1)

    print(f"Reading: {file2}")
    header2, atom_lines2, data2 = read_cube_file(file2)

    print("Validating compatibility...")
    validate_compatibility(header1, atom_lines1, data1, header2, atom_lines2, data2)

    print("Calculating a^2 - b^2 difference...")
    diff_squared = data1**2 - data2**2

    print(f"Writing output: {output_file}")
    write_cube_file(output_file, header1, atom_lines1, diff_squared)

    print("Done.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python cube_diff_squared.py file1.cube file2.cube output.cube")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
