import json
import csv
import logging

logger = logging.getLogger(__name__)

def save_data(data, filename="output.json", save_csv=False, deduplicate=False):
    if deduplicate:
        for tag in data:
            original = data[tag]
            if isinstance(original, list):
                seen = set()
                unique = []
                for item in original:
                    if isinstance(item, dict):
                        key = (item.get("label", ""), item.get("url", ""))
                    else:
                        key = item
                    if key not in seen:
                        seen.add(key)
                        unique.append(item)
                data[tag] = unique
        logger.info("Deduplication applied to extracted data")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logger.info(f"JSON data saved to {filename}")

    if save_csv:
        csv_filename = filename.replace(".json", ".csv")
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tag Type", "Text/Label", "URL/Attribute"])
            
            for tag, items in data.items():
                for item in items:
                    if isinstance(item, dict):
                        label = item.get("label", "")
                        url = item.get("url", "")
                        writer.writerow([tag, label, url])
                    else:
                        writer.writerow([tag, item, "N/A"])
                        
        logger.info(f"CSV data saved to {csv_filename}")
