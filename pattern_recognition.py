import cv2
import numpy as np

class PatternRecognizer:
    def __init__(self):
        pass

    def analyze_patterns(self, image_path):
        image = cv2.imread(str(image_path))
        if image is None: return self._default_patterns()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rects = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 100]
        
        spacings = []
        rects.sort(key=lambda x: x[0])
        for i in range(len(rects) - 1):
            gap = rects[i+1][0] - (rects[i][0] + rects[i][2])
            if gap > 0: spacings.append(gap)
                
        base_unit = 8
        if spacings:
            hist = np.histogram(spacings, bins=range(0, 100, 4))
            if hist[1][np.argmax(hist[0])] > 0:
                base_unit = int(hist[1][np.argmax(hist[0])])

        cols = 12
        if len(rects) > 2:
            avg_width = np.mean([r[2] for r in rects])
            cols = max(1, min(12, int(image.shape[1] / (avg_width + base_unit))))

        return {
            "spacing": {
                "base_unit": base_unit,
                "spacing_scale": {
                    "xs": base_unit // 2, "sm": base_unit, "md": base_unit * 2,
                    "lg": base_unit * 4, "xl": base_unit * 8
                },
                "total_gaps_analyzed": len(spacings)
            },
            "grid": {"columns": cols, "gutter": base_unit * 2, "margin": base_unit * 3}
        }

    def _default_patterns(self):
        return {
            "spacing": {"base_unit": 8, "spacing_scale": {"xs": 4, "sm": 8, "md": 16}, "total_gaps_analyzed": 0},
            "grid": {"columns": 12, "gutter": 16, "margin": 24}
        }

    def generate_design_tokens(self, patterns):
        tokens = {}
        for name, value in patterns['spacing']['spacing_scale'].items():
            tokens[f"spacing-{name}"] = {"value": f"{value}px", "type": "dimension"}
        
        tokens["grid-cols"] = {"value": str(patterns['grid']['columns']), "type": "integer"}
        tokens["grid-gutter"] = {"value": f"{patterns['grid']['gutter']}px", "type": "dimension"}
        return tokens

    def export_css_variables(self, tokens):
        css = ":root {\n"
        for name, token in tokens.items():
            css += f"  --{name}: {token['value']};\n"
        css += "}"
        return css