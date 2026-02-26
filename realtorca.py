""" Selenium-based scraper for realtor.ca properties. """
import os
import pandas as pd
from queries import scrape_property_list


def scrape_properties_by_city(city, max_pages=1):
    """Scrapes properties for a given city and saves them to a CSV file.
    
    Args:
        city: City name (e.g., "Toronto, ON")
        max_pages: Number of pages to scrape (default: 1)
    """
    
    filename = city.replace(" ", "").replace(",", "") + ".csv"
    
    try:
        properties = scrape_property_list(city, max_pages=max_pages)
        
        if not properties:
            print(f"❌ No properties found for {city}")
            return
        
        # Create DataFrame from scraped properties
        results_df = pd.DataFrame(properties)
        
        # Save to CSV
        results_df.to_csv(filename, index=False)
        print(f"\n✅ Successfully scraped {len(properties)} properties for {city}")
        print(f"✅ Data saved to {filename}")
        print(f"\nColumns: {', '.join(results_df.columns)}")
        print(f"\nFirst few rows:")
        print(results_df.head())
        
    except Exception as e:
        print(f"❌ Error occurred while scraping {city}: {e}")


def main():
    """Main entry point for the scraper."""
    
    print("=" * 70)
    print("Realtor.ca Web Scraper (using Selenium)")
    print("=" * 70)
    print("\n⚠️  Requirements:")
    print("  - Chrome or Chromium browser installed")
    print("  - Internet connection")
    print("\n")
    
    # Example: scrape properties in Toronto, ON
    # Modify the city and max_pages as needed
    scrape_properties_by_city("Toronto, ON", max_pages=3)
    
    # You can also scrape multiple cities:
    # cities = ["Toronto, ON", "Vancouver, BC", "Montreal, QC"]
    # for city in cities:
    #     scrape_properties_by_city(city, max_pages=1)
    #     print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()