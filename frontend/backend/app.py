from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import traceback
import re
import time
from urllib.parse import quote_plus
import os

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Selenium WebDriver Setup ---
def create_driver():
    """Creates and configures a headless Selenium WebDriver instance."""
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Enhanced anti-bot detection measures
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Use local chromedriver path instead of webdriver-manager
        chromedriver_path = r"C:\Users\ksasw\OneDrive - vitap.ac.in\Android Dev Hackathon\chromedriver-win64\chromedriver.exe"
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        # Additional bot detection evasion
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        print("ChromeDriver is set up and running.")
        return driver
    except Exception as e:
        print(f"FATAL: Could not create Chrome driver: {e}")
        raise

# --- Helper Functions for Scraping ---
def extract_price(element_container, selectors, site_name):
    """A generic function to extract and clean a price from a web element."""
    for selector in selectors:
        try:
            price_elem = element_container.find_element(By.CSS_SELECTOR, selector)
            price_text = price_elem.get_attribute("innerHTML") or price_elem.text
            print(f"DEBUG: Found price element with text: '{price_text}' using selector: '{selector}'")
            
            # Enhanced price cleaning - handle Indian rupee symbols and commas
            cleaned_price = re.sub(r'[₹,\s]', '', price_text)  # Remove ₹, commas, spaces
            cleaned_price = re.sub(r'[^\d.]', '', cleaned_price)  # Keep only digits and dots
            
            if cleaned_price:
                try:
                    price_value = float(cleaned_price)
                    print(f"DEBUG: Successfully extracted price: {price_value}")
                    return price_value
                except ValueError:
                    continue
        except (NoSuchElementException, AttributeError, ValueError) as e:
            print(f"DEBUG: Selector '{selector}' failed: {e}")
            continue
    print(f"Warning: Could not extract price from {site_name} using selectors: {selectors}")
    return None

def clean_product_name(product_name):
    """Cleans and optimizes the product name for better search results."""
    if not product_name:
        return ""
    
    # Remove common noise words that might interfere with search
    noise_words = ['buy', 'online', 'price', 'cheap', 'discount', 'offer', 'deal', 'sale']
    words = product_name.lower().split()
    
    # Keep meaningful words, remove noise
    filtered_words = [word for word in words if word not in noise_words and len(word) > 2]
    
    # Take first 8 words for comprehensive but focused search
    return ' '.join(filtered_words[:8])

# --- Main Scraping Logic ---
def search_product_on_site(product_name, target_site):
    """Searches for a product on the target site and returns the best result's info."""
    driver = create_driver()
    try:
        time.sleep(1)  # Rate limiting
        wait = WebDriverWait(driver, 15)
        
        cleaned_query = clean_product_name(product_name)
        print(f"Searching for '{cleaned_query}' on {target_site}")
        
        if target_site == 'amazon':
            search_url = f"https://www.amazon.in/s?k={quote_plus(cleaned_query)}"
            driver.get(search_url)
            time.sleep(2)
            
            try:
                # Wait for search results to load
                results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
                    "[data-component-type='s-search-result']")))
                
                # Try to find the best match from first few results
                for container in results[:5]:  # Check first 5 results
                    try:
                        price = extract_price(container, [
                            "span.a-price-whole", 
                            ".a-price .a-offscreen",
                            ".a-price-symbol + .a-price-whole",
                            ".a-price-range .a-price .a-offscreen",
                            "[data-a-color='base'] .a-offscreen",
                            ".a-price.a-text-price.a-size-medium.apexPriceToPay .a-offscreen"
                        ], "Amazon Search")
                        
                        if price:  # If we found a valid price
                            # Find title and link
                            link_elem = container.find_element(By.CSS_SELECTOR, 
                                "h2 a.a-link-normal, .a-size-mini .a-link-normal, .a-size-base-plus")
                            href = link_elem.get_attribute("href")
                            url = href if href.startswith('http') else f"https://www.amazon.in{href}"
                            title = link_elem.text.strip()
                            
                            if url and title:
                                return {
                                    'title': title, 
                                    'price': price, 
                                    'url': url, 
                                    'site': 'amazon',
                                    'site_name': 'Amazon'
                                }
                    except (NoSuchElementException, AttributeError):
                        continue  # Try next result
                        
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error processing Amazon search results: {e}")

        elif target_site == 'flipkart':
            search_url = f"https://www.flipkart.com/search?q={quote_plus(cleaned_query)}"
            driver.get(search_url)
            time.sleep(2)
            
            try:
                # Wait for search results to load
                results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
                    "._1AtVbE, ._4ddWXP, ._13oc-S, .cPHDOP")))
                
                # Try to find the best match from first few results
                for container in results[:5]:  # Check first 5 results
                    try:
                        price = extract_price(container, [
                            "._30jeq3", 
                            "._1_WHN1",
                            ".Nx9bqj",
                            "._3tbKJL",
                            "._25b18c",
                            ".CEmiEU div"
                        ], "Flipkart Search")
                        
                        if price:  # If we found a valid price
                            # Find title and link with more selectors
                            title = "N/A"
                            title_selectors = ["._4rR01T", ".s1Q9rs", "._2WkVRV", ".IRpwTa", ".KzDlHZ", "._2cLu-l"]
                            for title_sel in title_selectors:
                                try:
                                    title_elem = container.find_element(By.CSS_SELECTOR, title_sel)
                                    title = title_elem.text.strip()
                                    if title:
                                        print(f"DEBUG: Found title '{title}' using selector '{title_sel}'")
                                        break
                                except:
                                    continue
                            
                            # Try to get URL
                            url = "N/A"
                            link_selectors = ["a._1fQZEK", "a.s1Q9rs", "a._2rpwqI", "a.IRpwTa", "a._2UzuFa", "a"]
                            for link_sel in link_selectors:
                                try:
                                    link_elem = container.find_element(By.CSS_SELECTOR, link_sel)
                                    href = link_elem.get_attribute("href")
                                    url = href if href.startswith('http') else f"https://www.flipkart.com{href}"
                                    if url != "N/A":
                                        print(f"DEBUG: Found URL using selector '{link_sel}'")
                                        break
                                except:
                                    continue
                            
                            if title != "N/A":  # Only need title, URL is optional
                                return {
                                    'title': title, 
                                    'price': price, 
                                    'url': url, 
                                    'site': 'flipkart',
                                    'site_name': 'Flipkart'
                                }
                            else:
                                print(f"DEBUG: Skipping result - no title found despite having price {price}")
                    except (NoSuchElementException, AttributeError):
                        continue  # Try next result
                        
            except (TimeoutException, NoSuchElementException) as e:
                print(f"Error processing Flipkart search results: {e}")
                
    except Exception as e:
        print(f"Unexpected error searching {target_site}: {e}")
    finally:
        print(f"Closing driver for {target_site} search.")
        driver.quit()
    return None

# --- FLASK ROUTES ---
@app.route("/bestprice", methods=["POST"])
def best_price_endpoint():
    """API endpoint that finds the best price for a product name across sites."""
    try:
        # DEBUG LOGGING
        data = request.get_json()
        print(f"DEBUG: Received data from Express: {data}")
        print(f"DEBUG: Data type: {type(data)}")

        product_name = data.get("productOrUrl", "").strip() if data else ""
        print(f"DEBUG: Extracted product_name: '{product_name}'")

        if not product_name:
            print(f"DEBUG: Product name is empty. Raw data: {data}")
            return jsonify({"error": "Product name cannot be empty."}), 400

        print(f"Step 1: Searching for product: '{product_name}'")
        
        # Search on both sites simultaneously
        all_results = []
        sites = ['amazon', 'flipkart']
        
        for site in sites:
            print(f"Step 2: Searching on {site.title()}...")
            result = search_product_on_site(product_name, site)
            if result:
                all_results.append(result)
                print(f"Found on {site}: {result['title']} - ₹{result['price']}")

        if not all_results:
            print(f"DEBUG: No results found for '{product_name}'")
            return jsonify({
                "success": False,
                "error": f"No products found for '{product_name}' on Amazon or Flipkart. Please try with a different product name.",
                "search_query": product_name
            }), 200  # Changed from 404 to 200
        
        # Find the best deal (lowest price)
        best_deal = min(all_results, key=lambda x: x['price'])
        
        # Calculate savings if multiple results
        savings = 0
        if len(all_results) > 1:
            highest_price = max(all_results, key=lambda x: x['price'])['price']
            savings = highest_price - best_deal['price']
        
        print(f"Step 3: Best deal found on {best_deal['site_name']}: ₹{best_deal['price']}")
        
        return jsonify({
            "success": True,
            "best_site": best_deal['site'],
            "best_site_name": best_deal['site_name'],
            "best_price": best_deal['price'],
            "best_url": best_deal['url'],
            "best_title": best_deal['title'],
            "savings": round(savings, 2) if savings > 0 else 0,
            "total_sites_found": len(all_results),
            "all_results": all_results,
            "search_query": product_name
        })

    except Exception as e:
        print(f"An unexpected server error occurred: {e}")
        traceback.print_exc()
        return jsonify({
            "error": "An internal server error occurred. Please try again later.",
            "details": str(e) if app.debug else None
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "service": "price-comparison-scraper"}), 200

@app.route("/")
def home():
    """Simple home route to fix 404 errors."""
    return jsonify({
        "message": "Price Comparison API",
        "endpoints": {
            "/bestprice": "POST - Search for best product prices",
            "/health": "GET - Health check"
        }
    })

if __name__ == "__main__":
    print("Starting Flask Price Comparison Service...")
    print("Service will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
    #ffff