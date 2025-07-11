import os
import subprocess
import csv

# Running DFT simulation for one molecule with different solvent, which are listed in 'listed_solvent.csv'
# Step:
# 1. Create the folder if it doesn't exist
# 2. Change to the specified folder and create the input file
# 3. Write the custom ORCA input file with the correct charge and dielectric
# 4. Run the ORCA command
# 5. Go back to the parent directory

# File path for the CSV file
file_path = 'listed_solvent.csv'

# Open the CSV file and read its contents
with open(file_path, mode='r') as file:
    csv_reader = csv.DictReader(file, delimiter=';')

    # Loop through each row in the CSV file
    for row in csv_reader:
        folder = row['No']
        solvent = row['Keyword']

        # Define the result file name for ORCA output
        result_file = 'result.log'

        # Command to run ORCA (adjust based on your ORCA installation and setup)
        orca_command = f"$ORCA_BIN_DIR/orca input.inp > {result_file}"

        # Prepare the m062x.inp content for ORCA
        orca_input_content = f"""! M06L def2-SVP OPT FREQ UKS

%base "results"
%pal
nprocs 16
end

%cpcm
smd true
SMDSolvent "{solvent}"
end

*xyzfile 0 1 geom.xyz 

$new_job

! B3LYP D3BJ def2-TZVP UKS
%base"B3LYPsp"

%cpcm
smd true
SMDSolvent "{solvent}"
end

*xyzfile 0 1 results.xyz

$new_job

! PBE0 D3BJ def2-TZVP UKS
%base"PBE0sp"

%cpcm
smd true
SMDSolvent "{solvent}"
end

*xyzfile 0 1 results.xyz

"""

        # Create the folder if it doesn't exist
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print(f"Created folder: {folder}")
            except Exception as e:
                print(f"Error creating folder {folder}: {e}")
                continue  # Skip this folder if there was an issue creating it

        # Change to the specified folder and create the input file
        try:
            os.chdir(folder)
            print(f"Checking folder {folder}...")

            # Check if result.out exists and contains "* finished run on"
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    result_content = f.read()
                if "* finished run on" in result_content:
                    print(f"Skipping folder {folder} as result.out already contains '* finished run on'.")
                    os.chdir('..')  # Go back to the parent directory
                    continue  # Skip the calculation for this folder

            # Write the custom ORCA input file with the correct charge and dielectric
            with open('input.inp', 'w') as f:
                f.write(orca_input_content)

            # Run the ORCA command
            print(f"Running in folder {folder}: {orca_command}")
            subprocess.run(orca_command, shell=True, check=True)

            # Go back to the parent directory
            os.chdir('..')  # Return to the parent directory

        except FileNotFoundError:
            print(f"Folder {folder} not found or dft.xyz missing!")
            os.chdir('..')  # Go back to the parent directory in case of error
        except subprocess.CalledProcessError as e:
            print(f"Error running ORCA command in folder {folder}: {e}")
            os.chdir('..')  # Go back to the parent directory in case of error
        except Exception as e:
            print(f"Unexpected error in folder {folder}: {e}")
            os.chdir('..')  # Go back to the parent directory in case of error
