import json
import csv

def save_data(data, filename="output.json", save_csv=False):
    # Save JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"JSON data saved to {filename}")

    # Optionally save CSV
    if save_csv:
        csv_filename = filename.replace(".json", ".csv")
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Assuming data is dict of lists
            for tag, values in data.items():
                for val in values:
                    writer.writerow([tag, val])
        print(f"CSV data saved to {csv_filename}")
