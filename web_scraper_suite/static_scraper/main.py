from fetcher import fetch_page
from parser import get_all_tags, extract_tags, find_next_page
from saver import save_data

def main():
    # Setup Inputs
    urls_input = input("Enter starting URLs separated by commas: ").split(",")
    urls = [url.strip() for url in urls_input]
    
    try:
        max_pages = int(input("Enter max pages to scrape per URL (default 1): ") or 1)
    except ValueError:
        max_pages = 1

    combined_results = {}

    # Outer Loop: Iterate through each starting URL provided
    for start_url in urls:
        current_url = start_url
        pages_count = 0
        selected_tags = []

        # Inner Loop: Handle Pagination 
        while current_url and pages_count < max_pages:
            print(f"\nScraping Page {pages_count + 1}: {current_url}")

            referer_url = None if pages_count == 0 else current_url
            
            # Fetch HTML (Pass referer if it's not the first page)
            html = fetch_page(current_url, referer=referer_url)
            
            if not html:
                break
            
            # Identify tags only on the very first page of a domain
            if pages_count == 0:
                available_tags = get_all_tags(html)
                print(f"Available Tags: {', '.join(available_tags)}")
                tag_input = input("Select tags to extract (e.g., h1, p, img, a): ").split(",")
                selected_tags = [t.strip() for t in tag_input]

            #Extract Data (Passing current_url as the base for relative links)
            extracted = extract_tags(html, selected_tags, current_url)
            
            # Merge findings into combined_results
            for tag, items in extracted.items():
                if tag not in combined_results:
                    combined_results[tag] = []
                combined_results[tag].extend(items)
            
            #Look for 'Next' page URL
            next_url = find_next_page(html, current_url)
            
            # Increment the count 
            pages_count += 1
            
            # Check if we have a next URL AND if we are still under the limit
            if next_url and pages_count < max_pages:
                # Avoid infinite loops if 'Next' points to itself
                if next_url == current_url:
                    current_url = None
                else:
                    current_url = next_url
                    print(f"Next page found. Moving to Page {pages_count + 1}...")
            else:
                # Stop the loop: either no next page exists, or we hit the max_pages limit
                current_url = None
    #Final Export
    if combined_results:
        save_data(combined_results, filename="output.json", save_csv=True)
        print("\nScraping Task Complete!")
    else:
        print("\nNo data was extracted. Check your URLs or robots.txt permissions.")

if __name__ == "__main__":
    main()
