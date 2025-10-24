import cv2
import os
import tempfile
from analyzer import analyzer
import streamlit as st
from PIL import Image
import numpy as np

class VideoAnalyzer:
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv']
    
    def extract_keyframes(self, video_path, num_frames=8):
        """Extract keyframes from video for analysis"""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                st.error("❌ Could not open video file")
                return []
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = total_frames / fps if fps > 0 else 0
            
            st.info(f"📹 Video Info: {total_frames} frames, {duration:.1f}s duration, {fps:.1f} FPS")
            
            keyframes = []
            
            # Extract frames at regular intervals
            for i in range(num_frames):
                frame_time = (i / num_frames) * duration
                frame_pos = int(frame_time * fps)
                
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                ret, frame = cap.read()
                
                if ret:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_pil = Image.fromarray(frame_rgb)
                    
                    # Save frame temporarily
                    frame_path = f"video_frame_{i}.jpg"
                    frame_pil.save(frame_path)
                    
                    keyframes.append({
                        'frame_number': frame_pos,
                        'time_seconds': frame_time,
                        'image': frame_pil,
                        'path': frame_path
                    })
            
            cap.release()
            st.success(f"✅ Extracted {len(keyframes)} keyframes from video")
            return keyframes
            
        except Exception as e:
            st.error(f"❌ Video processing error: {e}")
            return []

    def analyze_video_against_image(self, video_path, reference_image_path):
        """Analyze video frames against a reference image"""
        try:
            # Extract keyframes from video
            keyframes = self.extract_keyframes(video_path)
            
            if not keyframes:
                st.error("❌ No frames extracted from video")
                return []
            
            results = []
            
            # Analyze each frame against the reference image
            for frame in keyframes:
                # Run comprehensive analysis for this frame
                analysis = analyzer.run_comprehensive_analysis(frame['path'], reference_image_path)
                
                results.append({
                    'frame_info': frame,
                    'analysis': analysis
                })
            
            return results
            
        except Exception as e:
            st.error(f"❌ Video analysis error: {e}")
            return []

# Global instance
video_analyzer = VideoAnalyzer()