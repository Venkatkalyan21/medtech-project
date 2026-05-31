# Initialize with your API key

## Setting Up the Agent

Before using the medical agent, you need to set up your Google Gemini API key.

### Option 1: Environment Variable

```bash
# Linux/macOS
export GEMINI_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"
```

Then initialize the agent:

```python
from agent_system import MedicalAgent

# API key is automatically loaded from environment variable
agent = MedicalAgent()
```

### Option 2: .env File

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-api-key-here
MONGO_URI=your-mongodb-uri
NEXTAUTH_SECRET=your-nextauth-secret
```

Then use a library like `python-dotenv` to load it:

```python
from dotenv import load_dotenv
from agent_system import MedicalAgent

load_dotenv()
agent = MedicalAgent()
```

### Option 3: Pass API Key Directly (Not Recommended for Production)

```python
from agent_system import MedicalAgent

agent = MedicalAgent(api_key="your-api-key-here")
```

⚠️ **Never commit API keys to version control!**

## Usage Example

```python
from agent_system import MedicalAgent

# Initialize agent
agent = MedicalAgent()

# Prepare lab results
lab_results = {
    "creatinine": {
        "value": 1.8,
        "unit": "mg/dL",
        "status": "HIGH",
        "reference_range": "0.7 - 1.3"
    },
    "egfr": {
        "value": 45,
        "unit": "mL/min/1.73m²",
        "status": "LOW",
        "reference_range": "> 90"
    }
}

# Analyze results
result = agent.analyze_and_explain(
    lab_results=lab_results,
    ckd_risk_level="MODERATE",
    ckd_risk_score=0.35
)

# Use the results
print(result["medical_explanation"])
for recommendation in result["recommendations"]:
    print(recommendation)
```

## Security Best Practices

1. **Never hardcode API keys** in your source code
2. **Use environment variables** for sensitive credentials
3. **Add `.env` to `.gitignore`** to prevent accidental commits
4. **Rotate API keys** regularly
5. **Use different keys** for development, staging, and production

## Troubleshooting

### Error: "GEMINI_API_KEY environment variable is not set"

Make sure you've set the environment variable before running your script:

```bash
export GEMINI_API_KEY="your-api-key-here"
python your_script.py
```

### Error: "Could not authenticate with the provided API key"

Check that:
- Your API key is valid
- Your Google Cloud project has the Generative AI API enabled
- You have the correct permissions in your Google Cloud account
