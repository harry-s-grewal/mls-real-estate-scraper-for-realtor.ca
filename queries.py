""" Contains all queries to Realtor.ca using undetected-chromedriver. """
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


def scrape_property_list(city, max_pages=1):
    """Scrapes properties from Realtor.ca for a given city.
    
    Args:
        city: City name (e.g., "Toronto, ON")
        max_pages: Maximum number of pages to scrape (default: 1)
    
    Returns:
        List of property dictionaries
    """
    
    properties = []
    driver = None
    
    try:
        print("🚀 Starting undetected Chrome browser...")
        driver = uc.Chrome(version_main=145)
        
        # TODO: Add your navigation logic here
        # Example:
        driver.get("https://www.realtor.ca")
        # time.sleep(5)        
        # Navigate to realtor.ca
        print("📄 Loading realtor.ca...")
        driver.get("https://www.realtor.ca")
        time.sleep(5)
        
        # Wait for search bar to load and interact with it
        print("🔍 Looking for search bar...")
        search_box = driver.find_element(By.XPATH, "//*[@id='homeSearchTxt']")
        print("✓ Found search bar")
        
        # Click on the search box and type
        search_box.click()
        time.sleep(1)
        search_box.send_keys("toronto on")
        print("✓ Typed 'toronto on'")
        
        # Press down arrow
        search_box.send_keys(Keys.DOWN)
        print("✓ Pressed down arrow")
        time.sleep(1)
        
        # Press Enter
        search_box.send_keys(Keys.RETURN)
        print("✓ Pressed Enter")
        time.sleep(5)        
        for page in range(1, max_pages + 1):
            print(f"\n📄 Processing page {page}...")
            
            try:
                # Wait for page to load
                time.sleep(3)
                
                # Get the rendered HTML
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Find all property cards
                property_cards = soup.find_all('div', class_='smallListingCard')
                
                if not property_cards:
                    print(f"⚠ No properties found on page {page}")
                    break
                
                print(f"✓ Found {len(property_cards)} properties on page {page}")
                
                # Extract property information from each card
                for idx, card in enumerate(property_cards, 1):
                    try:
                        # Extract address
                        address_elem = card.find('div', class_='smallListingCardAddress')
                        address = address_elem.get_text(strip=True) if address_elem else "N/A"
                        
                        # Extract price
                        price_elem = card.find('div', class_='smallListingCardPrice')
                        price = price_elem.get_text(strip=True) if price_elem else "N/A"
                        
                        # Extract bedroom, bathroom, sqft (from icon numbers)
                        icon_nums = card.find_all('div', class_='smallListingCardIconNum')
                        bedrooms = icon_nums[0].get_text(strip=True) if len(icon_nums) > 0 else "N/A"
                        bathrooms = icon_nums[1].get_text(strip=True) if len(icon_nums) > 1 else "N/A"
                        sqft = icon_nums[2].get_text(strip=True) if len(icon_nums) > 2 else "N/A"
                        
                        # Extract link
                        link_elem = card.find('a', class_='blockLink')
                        link = link_elem.get('href') if link_elem else "N/A"
                        full_link = link if link.startswith('http') else f"https://www.realtor.ca{link}"
                        
                        # Extract MLS number
                        mls_elem = card.find('div', class_='smallListingCardMLSVal')
                        mls = mls_elem.get_text(strip=True) if mls_elem else "N/A"
                        
                        properties.append({
                            "Address": address,
                            "Bedrooms": bedrooms,
                            "Bathrooms": bathrooms,
                            "SquareFootage": sqft,
                            "Price": price,
                            "MLS": mls,
                            "Link": full_link
                        })
                        
                    except Exception as e:
                        print(f"⚠ Error extracting property {idx}: {e}")
                        continue
                
                # Click next page button if there are more pages
                if page < max_pages:
                    try:
                        print(f"\n⏳ Going to page {page + 1}...")
                        next_button = driver.find_element(By.CLASS_NAME, "lnkNextResultsPage")
                        next_button.click()
                        time.sleep(8)  # Wait longer for next page to load
                    except Exception as e:
                        print(f"⚠ No next page button found: {e}")
                        break
                
            except Exception as e:
                print(f"❌ Error processing page {page}: {e}")
                if page == 1:
                    break
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            print("\n🛑 Closing browser...")
            driver.quit()
    
    return properties
