# S&P 500 Earnings Calendar

A web application that displays the S&P 500 earnings calendar with a clean, interactive interface.

## Features
- Interactive calendar view
- Company earnings information
- Modal popups with detailed company data
- Responsive design

## Local Development
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API key:
   ```
   FMP_API_KEY=your_api_key_here
   ```
6. Run the application: `python main.py`
7. Access the application at `http://localhost:8080`

## Deployment to Render
1. Create a free account on [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
5. Add your `FMP_API_KEY` in the Environment Variables section
6. Deploy!

## API Key
This application uses the Financial Modeling Prep API. You can get a free API key at [Financial Modeling Prep](https://financialmodelingprep.com/developer/docs/).

## License
MIT

## Project Structure

```
sp500_earnings_calendar/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore file
└── templates/
    └── index.html      # Calendar template
``` 