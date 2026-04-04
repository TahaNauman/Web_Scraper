def main():
    urls = input("Enter URLs separated by commas: ").split(",")
    urls = [url.strip() for url in urls]

    combined_results = {}

    for url in urls:
        html = fetch_page(url)
        if html:

            tags = get_all_tags(html)

            print("\n Available Tags:")
            print(", ".join(tags))

            selected_tags = input("Enter comma-separated tags to extract: ").split(",")
            selected_tags = [tag.strip() for tag in selected_tags]


            extracted = extract_tags(html, selected_tags)
            # Combine results
            for tag, items in extracted.items():
                if tag not in combined_results:
                    combined_results[tag] = []
                combined_results[tag].extend(items)

    save_data(combined_results, filename="output.json", save_csv=True)

  

# Run script
if __name__ == "__main__":
    main()
