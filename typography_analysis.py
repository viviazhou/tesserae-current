import cv2
import numpy as np

class TypographyAnalyzer:
    def __init__(self):
        self.pairings_db = [
            {"name": "Modern Sans", "heading": "Inter", "body": "Roboto", "use_case": "UI"},
            {"name": "Classic Serif", "heading": "Playfair Display", "body": "Lato", "use_case": "Editorial"},
            {"name": "Tech Mono", "heading": "Space Grotesk", "body": "JetBrains Mono", "use_case": "Tech"}
        ]

    def analyze_typography(self, image_path):
        image = cv2.imread(str(image_path))
        if image is None: return self._default_result()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
        grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
        _, binary = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = sum(1 for c in contours if cv2.boundingRect(c)[2] > 20)
        
        avg_brightness = np.mean(gray)
        idx = 2 if avg_brightness < 80 else (1 if avg_brightness > 200 else 0)
            
        selected = self.pairings_db[idx]
        
        return {
            "text_detected": text_regions > 0,
            "text_regions": text_regions,
            "analysis": {"dominant_weight": "Regular" if avg_brightness > 128 else "Bold"},
            "font_pairings": [selected, self.pairings_db[(idx + 1) % 3]],
            "font_suggestions": {"heading": {"fonts": [selected['heading']]}, "body": {"fonts": [selected['body']]}}
        }

    def _default_result(self):
        return {
            "text_detected": False, "text_regions": 0,
            "analysis": {"dominant_weight": "Regular"},
            "font_pairings": [self.pairings_db[0]],
            "font_suggestions": {"heading": {"fonts": ["Inter"]}, "body": {"fonts": ["Roboto"]}}
        }

    def generate_design_tokens(self, typography_data):
        pairings = typography_data.get("font_pairings", []) if isinstance(typography_data, dict) else typography_data
        if not pairings: return {}
            
        primary = pairings[0]
        return {
            "font-family-heading": {"value": primary['heading'], "type": "fontFamily"},
            "font-family-body": {"value": primary['body'], "type": "fontFamily"},
            "font-weight-base": {"value": "400", "type": "fontWeight"}
        }

    def export_css_variables(self, tokens):
        css = ":root {\n"
        for name, token in tokens.items():
            css += f"  --{name}: {token['value']};\n"
        css += "}"
        return css