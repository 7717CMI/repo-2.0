# 🚛 Freight Intelligence Dashboard

A production-ready, interactive dashboard for visualizing freight lead data using Plotly Dash. This dashboard provides comprehensive insights into drayage, container shipping, and freight forwarding leads with dynamic filtering and clean, business-grade UI.

## ✨ Features

- **📊 7 Interactive Charts**: Load origins, intent distribution, industry breakdown, priority analysis, lead sources, shipment values, timeline trends
- **👥 Comprehensive Lead Management**: Contact information, priority levels, status tracking
- **🔍 Advanced Filtering**: State, industry, inquiry type, priority, intent score, date range
- **📥 Export Capabilities**: CSV download and contact export
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🚀 Production Ready**: Optimized for cloud deployment

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open browser to http://localhost:8050
```

### Render Deployment
1. Push code to GitHub repository
2. Go to [Render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:server`

### Docker Deployment
```bash
# Build and run
docker build -t freight-dashboard .
docker run -p 8050:8050 freight-dashboard
```

## 📁 Project Structure

```
freight-dashboard/
├── app.py                 # Main Dash application
├── data/
│   └── leads.csv         # Sample freight data (300 records)
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment config
├── runtime.txt          # Python version specification
├── Dockerfile           # Docker configuration
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 📊 Dashboard Analytics

### 1. Load Origins by State
Geographic distribution of shipment origins across US states

### 2. Intent Score Distribution
Lead quality categorization (High/Medium/Low) for conversion prediction

### 3. Industry Breakdown
Market share analysis by industry sector

### 4. Priority Level Analysis
Urgency distribution for sales team prioritization

### 5. Lead Source Performance
Marketing channel effectiveness analysis

### 6. Shipment Value Analysis
Revenue potential by industry and priority

### 7. Timeline Analysis
Lead generation trends over time

## 🎯 Key Metrics

- **Total Leads**: Count with trend indicators
- **Average Intent Score**: Lead quality metric
- **Total Shipment Value**: Revenue potential
- **High Priority Leads**: Urgent/High priority count
- **Top Industry**: Most active sector
- **Conversion Rate**: Success rate percentage

## 📋 Data Schema

The dataset includes comprehensive lead information:
- **Contact Details**: Company name, contact person, phone, email
- **Business Info**: Industry, company size, state, city
- **Lead Management**: Priority level, status, intent score
- **Shipment Data**: Origin, destination, weight, value
- **Timeline**: Inquiry date, expected ship date, follow-up date
- **Actions**: Next action required, lead source

## 🔧 Configuration

### Environment Variables
- `PORT`: Application port (default: 8050)
- `PYTHON_VERSION`: Python version (3.11.7)

### Dependencies
- Dash 2.14.1 - Web framework
- Plotly 5.17.0 - Interactive charts
- Pandas 2.1.3 - Data processing
- Bootstrap Components - UI styling
- Gunicorn 21.2.0 - Production server

## 📞 Support

For questions or issues, please refer to the Plotly Dash documentation or create an issue in the project repository.

## 📄 License

MIT License - see LICENSE file for details