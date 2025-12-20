# 🏥 Unmasking Silent Diseases

An AI-powered medical lab report analysis platform that provides early disease risk prediction, intelligent insights, and personalized health recommendations.

## 🌟 Overview

This project is a comprehensive healthcare solution that combines OCR technology, machine learning, and AI agents to analyze medical lab reports and predict chronic kidney disease (CKD) risk. The system features an ultra-modern 3D UI with advanced visualizations and real-time health insights.

## 🎯 Key Features

- **📄 PDF Lab Report Upload & OCR**: Automated extraction of lab values from medical reports
- **🤖 AI-Powered Analysis**: Google Gemini-based intelligent agent for medical explanations
- **📊 CKD Risk Prediction**: Machine learning model for early disease detection
- **📥 PDF Report Download**: Generate and download professional medical reports as PDF
- **🎨 Ultra-Modern 3D UI**: Stunning interface with Three.js, particle effects, and holographic cards
- **📈 Interactive Visualizations**: Real-time charts, 3D health spheres, and biomarker tracking
- **💡 Personalized Recommendations**: Tailored health advice based on lab results
- **🔐 Secure Authentication**: NextAuth-based user authentication system

## 🏗️ Project Structure

```
Unmasking Silent Diseases/
├── frontend/          # Next.js React frontend with 3D UI
├── backend/           # FastAPI backend server
└── agent/             # Standalone AI agent system
```

## 🚀 Technology Stack

### Frontend
- **Framework**: Next.js 16.1.0 with React 19
- **3D Graphics**: Three.js, React Three Fiber, React Three Drei
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Authentication**: NextAuth
- **Styling**: CSS with modern design patterns
- **Language**: TypeScript

### Backend
- **Framework**: FastAPI 0.109.0
- **Server**: Uvicorn
- **Database**: MongoDB (PyMongo)
- **OCR**: Pytesseract, PDF2Image
- **AI**: Google Generative AI (Gemini)
- **Image Processing**: Pillow

### AI Agent
- **Model**: Google Gemini API
- **Purpose**: Medical explanation generation and decision-making

## 📦 Installation

### Prerequisites
- Node.js 20+ and npm
- Python 3.8+
- MongoDB
- Tesseract OCR

### Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env.local` file:
```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017/medtech
GEMINI_API_KEY=your-gemini-api-key
```

Run the backend server:
```bash
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`

### Agent Setup

```bash
cd agent
pip install -r requirements.txt
```

The agent is integrated into the backend but can also run standalone for testing.

## 🎮 Usage

### 1. User Authentication
- Navigate to the login page
- Sign in or create an account

### 2. Upload Lab Report
- Go to the upload page
- Upload a PDF medical lab report
- The system will automatically extract lab values using OCR

### 3. View Analysis
- Navigate to the dashboard
- View comprehensive analysis including:
  - Lab value classifications (LOW/NORMAL/HIGH)
  - CKD risk prediction with confidence scores
  - AI-generated medical explanations
  - Personalized health recommendations
  - Interactive 3D visualizations

### 4. Track Health Trends
- Monitor biomarker trends over time
- View health timeline
- Analyze risk distribution

### 5. Download PDF Report
- Click the "Download PDF Report" button in the dashboard header
- Professional medical report is generated with:
  - Complete lab results table
  - Risk assessment
  - AI-generated explanations
  - Personalized recommendations
  - Medical disclaimer
- PDF automatically downloads to your device

## 🧠 AI Agent System

The medical agent provides intelligent analysis through:

### Decision Making
- Analyzes risk levels and lab results
- Determines priority and urgency
- Identifies focus areas
- Decides if specialist consultation is needed

### AI Explanation
- Uses Google Gemini for natural language explanations
- Tailors tone based on severity
- Explains in patient-friendly language
- Provides context for abnormal values

### Recommendations
- Generates personalized health advice
- Suggests lifestyle changes
- Recommends follow-up actions
- Indicates when to seek medical help

## 📊 API Endpoints

### Backend API

- `GET /` - Health check
- `POST /upload` - Upload lab report PDF
- `POST /analyze` - Analyze lab results and get predictions
- `POST /download/pdf` - Generate and download PDF report
- `GET /download/test-pdf` - Test PDF generation with sample data

## 🎨 UI Features

### 3D Visualizations
- **Health Sphere**: Interactive 3D representation of health status
- **Risk Meter**: 3D animated risk level indicator
- **Particle Background**: Dynamic particle system

### Advanced Components
- **Holographic Cards**: Glassmorphic cards with depth effects
- **Biomarker Charts**: Real-time trend visualization
- **Vital Signs Radar**: Multi-dimensional health metrics
- **AI Insights Panel**: Intelligent recommendations display
- **Reasoning Panel**: Transparent AI decision-making

### Animations
- Smooth page transitions
- Micro-interactions on hover
- Loading states with premium animations
- Dynamic gradient backgrounds

## 🔬 Medical Analysis Pipeline

1. **PDF Upload** → User uploads medical lab report
2. **OCR Extraction** → Tesseract extracts text from PDF
3. **Lab Parsing** → Identifies and extracts lab values
4. **Classification** → Rule engine classifies values (LOW/NORMAL/HIGH)
5. **ML Prediction** → Model predicts CKD risk
6. **Agent Analysis** → AI agent generates explanations
7. **Recommendations** → Personalized health advice
8. **Visualization** → Results displayed in 3D UI

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Agent Tests
```bash
cd agent
python test_agent.py
```

## 📝 Development Notes

### Backend Integration
The AI agent is integrated into the backend via `services/agent_service.py`. The agent processes:
- Classified lab results
- CKD risk predictions
- Patient context

### Database Schema
MongoDB collections:
- `users` - User authentication data
- `reports` - Uploaded lab reports
- `analyses` - Analysis results and predictions

## 🔐 Security

- Environment variables for sensitive data
- CORS configured for frontend-backend communication
- Secure file upload handling
- Authentication via NextAuth

## 🚧 Future Enhancements

- [ ] Multi-disease prediction (diabetes, cardiovascular)
- [ ] Mobile app version
- [ ] Doctor dashboard for patient monitoring
- [ ] Integration with electronic health records (EHR)
- [ ] Multi-language support
- [ ] Voice-based report reading
- [ ] Telemedicine integration

## 📄 License

This project is developed for educational and research purposes.

## 👥 Contributors

- Frontend & 3D UI Development
- Backend & ML Integration
- AI Agent System

## 🆘 Support

For issues or questions:
1. Check the documentation in each module's README
2. Review test results in `TEST_RESULTS.md` files
3. Check integration notes in `AGENT_INTEGRATION.md`

## 🎉 Acknowledgments

- Google Gemini API for AI capabilities
- Three.js community for 3D graphics
- FastAPI and Next.js teams for excellent frameworks

---

**Built with ❤️ for better healthcare outcomes**
