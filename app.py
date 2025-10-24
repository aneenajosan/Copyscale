import streamlit as st
from analyzer import analyzer
from visualizer import visualizer
from video_analyzer import video_analyzer
from copyright_db import copyright_db
from PIL import Image
import os
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Copyscale - AI Training Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look with new color scheme
st.markdown("""
<style>
    /* Import font for title */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');
    
    /* Main app background - space/cosmic theme */
    .stApp {
        background-image: url('https://images.pexels.com/photos/6138036/pexels-photo-6138036.jpeg?auto=compress&cs=tinysrgb&w=1920');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    /* Semi-transparent overlay for better readability */
    .main .block-container {
        background-color: rgba(0, 20, 40, 0.85);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* COPYSCALE Title */
    .copyscale-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 4.5rem;
        font-weight: 300;
        letter-spacing: 1.2rem;
        text-align: center;
        color: #FFFFFF;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }
    
    /* Subtitle */
    .copyscale-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 0.3rem;
        text-align: center;
        color: #B8D4E8;
        margin-bottom: 3rem;
    }
    
    /* Navigation buttons style */
    .nav-button-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 3rem 0;
        flex-wrap: wrap;
    }
    
    .nav-button {
        background-color: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: #FFFFFF;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 400;
        letter-spacing: 0.1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
        font-family: 'Montserrat', sans-serif;
    }
    
    .nav-button:hover {
        background-color: rgba(255, 255, 255, 0.25);
        border-color: rgba(255, 255, 255, 0.6);
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(255, 255, 255, 0.3);
    }
    
    /* Tab styling to match theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        letter-spacing: 0.1rem;
        padding: 12px 30px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(100, 180, 255, 0.3);
        border-color: rgba(150, 200, 255, 0.6);
        color: #FFFFFF;
    }
    
    /* Headers within pages */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 0.15rem;
    }
    
    /* All text to white/light colors */
    p, label, span, div {
        color: #E0E0E0 !important;
    }
    
    /* Upload sections */
    .upload-section {
        background-color: rgba(30, 60, 90, 0.6);
        border: 2px solid rgba(100, 180, 255, 0.4);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        border: 2px dashed rgba(150, 200, 255, 0.5) !important;
        background-color: rgba(30, 60, 90, 0.4) !important;
        border-radius: 10px;
        padding: 20px;
    }
    
    .stFileUploader > div > div:hover {
        border-color: rgba(150, 200, 255, 0.8) !important;
        background-color: rgba(40, 80, 120, 0.5) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: rgba(100, 180, 255, 0.25);
        color: #FFFFFF;
        border: 2px solid rgba(150, 200, 255, 0.5);
        border-radius: 50px;
        padding: 0.6rem 2rem;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 0.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: rgba(100, 180, 255, 0.4);
        border-color: rgba(150, 200, 255, 0.8);
        box-shadow: 0 4px 15px rgba(100, 180, 255, 0.4);
    }
    
    /* Metric cards */
    .metric-card {
        background-color: rgba(30, 60, 90, 0.7);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid rgba(100, 180, 255, 0.3);
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stMetric {
        background-color: rgba(30, 60, 90, 0.6);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(100, 180, 255, 0.3);
    }
    
    .stMetric label, .stMetric value {
        color: #FFFFFF !important;
    }
    
    /* Risk level indicators */
    .risk-high {
        background-color: rgba(255, 70, 70, 0.8);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        border: 2px solid rgba(255, 100, 100, 0.6);
    }
    
    .risk-medium {
        background-color: rgba(255, 180, 70, 0.8);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        border: 2px solid rgba(255, 200, 100, 0.6);
    }
    
    .risk-low {
        background-color: rgba(70, 200, 120, 0.8);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        border: 2px solid rgba(100, 220, 140, 0.6);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(30, 60, 90, 0.6);
        border: 1px solid rgba(100, 180, 255, 0.3);
        border-radius: 8px;
        color: #FFFFFF !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(30, 60, 90, 0.5);
        color: #FFFFFF;
        border: 2px solid rgba(100, 180, 255, 0.4);
        border-radius: 8px;
    }
    
    /* Sidebar if needed */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 25, 50, 0.95);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, 
            rgba(100, 180, 255, 0.3), 
            rgba(150, 200, 255, 0.6), 
            rgba(100, 180, 255, 0.3));
        margin: 2rem 0;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess, .stWarning, .stError, .stInfo {
        background-color: rgba(30, 60, 90, 0.8) !important;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Add new imports at the top
from video_analyzer import video_analyzer
from copyright_db import copyright_db

# Add new tab functions
def video_analysis_tab():
    st.header("Video Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Reference Image")
        reference_file = st.file_uploader("Upload reference image", type=['jpg', 'png', 'jpeg'], key="video_ref")
    
    with col2:
        st.subheader("Video File")
        video_file = st.file_uploader("Upload video to analyze", type=['mp4', 'avi', 'mov'], key="video_file")
    
    if reference_file and video_file:
        # Save files temporarily
        ref_path = "temp_video_ref.jpg"
        video_path = "temp_video.mp4"
        
        with open(ref_path, "wb") as f:
            f.write(reference_file.getbuffer())
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        
        if st.button("Analyze Video Frames"):
            with st.spinner("Extracting and analyzing video frames..."):
                results = video_analyzer.analyze_video_against_image(video_path, ref_path)
                
                if results:
                    display_video_results(results, ref_path)
        
        # Cleanup
        os.remove(ref_path)
        os.remove(video_path)


def database_tab():
    st.header("Copyright Database Management")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Content")
        
        # File upload for new content
        new_image = st.file_uploader(
            "Upload copyrighted image", 
            type=['jpg', 'png', 'jpeg'], 
            key="db_upload"
        )
        
        # Metadata inputs
        title = st.text_input("Title *", placeholder="Name of the artwork/frame")
        owner = st.text_input("Owner/Creator *", placeholder="Your name or company")
        description = st.text_area("Description", placeholder="Additional details about this content")
        
        # Add to database button
        if new_image and title and owner:
            if st.button("Add to Database", type="primary"):
                # Save temporary file
                temp_path = "temp_db_image.jpg"
                with open(temp_path, "wb") as f:
                    f.write(new_image.getbuffer())
                
                # Add to database
                if copyright_db.add_copyrighted_content(temp_path, title, owner, description):
                    st.success(f"Successfully added '{title}' to copyright database!")
                else:
                    st.error("Failed to add image to database. Please try again.")
                
                # Cleanup
                os.remove(temp_path)
        
        # Database statistics
        st.subheader("Database Stats")
        stats = copyright_db.get_database_stats()
        st.metric("Total Images", stats['total_images'])
        st.write(f"**Owners:** {', '.join(stats['owners']) if stats['owners'] else 'None'}")
        
        # Clear database option (for testing)
        if st.button("Clear Database", type="secondary"):
            copyright_db.database = {}
            copyright_db.save_database()
            st.warning("Database cleared!")
    
    with col2:
        st.subheader("Database Contents")
        
        if not copyright_db.database:
            st.info("Database is empty. Add some copyrighted content using the form on the left.")
        else:
            # Display all database entries
            for image_id, data in copyright_db.database.items():
                with st.expander(f"{data['title']} - {data['owner']}", expanded=False):
                    
                    # Display image if available
                    col_img, col_info = st.columns([1, 2])
                    
                    with col_img:
                        if os.path.exists(data['path']):
                            st.image(data['path'], use_column_width=True)
                        else:
                            st.warning("Image file not found")
                    
                    with col_info:
                        st.write(f"**Owner:** {data['owner']}")
                        st.write(f"**Description:** {data['description']}")
                        st.write(f"**File:** {os.path.basename(data['path'])}")
                        
                        # Remove button
                        if st.button("Remove", key=f"remove_{image_id}"):
                            del copyright_db.database[image_id]
                            copyright_db.save_database()
                            st.success("Removed from database!")
                            st.rerun()

def display_video_results(results, reference_path):
    """Display video analysis results"""
    st.subheader("Video Analysis Results")
    
    # Overall summary
    high_risk_frames = [r for r in results if r['analysis']['risk_level'] == "HIGH"]
    medium_risk_frames = [r for r in results if r['analysis']['risk_level'] == "MEDIUM"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Frames", len(results))
    with col2:
        st.metric("High Risk Frames", len(high_risk_frames))
    with col3:
        st.metric("Medium Risk Frames", len(medium_risk_frames))
    
    # Show frame-by-frame results
    for i, result in enumerate(results):
        # FIXED: Use 'time_seconds' instead of 'timestamp'
        with st.expander(f"Frame {i+1} - {result['frame_info']['time_seconds']:.1f}s - {result['analysis']['risk_level']} Risk"):
            col1, col2 = st.columns(2)
            with col1:
                st.image(result['frame_info']['image'], caption=f"Video Frame at {result['frame_info']['time_seconds']:.1f}s")
            with col2:
                st.image(reference_path, caption="Reference Image")
                
            # Show analysis results
            analysis = result['analysis']
            st.write(f"**Direct Similarity:** {analysis['direct_similarity']:.3f}")
            st.write(f"**Style Similarity:** {analysis['style_similarity']:.3f}")
            st.write(f"**Content Similarity:** {analysis['content_similarity']:.3f}")
            st.write(f"**Overall Risk:** {analysis['risk_level']}")

def database_scan_tab():
    st.header("Database Scan")
    st.write("Upload any image or video to check against your entire copyright database")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload image or video to scan", 
        type=['jpg', 'png', 'jpeg', 'mp4', 'avi', 'mov'],
        key="db_scan"
    )
    
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Save uploaded file
        temp_path = f"temp_scan{file_ext}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if file_ext in ['.jpg', '.png', '.jpeg']:
            # Image scan
            st.subheader("Image Scan Results")
            if st.button("Scan Image Against Database"):
                with st.spinner("Scanning against entire database..."):
                    matches = copyright_db.search_similar_content(temp_path, top_k=3)
                    display_database_scan_results(matches, temp_path, is_video=False)
        
        else:
            # Video scan  
            st.subheader("Video Scan Results")
            if st.button("Scan Video Against Database"):
                with st.spinner("Extracting frames and scanning database..."):
                    video_results = copyright_db.batch_video_analysis(temp_path)
                    display_video_scan_results(video_results, temp_path)
        
        # Cleanup
        os.remove(temp_path)

def display_database_scan_results(matches, query_path, is_video=False):
    """Display results from database scanning"""
    
    if not matches:
        st.success("No significant matches found in database!")
        return
    
    st.subheader(f"Top {len(matches)} Matches Found")
    
    for i, match in enumerate(matches):
        with st.expander(f"#{i+1}: {match['title']} by {match['owner']} (Similarity: {match['similarity']:.3f})"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(query_path, caption="Query Image", use_column_width=True)
            
            with col2:
                if os.path.exists(match['path']):
                    st.image(match['path'], caption=f"Match: {match['title']}", use_column_width=True)
            
            # Display full analysis results
            analysis = match['full_analysis']
            
            st.subheader("Detailed Analysis")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Direct Similarity", f"{analysis['direct_similarity']:.3f}")
            with col2:
                st.metric("Style Similarity", f"{analysis['style_similarity']:.3f}")
            with col3:
                st.metric("Content Similarity", f"{analysis['content_similarity']:.3f}")
            
            # Risk assessment
            risk_color = "HIGH" if analysis['risk_level'] == "HIGH" else "MEDIUM" if analysis['risk_level'] == "MEDIUM" else "LOW"
            st.write(f"**Overall Risk:** {risk_color}")
            st.write(f"**AI Training Detected:** {'YES' if analysis['is_ai_trained'] else 'NO'}")
            
            # Analysis notes
            st.subheader("Analysis Notes")
            for note in analysis.get('analysis_notes', []):
                if 'HIGH' in note:
                    st.error(note)
                elif 'MEDIUM' in note:
                    st.warning(note)
                else:
                    st.info(note)

def display_video_scan_results(video_results, video_path):
    """Display video database scan results"""
    
    # Overall summary
    high_risk_frames = [r for r in video_results if r['best_match'] and r['best_match']['full_analysis']['risk_level'] == "HIGH"]
    total_matches = sum(len(r['top_matches']) for r in video_results if r['top_matches'])
    
    st.subheader("Video Scan Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Frames", len(video_results))
    with col2:
        st.metric("High Risk Frames", len(high_risk_frames))
    with col3:
        st.metric("Total Matches", total_matches)
    
    # Show frame-by-frame results
    for i, result in enumerate(video_results):
        if result['top_matches']:
            best_match = result['top_matches'][0]
            
            with st.expander(f"Frame {i+1} - {result['frame_info']['time_seconds']:.1f}s - Best Match: {best_match['title']}"):
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.image(result['frame_info']['image'], caption=f"Video Frame at {result['frame_info']['time_seconds']:.1f}s")
                
                with col2:
                    if os.path.exists(best_match['path']):
                        st.image(best_match['path'], caption=f"Match: {best_match['title']}")
                
                with col3:
                    analysis = best_match['full_analysis']
                    st.write(f"**Similarity:** {best_match['similarity']:.3f}")
                    st.write(f"**Risk Level:** {analysis['risk_level']}")
                    st.write(f"**Owner:** {best_match['owner']}")
                    
                    if analysis['is_ai_trained']:
                        st.error("AI Training Likely Detected!")

def main():
    # Header
    st.markdown('<h1 class="copyscale-title">C O P Y S C A L E</h1>', unsafe_allow_html=True)
    st.markdown('<p class="copyscale-subtitle">Protect Your Intellectual Property</p>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["Image Analysis", "Database Scan", "Manage Database", "Video Analysis"])
    
    with tab1:
        image_analysis_section()
    
    with tab2:
        database_scan_tab()
    
    with tab3:
        database_tab()
    
    with tab4:
        video_analysis_tab()

def image_analysis_section():
    """The original image analysis functionality"""
    st.header("Image Analysis")
    
    # Introduction
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
    <h3>Protect Your Intellectual Property</h3>
    <p>Upload copyrighted images to detect if AI models were trained on your content using our advanced multi-layer neural network analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload sections in columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
        st.subheader("Reference Image")
        st.write("Your original copyrighted content")
        reference_file = st.file_uploader("Upload Reference", type=['jpg', 'png', 'jpeg'], key="reference", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
        st.subheader("Query Image") 
        st.write("Suspected AI-generated or training content")
        query_file = st.file_uploader("Upload Query", type=['jpg', 'png', 'jpeg'], key="query", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Analysis button
    if reference_file and query_file:
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        if st.button("Run Comprehensive Multi-Test Analysis", type="primary", use_container_width=True, help="Click to analyze both images using our advanced detection system"):
            with st.spinner('Running advanced multi-layer analysis... This may take a few moments.'):
                # Save uploaded files
                ref_path = "temp_reference.jpg"
                query_path = "temp_query.jpg"
                
                with open(ref_path, "wb") as f:
                    f.write(reference_file.getbuffer())
                with open(query_path, "wb") as f:
                    f.write(query_file.getbuffer())
                
                # Display uploaded images
                st.subheader("Uploaded Images")
                img_col1, img_col2 = st.columns(2)
                with img_col1:
                    st.image(reference_file, caption="Reference Image")
                with img_col2:
                    st.image(query_file, caption="Query Image")
                
                # Run comprehensive analysis
                results = analyzer.run_comprehensive_analysis(query_path, ref_path)
                
                # Display professional results
                display_professional_results(results, ref_path, query_path)
                
                # Cleanup
                os.remove(ref_path)
                os.remove(query_path)

def display_professional_results(results, ref_path, query_path):
    """Display professional results dashboard"""
    
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    st.markdown("## Comprehensive Multi-Test Analysis Results")
    
    # Risk Summary Card
    risk_level = results['risk_level'].lower()
    risk_color_class = f"risk-{risk_level}"
    
    st.markdown(f"""
    <div class='metric-card'>
        <h3>Overall Risk Assessment</h3>
        <div style='display: flex; align-items: center; gap: 2rem; margin: 1rem 0;'>
            <div class='{risk_color_class}' style='flex: 1; max-width: 200px;'>{results['risk_level']} RISK</div>
            <div style='flex: 2;'>
                <p><strong>Weighted Confidence Score:</strong> {results['weighted_score']:.2%}</p>
                <p><strong>AI Training Detected:</strong> {'YES' if results['is_ai_trained'] else 'NO'}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Three Metric Columns
    st.subheader("Detailed Similarity Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(
            "Direct Copy Risk", 
            f"{results['direct_similarity']:.2%}",
            delta=f"{(results['direct_similarity']-0.1)*100:+.1f}% vs safe" if results['direct_similarity'] > 0.1 else None,
            delta_color="inverse"
        )
        st.caption("Measures pixel-level and structural similarity. High values indicate potential direct copying.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(
            "Style Match", 
            f"{results['style_similarity']:.2%}",
            delta=f"Style influence detected" if results['style_similarity'] > 0.3 else "Minimal style match"
        )
        st.caption("Analyzes artistic style, textures, and patterns. Detects 'concept bleed' in AI training.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(
            "Content Similarity", 
            f"{results['content_similarity']:.2%}",
            delta=f"Content alignment" if results['content_similarity'] > 0.3 else "Different content"
        )
        st.caption("Evaluates subject matter, composition, and object relationships. Identifies content-based training.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Progress Bars
    visualizer.create_progress_bars(results)
    
    # Advanced Visualizations
    st.subheader("Advanced Analysis Visualizations")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.write("**Similarity Profile Radar**")
        radar_fig = visualizer.create_similarity_radar(results)
        st.pyplot(radar_fig)
        plt.close()
    
    with viz_col2:
        st.write("**Risk Assessment Heatmap**")
        heatmap_fig = visualizer.create_risk_heatmap(results)
        st.pyplot(heatmap_fig)
        plt.close()
    
    # Side-by-side comparison
    st.subheader("Visual Comparison Analysis")
    comparison_fig = visualizer.create_side_by_side_comparison(ref_path, query_path, results)
    st.pyplot(comparison_fig)
    plt.close()
    
    # Analysis Notes
    st.subheader("Expert Analysis Notes")
    for note in results.get('analysis_notes', []):
        if 'HIGH' in note:
            st.error(note)
        elif 'MEDIUM' in note:
            st.warning(note)
        else:
            st.info(note)
    
    # Technical Details
    with st.expander("Technical Analysis Details"):
        st.write(f"**Raw Similarity Scores:**")
        st.write(f"- Direct: `{results['direct_similarity']:.6f}`")
        st.write(f"- Style: `{results['style_similarity']:.6f}`")
        st.write(f"- Content: `{results['content_similarity']:.6f}`")
        st.write(f"- Weighted: `{results['weighted_score']:.6f}`")
        
        st.write("**Analysis Method:**")
        st.write("- Direct: Final ResNet50 layer features")
        st.write("- Style: Layer 2-3 features (textures/patterns)")
        st.write("- Content: Layer 1 + Final features (shapes/objects)")
        st.write("- Thresholds: HIGH > 0.7, MEDIUM > 0.4, LOW ≤ 0.4")

if __name__ == "__main__":
    main()
