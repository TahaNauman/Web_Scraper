import json
import csv

def save_data(data, filename="output.json", save_csv=False):
    # Save JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"JSON data saved to {filename}")

    # Save CSV
    if save_csv:
        csv_filename = filename.replace(".json", ".csv")
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Write a Header Row
            writer.writerow(["Tag Type", "Text/Label", "URL/Attribute"])
            
            for tag, items in data.items():
                for item in items:
                    # Check if the item is a dictionary (like our <a> or <img> tags)
                    if isinstance(item, dict):
                        # Extract the label and the absolute URL we generated
                        label = item.get("label", "")
                        url = item.get("url", "")
                        writer.writerow([tag, label, url])
                    else:
                        # It's just a regular string (like a <p> or <h1> tag)
                        writer.writerow([tag, item, "N/A"])
                        
        print(f"CSV data saved to {csv_filename}")
