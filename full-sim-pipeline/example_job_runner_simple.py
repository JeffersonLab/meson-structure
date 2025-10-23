#!/usr/bin/env python3
"""
example_minimal.py

Minimal working example of using JobRunner.
This demonstrates the simplest possible use case.
"""

import os
from job_runner import JobRunner


def main():
    """Minimal example of JobRunner usage."""
    
    # Define how output files are named based on input files
    def output_name(input_file, output_dir):
        """Convert input.dat -> input.out in the output directory."""
        basename = os.path.basename(input_file).replace('.dat', '.out')
        return os.path.join(output_dir, basename)
    
    # Create some example input files for demonstration
    input_files = [
        '/data/input/sample1.dat',
        '/data/input/sample2.dat',
        '/data/input/sample3.dat'
    ]
    
    # Create runner with minimal required parameters
    runner = JobRunner(
        input_files=input_files,
        output_file_name_func=output_name,
        output_dir='/data/output',
        bind_dirs=['/data', '/home']  # Directories to mount in container
    )
    
    # Set the job template - this is what runs inside the container
    # All {variable} placeholders will be replaced with actual values
    runner.container_job_template = '''#!/bin/bash
set -e

echo "=========================================="
echo "Processing: {basename}"
echo "=========================================="
echo "Input:  {input_file}"
echo "Output: {output_file}"
echo "Events: {events}"
echo ""

# Your actual processing command here
# For example:
my_analysis_program \\
    --input {input_file} \\
    --output {output_file} \\
    --nevents {events}

echo "Job completed successfully!"
'''
    
    # Generate all scripts (container scripts, SLURM scripts, etc.)
    runner.run()
    
    print("\n✅ Job scripts generated successfully!")
    print("Check the output directory for generated scripts.")


if __name__ == "__main__":
    main()