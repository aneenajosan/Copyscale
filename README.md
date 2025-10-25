# Copyscale
An advanced multi-layer neural network analysis system designed to detect if AI models were trained on copyrighted content. Protect your intellectual property with comprehensive similarity detection across images and videos.

Content creators, movie studios, and copyright holders currently lack effective tools to detect and prove when their intellectual property has been used without permission to train generative AI models, leading to widespread unauthorized use and significant financial/creative losses. Copyscale helps protect your intellectual property.

---

# Features
### Multi-Test Image Analysis
1. **Direct Copy Detection**: Pixel-level and structural similarity analysis

2. **Style Match Analysis**: Artistic patterns, textures, and stylistic elements

3. **Content Similarity**: Subject matter, composition, and object relationships

4. **Weighted Risk Assessment**: Intelligent scoring with configurable weights

### Video Content Protection
1. Frame-by-frame analysis of video content

2. Keyframe extraction and comparison

3. Batch processing against copyright database
### Advanced Analytics
1. Interactive radar charts and heatmaps

2. Progress visualization with detailed metrics

3. Professional risk assessment dashboard

4. Comprehensive analysis notes

### Copyright Database
1. Secure storage of copyrighted content fingerprints

2. Batch scanning against entire database

3. Multi-owner support with metadata management
---
# Installation
## Pre-requisites
- Python 3.8 or higher
- pip package manager

 ## Step-by-Step Setup
### 1. Clone the Repository
```bash
git clone https://github.com/aneenajosan/Copyscale.git
cd copyscale
```
### 2. Create Virtual Environment (Recommended)
**For Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Launch the Application
```bash
streamlit run app.py
```
### 5. Access the Application
Open your web browser and navigate to:

```text
http://localhost:8501
```

---
# File Structure
```text
Copyscale/
├── app.py                 # Main Streamlit application
├── analyzer.py           # Core analysis engine with multi-layer features
├── fingerprint.py        # Image fingerprinting using ResNet50
├── visualizer.py         # Data visualization and chart generation
├── video_analyzer.py     # Video processing and frame analysis
├── copyright_db.py       # Database management for copyrighted content
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore file
├── Project Abstract.docx # Project abstract and user flow
└── copyscale.pdf        # Project documentation and presentation
```
