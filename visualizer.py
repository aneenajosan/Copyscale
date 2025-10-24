import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st
import io

class ResultsVisualizer:
    def __init__(self):
        self.colors = {
            'high_risk': '#ff6b6b',
            'medium_risk': '#ffd166', 
            'low_risk': '#06d6a0',
            'neutral': '#118ab2'
        }
    
    def create_similarity_radar(self, results):
        """Create radar chart for similarity profile"""
        categories = ['Direct', 'Style', 'Content']
        values = [results['direct_similarity'], results['style_similarity'], results['content_similarity']]
        
        # Create radar chart
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]  # Complete the circle
        angles += angles[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        # Plot the main area
        ax.plot(angles, values, 'o-', linewidth=2, color=self.colors['neutral'], label='Similarity')
        ax.fill(angles, values, alpha=0.25, color=self.colors['neutral'])
        
        # Configure the chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
        ax.grid(True)
        
        # Add value annotations
        for angle, value, category in zip(angles[:-1], values[:-1], categories):
            ax.text(angle, value + 0.1, f'{value:.2f}', ha='center', va='center', 
                   fontweight='bold', fontsize=10)
        
        ax.set_title('Similarity Profile Analysis', size=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        return fig
    
    def create_risk_heatmap(self, results):
        """Create heatmap visualization of risks"""
        metrics = ['Direct Copy', 'Style Match', 'Content Match']
        scores = [results['direct_similarity'], results['style_similarity'], results['content_similarity']]
        colors = [self.get_color(score) for score in scores]
        
        fig, ax = plt.subplots(figsize=(10, 4))
        bars = ax.barh(metrics, scores, color=colors, height=0.6)
        
        # Add value labels
        for bar, score in zip(bars, scores):
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                   f'{score:.3f}', va='center', fontweight='bold', fontsize=11)
        
        ax.set_xlim(0, 1)
        ax.set_xlabel('Similarity Score', fontweight='bold')
        ax.set_title('Risk Assessment by Metric', fontweight='bold', pad=20)
        
        # Add threshold lines
        ax.axvline(x=0.7, color='red', linestyle='--', alpha=0.7, label='High Risk Threshold')
        ax.axvline(x=0.4, color='orange', linestyle='--', alpha=0.7, label='Medium Risk Threshold')
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    def get_color(self, score):
        """Get color based on risk score"""
        if score > 0.7:
            return self.colors['high_risk']
        elif score > 0.4:
            return self.colors['medium_risk']
        else:
            return self.colors['low_risk']
    
    def create_side_by_side_comparison(self, img1_path, img2_path, similarity_scores):
        """Create side-by-side comparison with annotations"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        try:
            # Load and display images
            img1 = Image.open(img1_path)
            img2 = Image.open(img2_path)
            
            ax1.imshow(img1)
            ax1.set_title('🖼️ Reference Image', fontsize=14, fontweight='bold', pad=10)
            ax1.axis('off')
            
            ax2.imshow(img2)
            ax2.set_title('🔍 Query Image', fontsize=14, fontweight='bold', pad=10)
            ax2.axis('off')
            
            # Add similarity score box
            score_text = (f"Similarity Analysis:\n"
                         f"• Direct: {similarity_scores['direct_similarity']:.3f}\n"
                         f"• Style: {similarity_scores['style_similarity']:.3f}\n" 
                         f"• Content: {similarity_scores['content_similarity']:.3f}\n"
                         f"• Overall: {similarity_scores['weighted_score']:.3f}")
            
            fig.text(0.5, 0.02, score_text, ha='center', va='bottom', 
                    fontsize=11, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray"),
                    transform=fig.transFigure)
            
        except Exception as e:
            # Fallback if images can't be loaded
            ax1.text(0.5, 0.5, 'Reference Image\n(Not available)', ha='center', va='center', transform=ax1.transAxes)
            ax2.text(0.5, 0.5, 'Query Image\n(Not available)', ha='center', va='center', transform=ax2.transAxes)
            ax1.axis('off')
            ax2.axis('off')
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        return fig
    
    def create_progress_bars(self, results):
        """Create custom progress bars for Streamlit"""
        st.subheader("📊 Similarity Progress")
        
        # Direct Similarity
        direct = results['direct_similarity']
        st.write(f"**Direct Copy Risk:** {direct:.1%}")
        st.progress(direct)
        
        # Style Similarity  
        style = results['style_similarity']
        st.write(f"**Style Match:** {style:.1%}")
        st.progress(style)
        
        # Content Similarity
        content = results['content_similarity']
        st.write(f"**Content Match:** {content:.1%}")
        st.progress(content)

# Global instance
visualizer = ResultsVisualizer()
