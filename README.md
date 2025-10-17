# 🚛 Comprehensive Customer Intelligence Dashboard

A production-ready, interactive dashboard for visualizing freight customer data and shipment requirements using Plotly Dash. This dashboard provides comprehensive insights into customer inquiries, contact information, and shipment analytics with dynamic filtering and clean, business-grade UI.

## ✨ Features

- **📊 7 Interactive Charts**: Shipment origins, requirements distribution, industry breakdown, rate analysis, distance distribution, commodity analysis, timeline trends
- **👥 Comprehensive Customer Management**: Complete contact information, shipment requirements, and business intelligence
- **🔍 Advanced Filtering**: Industry, shipment type, commodity, priority, source/destination countries, rate range, date range
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
docker build -t customer-intelligence-dashboard .
docker run -p 8050:8050 customer-intelligence-dashboard
```

## 📁 Project Structure

```
customer-intelligence-dashboard/
├── app.py                 # Main Dash application
├── data/
│   └── leads.csv         # Customer data (300 records)
├── requirements.txt      # Python dependencies
├── Procfile             # Render deployment config
├── runtime.txt          # Python version specification
├── Dockerfile           # Docker configuration
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 📊 Dashboard Analytics

### 1. Shipment Origins by Country
Geographic distribution of shipment origins across countries

### 2. Shipment Requirements Distribution
Distribution of different shipment types (Container, FTL, LTL, Drayage, etc.)

### 3. Industry Type Breakdown
Market share analysis by industry sector

### 4. Rate Value Analysis
Revenue potential analysis by rate categories (High/Medium/Low Value)

### 5. Distance Distribution
Distance analysis by industry and priority level

### 6. Commodity Type Analysis
Product/commodity type distribution and trends

### 7. Inquiry Timeline
Customer inquiry trends over time

## 🎯 Key Metrics

- **Total Customers**: Count with comprehensive filtering
- **Average Rate**: Average quote/rate requested
- **Total Distance**: Sum of all shipment distances
- **High Priority**: Urgent/High priority customer count
- **Top Industry**: Most active industry sector
- **Conversion Rate**: Success rate percentage

## 📋 Customer Intelligence Data Schema

The dataset includes comprehensive customer information:

### **Contact Details**
- Company Name
- Contact Person Name
- Email
- Phone

### **Shipment Requirements**
- Shipment Requirement (Container, FTL, LTL, Drayage, etc.)
- Product / Commodity Type
- Industry Type

### **Location Intelligence**
- Source Location / Country / Region
- Destination Location / Country / Region
- Distance to be Covered (in Km)

### **Business Intelligence**
- Rate / Quote Requested
- Date of Inquiry
- Priority Level
- Status
- Lead Source

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