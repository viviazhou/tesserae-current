import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import colorsys

class ColorExtractor:
    def __init__(self, n_colors=8):
        self.n_colors = n_colors

    def extract_palette(self, image_path):
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError("Could not load image")
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
        modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)

        clf = KMeans(n_clusters=self.n_colors, n_init=10)
        labels = clf.fit_predict(modified_image)
        
        counts = Counter(labels)
        center_colors = clf.cluster_centers_
        
        ordered_colors = [center_colors[i] for i in counts.keys()]
        ordered_counts = [counts[i] for i in counts.keys()]
        total_pixels = sum(ordered_counts)
        
        sorted_indices = np.argsort(ordered_counts)[::-1]
        
        colors_data = []
        for i in sorted_indices:
            rgb = ordered_colors[i].astype(int)
            hex_code = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
            percentage = round((ordered_counts[i] / total_pixels) * 100, 1)
            
            # Calculate HSL (colorsys returns 0-1)
            r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            
            # FIX: Return HSL as dictionary with 0-100 scale for S/L
            hsl_dict = {
                'h': int(h * 360),
                's': int(s * 100),
                'l': int(l * 100)
            }
            
            if l > 0.90: role = "Background"
            elif l < 0.10: role = "Text/Dark"
            elif s > 0.5: role = "Accent"
            else: role = "Secondary"
            
            name = self._get_color_name(h, l, s)

            colors_data.append({
                "name": name,
                "hex": hex_code,
                "rgb": list(rgb),
                "hsl": hsl_dict, # <--- Dictionary, not list
                "percentage": percentage,
                "role": role
            })

        if colors_data:
            colors_data[0]['role'] = 'Primary'
            
        return {
            "colors": colors_data,
            "analysis": {
                "color_scheme": "Generated Scheme",
                "temperature": "Warm" if any(c['name'] in ['Red', 'Orange', 'Yellow'] for c in colors_data[:3]) else "Cool",
                "accessibility": ["AA Large", "AA Normal"]
            }
        }

    def generate_design_tokens(self, palette_data):
        colors_list = palette_data['colors'] if isinstance(palette_data, dict) else palette_data
            
        tokens = {}
        for i, color in enumerate(colors_list):
            role_key = color.get('role', 'secondary').lower().replace('/', '-')
            key = f"color-{role_key}-{i+1}"
            tokens[key] = {
                "value": color['hex'],
                "type": "color",
                "comment": f"{color.get('name', 'Color')} - {color.get('percentage', 0)}% coverage"
            }
        return tokens

    def export_css_variables(self, tokens):
        # Generate CSS block
        css = ":root {\n"
        for name, token in tokens.items():
            css += f"  --{name}: {token['value']};\n"
        css += "}"
        return css

    def _get_color_name(self, h, l, s):
        if l < 0.1: return "Black"
        if l > 0.9: return "White"
        if s < 0.1: return "Gray"
        hue_deg = h * 360
        if hue_deg < 30: return "Red"
        if hue_deg < 90: return "Yellow"
        if hue_deg < 150: return "Green"
        if hue_deg < 210: return "Cyan"
        if hue_deg < 270: return "Blue"
        if hue_deg < 330: return "Magenta"
        return "Red"