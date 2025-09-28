# CashTrim Companion

A real-time price comparison web application that helps users find the best deals across major Indian e-commerce platforms (Amazon India & Flipkart).

## Features

- **Multi-Platform Search**: Simultaneously searches Amazon India and Flipkart
- **Real-Time Price Comparison**: Live scraping and instant price comparison
- **Savings Calculator**: Shows how much money you save by choosing the best deal
- **Auto-Redirect**: Automatically redirects to the best price after 3 seconds
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Smart Search**: Intelligent product name cleaning for better results

## Tech Stack

### Backend
- **Flask**: Python web framework for API backend
- **Selenium WebDriver**: Web scraping and browser automation
- **ChromeDriver**: Headless browser for dynamic content extraction

### Frontend
- **HTML5/CSS3**: Modern responsive user interface
- **JavaScript**: Client-side logic and API communication
- **Font Awesome**: Icons and visual elements

### Middleware
- **Express.js**: Node.js server for request routing
- **CORS**: Cross-origin request handling

## Architecture

```
Frontend (HTML/CSS/JS) → Express.js Server → Flask API → Selenium ChromeDriver → E-commerce Sites
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- Chrome browser
- ChromeDriver

### Backend Setup (Flask)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cashtrim-companion.git
cd cashtrim-companion
```

2. Install Python dependencies:
```bash
pip install flask selenium
```

3. Download ChromeDriver:
   - Download from [ChromeDriver Downloads](https://chromedriver.chromium.org/)
   - Extract to a known location
   - Update the path in `app.py`:
```python
chromedriver_path = r"path/to/your/chromedriver.exe"
```

4. Run Flask server:
```bash
python app.py
```
Flask server will start on `http://localhost:5000`

### Frontend Setup (Express.js)

1. Install Node.js dependencies:
```bash
npm install express cors node-fetch
```

2. Run Express server:
```bash
node app.js
```
Express server will start on `http://localhost:3000`

### Access the Application
Open your browser and navigate to `http://localhost:3000`

## Usage

1. Enter a product name in the search box (e.g., "iPhone 15", "Samsung TV", "Nike shoes")
2. Click "Find Best Price" 
3. Wait for the system to search both platforms (10-15 seconds)
4. View the best price found with savings information
5. Get automatically redirected to purchase the item at the best price

## API Endpoints

### Express Server (Port 3000)
- `GET /` - Serves the main HTML interface
- `POST /getbestprice` - Accepts product search requests and forwards to Flask

### Flask Server (Port 5000)
- `POST /bestprice` - Main price comparison endpoint
- `GET /health` - Health check endpoint
- `GET /` - API information endpoint

## Sample Request/Response

**Request:**
```json
{
  "productOrUrl": "iPhone 15 Pro"
}
```

**Response:**
```json
{
  "success": true,
  "best_site": "amazon",
  "best_site_name": "Amazon",
  "best_price": 119900,
  "best_url": "https://amazon.in/product-url",
  "best_title": "Apple iPhone 15 Pro 128GB",
  "savings": 10000,
  "total_sites_found": 2,
  "search_query": "iPhone 15 Pro"
}
```

## Configuration

### ChromeDriver Path
Update the ChromeDriver path in `app.py`:
```python
chromedriver_path = r"C:\path\to\chromedriver.exe"
```

### Search Customization
Modify search behavior in `clean_product_name()` function:
- Add/remove noise words
- Adjust word filtering logic
- Change search term length limits

## Troubleshooting

### Common Issues

**ChromeDriver not found:**
- Ensure ChromeDriver is downloaded and path is correct
- Verify ChromeDriver version matches your Chrome browser

**No results found:**
- Try simpler search terms (e.g., "iPhone" instead of "iPhone 15 Pro Max 256GB")
- Check internet connection
- Verify both servers are running

**Price extraction failing:**
- E-commerce sites frequently change their HTML structure
- CSS selectors in `extract_price()` function may need updates
- Check debug logs for selector failures

**CORS errors:**
- Ensure Express server is running on port 3000
- Check CORS configuration in `app.js`

## Development

### Adding New E-commerce Sites
1. Create new search function in `app.py`
2. Add CSS selectors for price, title, and URL extraction  
3. Update the sites list in `best_price_endpoint()`

### Debugging
Enable detailed logging by checking Flask debug output:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Testing
Test individual components:
- Flask API: Use Postman or curl to test `/bestprice` endpoint
- Scraping: Run individual site search functions
- Frontend: Test UI components independently

## Limitations

- Currently supports Amazon India and Flipkart only
- Depends on website structure (may break if sites update HTML)
- Rate limited by scraping speed (10-15 seconds per search)
- Requires active internet connection for real-time scraping

## Future Enhancements

- [ ] Add more e-commerce platforms (Myntra, Snapdeal, etc.)
- [ ] Implement price history tracking
- [ ] Add user accounts and wishlists  
- [ ] Create browser extension version
- [ ] Add price alert notifications
- [ ] Mobile app development
- [ ] Machine learning for better product matching

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Selenium WebDriver for web automation capabilities
- Flask framework for robust backend development  
- Express.js for efficient request handling
- Chrome DevTools for debugging scraping issues

## Contact

**Team**: HackStreet Boys  
**Project**: CashTrim Companion  
**Hackathon**: September Sprint Hackathon 2025

For questions or support, please open an issue on GitHub.
