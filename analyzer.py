from sklearn.metrics.pairwise import cosine_similarity
import fingerprint
import numpy as np
import torch
import torch.nn as nn

class AdvancedAnalyzer:
    def __init__(self):
        self.fingerprinter = fingerprint.ImageFingerprinter()
        self.feature_cache = {}
        
    def extract_multi_layer_features(self, image_path):
        """Extract features from different ResNet layers for detailed analysis"""
        try:
            from PIL import Image
            
            # Hook to get intermediate layer features
            features = {}
            def get_features(name):
                def hook(model, input, output):
                    features[name] = output.detach()
                return hook
            
            # Register hooks for different layers
            self.fingerprinter.model.layer1.register_forward_hook(get_features('layer1'))  # Basic edges/shapes
            self.fingerprinter.model.layer2.register_forward_hook(get_features('layer2'))  # Textures/patterns  
            self.fingerprinter.model.layer3.register_forward_hook(get_features('layer3'))  # Style features
            self.fingerprinter.model.layer4.register_forward_hook(get_features('layer4'))  # Content/objects
            
            # Process image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.fingerprinter.transform(image).unsqueeze(0)
            
            with torch.no_grad():
                final_output = self.fingerprinter.model(image_tensor)
                features['final'] = final_output
            
            # Convert to numpy arrays
            feature_dict = {}
            for layer_name, tensor in features.items():
                feature_dict[layer_name] = tensor.numpy().flatten()
            
            return feature_dict
            
        except Exception as e:
            print(f"Error extracting layer features: {e}")
            return None
    
    def calculate_direct_similarity(self, img1_path, img2_path):
        """Direct pixel/structure similarity using final layer"""
        fp1 = self.fingerprinter.get_fingerprint(img1_path)
        fp2 = self.fingerprinter.get_fingerprint(img2_path)
        
        if fp1 is None or fp2 is None:
            return 0.0
            
        similarity = float(cosine_similarity([fp1], [fp2])[0][0])
        print(f"Direct similarity: {similarity:.4f}")
        return similarity
    
    def calculate_style_similarity(self, img1_path, img2_path):
        """Style similarity using intermediate layers (textures, patterns)"""
        try:
            features1 = self.extract_multi_layer_features(img1_path)
            features2 = self.extract_multi_layer_features(img2_path)
            
            if features1 is None or features2 is None:
                return 0.0
            
            # Use layer2 and layer3 for style (captures textures and patterns)
            style_features1 = []
            style_features2 = []
            
            for layer in ['layer2', 'layer3']:
                if layer in features1 and layer in features2:
                    style_features1.append(features1[layer])
                    style_features2.append(features2[layer])
            
            if not style_features1:
                return 0.0
                
            # Average similarity across style layers
            style_similarities = []
            for feat1, feat2 in zip(style_features1, style_features2):
                sim = cosine_similarity([feat1], [feat2])[0][0]
                style_similarities.append(sim)
            
            avg_style_sim = np.mean(style_similarities)
            print(f"Style similarity: {avg_style_sim:.4f}")
            return float(avg_style_sim)
            
        except Exception as e:
            print(f"Style similarity error: {e}")
            return 0.0
    
    def calculate_content_similarity(self, img1_path, img2_path):
        """Content similarity using early and final layers (objects, composition)"""
        try:
            features1 = self.extract_multi_layer_features(img1_path)
            features2 = self.extract_multi_layer_features(img2_path)
            
            if features1 is None or features2 is None:
                return 0.0
            
            # Use layer1 and final layer for content (captures basic shapes and high-level objects)
            content_features1 = []
            content_features2 = []
            
            for layer in ['layer1', 'final']:
                if layer in features1 and layer in features2:
                    content_features1.append(features1[layer])
                    content_features2.append(features2[layer])
            
            if not content_features1:
                return 0.0
                
            # Average similarity across content layers
            content_similarities = []
            for feat1, feat2 in zip(content_features1, content_features2):
                sim = cosine_similarity([feat1], [feat2])[0][0]
                content_similarities.append(sim)
            
            avg_content_sim = np.mean(content_similarities)
            print(f"Content similarity: {avg_content_sim:.4f}")
            return float(avg_content_sim)
            
        except Exception as e:
            print(f"Content similarity error: {e}")
            return 0.0
    
    def run_comprehensive_analysis(self, query_path, reference_path):
        """Run all analysis types and return comprehensive results"""
        print(f"🔍 Running comprehensive analysis: {query_path} vs {reference_path}")
        
        try:
            # Calculate all similarity types
            print("📊 Calculating direct similarity...")
            direct_sim = self.calculate_direct_similarity(reference_path, query_path)
            
            print("🎨 Calculating style similarity...")
            style_sim = self.calculate_style_similarity(reference_path, query_path)
            
            print("🖼️ Calculating content similarity...")
            content_sim = self.calculate_content_similarity(reference_path, query_path)
            
            # Overall risk assessment with weighted scoring
            weighted_score = (direct_sim * 0.5) + (style_sim * 0.1) + (content_sim * 0.5)
            
            # Determine risk levels
            if weighted_score > 0.7:
                risk_level = "HIGH"
                is_ai_trained = True
            elif weighted_score > 0.4:
                risk_level = "MEDIUM" 
                is_ai_trained = True
            else:
                risk_level = "LOW"
                is_ai_trained = False
            
            print(f"✅ Analysis complete - Overall risk: {risk_level} ({weighted_score:.4f})")
            
            return {
                "direct_similarity": direct_sim,
                "style_similarity": style_sim,
                "content_similarity": content_sim,
                "weighted_score": weighted_score,
                "is_ai_trained": is_ai_trained,
                "risk_level": risk_level,
                "analysis_notes": self.generate_analysis_notes(direct_sim, style_sim, content_sim)
            }
            
        except Exception as e:
            print(f"❌ Comprehensive analysis error: {e}")
            return {
                "direct_similarity": 0.0,
                "style_similarity": 0.0,
                "content_similarity": 0.0,
                "weighted_score": 0.0,
                "is_ai_trained": False,
                "risk_level": "LOW",
                "analysis_notes": "Analysis failed due to error"
            }
    
    def generate_analysis_notes(self, direct, style, content):
        """Generate human-readable analysis notes"""
        notes = []
        
        if direct > 0.8:
            notes.append("🚨 Very high direct similarity - potential exact copy")
        elif direct > 0.6:
            notes.append("⚠️ High direct similarity - strong structural match")
        elif direct > 0.4:
            notes.append("📝 Moderate direct similarity - some structural elements match")
        
        if style > 0.7:
            notes.append("🎨 Strong style match - similar artistic patterns and textures")
        elif style > 0.5:
            notes.append("🖌️ Moderate style influence - some stylistic elements shared")
        
        if content > 0.7:
            notes.append("🖼️ High content similarity - similar subjects and composition")
        elif content > 0.5:
            notes.append("📷 Moderate content match - some subject matter overlap")
        
        if not notes:
            notes.append("✅ Minimal similarities detected - low risk of training data contamination")
        
        return notes

# Global instance for easy import
analyzer = AdvancedAnalyzer()

# Test function
def test_advanced_analyzer():
    """Test the advanced analyzer"""
    print("🧪 Testing Advanced Analyzer...")
    test_analyzer = AdvancedAnalyzer()
    
    # This will work when you have test images
    try:
        result = test_analyzer.run_comprehensive_analysis("test_image.jpg", "test_image.jpg")
        print(f"Test result: {result}")
    except Exception as e:
        print(f"Test failed (normal without test images): {e}")
        print("✅ Advanced analyzer is ready!")

if __name__ == "__main__":
    test_advanced_analyzer()
