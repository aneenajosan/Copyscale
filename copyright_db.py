import json
import os
import numpy as np
from analyzer import analyzer
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

class CopyrightDatabase:
    def __init__(self, db_file="copyright_database.json"):
        self.db_file = db_file
        self.database = self.load_database()
    
    def load_database(self):
        """Load the copyright database from file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_database(self):
        """Save the database to file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.database, f, indent=2)
    
    def add_copyrighted_content(self, image_path, title, owner, description=""):
        """Add a copyrighted image to the database"""
        try:
            # Generate fingerprint
            fingerprint = analyzer.fingerprinter.get_fingerprint(image_path)
            
            if fingerprint is not None:
                image_id = f"{owner}_{title}_{os.path.basename(image_path)}"
                
                self.database[image_id] = {
                    'title': title,
                    'owner': owner,
                    'description': description,
                    'fingerprint': fingerprint.tolist(),
                    'path': image_path,
                    'image_id': image_id
                }
                
                self.save_database()
                return True
        except Exception as e:
            st.error(f"Error adding to database: {e}")
        
        return False
    
    def search_similar_content(self, query_image_path, top_k=3):
        """Search for similar content in the database and return top matches with full analysis"""
        query_fp = analyzer.fingerprinter.get_fingerprint(query_image_path)
        if query_fp is None:
            return []
        
        matches = []
        
        # Compare against every image in database
        for image_id, data in self.database.items():
            db_fingerprint = np.array(data['fingerprint'])
            
            # Calculate similarity
            similarity = cosine_similarity([query_fp], [db_fingerprint])[0][0]
            
            # Run full comprehensive analysis for top candidates
            if similarity > 0.3:  # Only analyze reasonably similar images
                full_analysis = analyzer.run_comprehensive_analysis(query_image_path, data['path'])
                
                matches.append({
                    'image_id': image_id,
                    'similarity': float(similarity),
                    'title': data['title'],
                    'owner': data['owner'],
                    'description': data['description'],
                    'path': data['path'],
                    'full_analysis': full_analysis
                })
        
        # Sort by similarity and return top K
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches[:top_k]
    
    def batch_video_analysis(self, video_path, top_matches_per_frame=2):
        """Analyze video against entire database"""
        from video_analyzer import video_analyzer
        
        keyframes = video_analyzer.extract_keyframes(video_path)
        all_frame_results = []
        
        progress_bar = st.progress(0)
        
        for i, frame in enumerate(keyframes):
            progress = (i + 1) / len(keyframes)
            progress_bar.progress(progress)
            
            # Search database for this frame
            frame_matches = self.search_similar_content(frame['path'], top_k=top_matches_per_frame)
            
            all_frame_results.append({
                'frame_info': frame,
                'top_matches': frame_matches,
                'best_match': frame_matches[0] if frame_matches else None
            })
        
        progress_bar.empty()
        return all_frame_results
    
    def get_database_stats(self):
        """Get database statistics"""
        return {
            'total_images': len(self.database),
            'owners': list(set(item['owner'] for item in self.database.values()))
        }

# Global instance
copyright_db = CopyrightDatabase()
