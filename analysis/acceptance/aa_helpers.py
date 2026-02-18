#!/usr/bin/env python3
"""
EIC Center Forward Plotting and Data Processing Utility

This module provides functions for:
1. Creating plots with calibrated background images (pixel to mm conversion)
2. Converting and concatenating CSV files to Feather format with unique event IDs
"""

import argparse
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import glob
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Default configuration for background image and calibration points
DEFAULT_BCK_IMAGE = "eic_center_forward_bw.png"

# Default calibration points for pixel-to-millimeter conversion
# Format: Two correspondence points mapping (x_mm, y_mm) <-> (x_pixel, y_pixel)
DEFAULT_BCK_SCALE_POINTS = [
    {"mm": {"x": 0.0, "y": 0.0}, "pixel": {"x": 371.0, "y": 281.0}},
    {"mm": {"x": 4937.0, "y": 2622.0}, "pixel": {"x": 739.0, "y": 85.0}}
]


def create_plot_with_background(
        figsize: Tuple[int, int] = (20, 10),
        bck_image: str = DEFAULT_BCK_IMAGE,
        bck_scale_points: List[Dict] = DEFAULT_BCK_SCALE_POINTS
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create a matplotlib plot with a calibrated background image.

    This function loads an image and sets up a coordinate system where the image
    pixels are mapped to physical millimeter coordinates using two calibration points.

    Parameters
    ----------
    figsize : tuple of int, optional
        Figure size in inches (width, height). Default is (20, 10).
    bck_image : str, optional
        Path to the background image file. Default is "eic_center_forward.png".
    bck_scale_points : list of dict, optional
        Two calibration points for pixel-to-mm conversion. Each point should have
        the structure: {"mm": {"x": x_mm, "y": y_mm}, "pixel": {"x": x_px, "y": y_px}}

    Returns
    -------
    fig : matplotlib.figure.Figure
        The created figure object
    ax : matplotlib.axes.Axes
        The axes object with the calibrated background image

    Raises
    ------
    FileNotFoundError
        If the background image file cannot be found
    ValueError
        If calibration points are invalid

    Examples
    --------
    >>> fig, ax = create_plot_with_background()
    >>> ax.plot([0, 1000], [0, 500], 'r-')  # Plot in mm coordinates
    >>> plt.show()
    """
    # Extract calibration points
    p0 = bck_scale_points[0]
    p1 = bck_scale_points[1]

    p0_x_mm = p0["mm"]["x"]
    p0_y_mm = p0["mm"]["y"]
    p0_x_pixel = p0["pixel"]["x"]
    p0_y_pixel = p0["pixel"]["y"]

    p1_x_mm = p1["mm"]["x"]
    p1_y_mm = p1["mm"]["y"]
    p1_x_pixel = p1["pixel"]["x"]
    p1_y_pixel = p1["pixel"]["y"]

    # Calculate linear transformation coefficients
    # Linear mapping: coord_mm = scale * coord_pixel + offset
    x_scale = (p1_x_mm - p0_x_mm) / (p1_x_pixel - p0_x_pixel)
    x_offset = p0_x_mm - x_scale * p0_x_pixel

    y_scale = (p1_y_mm - p0_y_mm) / (p1_y_pixel - p0_y_pixel)
    y_offset = p0_y_mm - y_scale * p0_y_pixel  # note: y_scale will often be negative

    def pixel_to_mm_x(x_pixel: float) -> float:
        """Convert x-coordinate from pixels to millimeters."""
        return x_scale * x_pixel + x_offset

    def pixel_to_mm_y(y_pixel: float) -> float:
        """Convert y-coordinate from pixels to millimeters."""
        return y_scale * y_pixel + y_offset

    # Load image
    try:
        image = mpimg.imread(bck_image)
    except FileNotFoundError:
        raise FileNotFoundError(f"Background image not found: {bck_image}")

    height_pixel, width_pixel = image.shape[:2]

    # Calculate image extent in millimeters (left, right, bottom, top)
    left_mm = pixel_to_mm_x(0)
    right_mm = pixel_to_mm_x(width_pixel)
    top_mm = pixel_to_mm_y(0)  # origin='upper' => row 0 is the top
    bottom_mm = pixel_to_mm_y(height_pixel)

    # Create plot with calibrated background
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(
        image,
        extent=(left_mm, right_mm, bottom_mm, top_mm),
        origin="upper",
        interpolation="nearest",
    )

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_title("EIC Center Forward View")

    return fig, ax


def concat_csvs_with_unique_events(files: List[str]) -> pd.DataFrame:
    """
    Load and concatenate multiple CSV files with globally unique event IDs.

    This function reads multiple CSV files and concatenates them into a single
    DataFrame. Event IDs are adjusted to ensure they remain globally unique
    across all files by adding an offset based on the maximum event ID from
    previous files.

    Parameters
    ----------
    files : list of str
        List of paths to CSV files to concatenate

    Returns
    -------
    pd.DataFrame
        Concatenated DataFrame with unique event IDs

    Raises
    ------
    ValueError
        If no files are provided
    FileNotFoundError
        If any of the CSV files cannot be found

    Examples
    --------
    >>> files = ['data1.csv', 'data2.csv', 'data3.csv']
    >>> df = concat_csvs_with_unique_events(files)
    >>> print(f"Total events: {len(df['event'].unique())}")
    """
    if not files:
        raise ValueError("No files provided for concatenation")

    dfs = []
    offset = 0

    for file in files:
        try:
            df = pd.read_csv(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {file}")
        except Exception as e:
            raise ValueError(f"Error reading CSV file {file}: {e}")

        if 'event' not in df.columns:
            raise ValueError(f"CSV file {file} does not contain an 'event' column")

        # Adjust event IDs to ensure global uniqueness
        df['event'] = df['event'] + offset
        offset = df['event'].max() + 1  # Set offset for next file

        dfs.append(df)
        print(f"Loaded {len(df)} rows from {file} (events {df['event'].min()}-{df['event'].max()})")

    # Concatenate all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Total: {len(combined_df)} rows with {len(combined_df['event'].unique())} unique events")

    return combined_df


def convert_to_feather(
        input_files: List[str],
        output_file: str,
        use_glob: bool = False
) -> pd.DataFrame:
    """
    Convert CSV files to Feather format with unique event IDs.

    This function can either process a list of specific files or use glob patterns
    to find files. The resulting DataFrame is saved in Feather format for faster
    loading in future operations.

    Parameters
    ----------
    input_files : list of str
        List of file paths or glob patterns (if use_glob=True)
    output_file : str
        Path for the output Feather file
    use_glob : bool, optional
        If True, treat input_files as glob patterns. Default is False.

    Returns
    -------
    pd.DataFrame
        The concatenated DataFrame that was saved to Feather format

    Raises
    ------
    ValueError
        If no files are found or provided

    Examples
    --------
    >>> # Using specific files
    >>> df = convert_to_feather(['file1.csv', 'file2.csv'], 'output.feather')

    >>> # Using glob pattern
    >>> df = convert_to_feather(['data/*.csv'], 'output.feather', use_glob=True)
    """
    if use_glob:
        # Expand glob patterns
        all_files = []
        for pattern in input_files:
            matched_files = sorted(glob.glob(pattern))
            if matched_files:
                all_files.extend(matched_files)
                print(f"Pattern '{pattern}' matched {len(matched_files)} files")
            else:
                print(f"Warning: Pattern '{pattern}' matched no files")
        files = all_files
    else:
        # Use files as-is
        files = input_files

    if len(files) == 0:
        raise ValueError("No files to process")

    print(f"\nProcessing {len(files)} CSV files...")

    # Concatenate CSVs with unique events
    df = concat_csvs_with_unique_events(files)

    # Save to Feather format
    df.to_feather(output_file)
    print(f"\nSaved {len(df)} rows to {output_file}")

    return df


def main():
    """
    Provides functionality to convert CSV files to Feather format with proper
    event ID handling. Supports both explicit file lists and glob patterns.
    """
    parser = argparse.ArgumentParser(
        description="Convert CSV files to Feather format with unique event IDs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert specific files
  %(prog)s file1.csv file2.csv file3.csv -o output.feather

  # Use glob pattern (quotes are important!)
  %(prog)s "data/*.csv" -o output.feather --glob

  # Multiple glob patterns
  %(prog)s "data1/*.csv" "data2/*.csv" -o output.feather --glob

  # Mix of patterns with glob
  %(prog)s "run1_*.csv" "run2_*.csv" -o combined.feather --glob
        """
    )

    parser.add_argument('input_files', nargs='+', help='Input CSV files or glob patterns (when using --glob)')
    parser.add_argument('-o', '--output', required=True, help='Output Feather file path')
    parser.add_argument('--glob', action='store_true', help='Treat input arguments as glob patterns')
    parser.add_argument('-v', '--verbose', action='store_true',  help='Enable verbose output')
    args = parser.parse_args()

    try:
        # Convert files to Feather format
        df = convert_to_feather(
            input_files=args.input_files,
            output_file=args.output,
            use_glob=args.glob
        )

        if args.verbose:
            print("\nDataFrame info:")
            print(df.info())
            print("\nFirst few rows:")
            print(df.head())

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nConversion complete! Output saved to: {args.output}")


if __name__ == "__main__":
    main()