from pathlib import Path
import pandas as pd
from preprocessing import (interpolate_csv)

# Configuration

INPUT_DATASET = Path("../Dataset")
OUTPUT_DATASET = Path("../prepared_dataset")


def prepare_csv(input_file: Path, output_file: Path):

    # Load
    df = pd.read_csv(input_file)

    # Preprocess
    df = interpolate_csv(df)

    # Create destination folder
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save
    df.to_csv(output_file, index=False)


def main():

    csv_files = sorted(INPUT_DATASET.rglob("*.csv"))

    print(f"Found {len(csv_files)} CSV files.\n")

    for i, csv_file in enumerate(csv_files, start=1):

        relative_path = csv_file.relative_to(INPUT_DATASET)
        destination = OUTPUT_DATASET / relative_path

        print(
            f"[{i}/{len(csv_files)}] "
            f"{relative_path}"
        )

        prepare_csv(csv_file, destination)

    print("\nDataset preparation complete!")


if __name__ == "__main__":
    main()