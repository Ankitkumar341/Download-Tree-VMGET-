import requests
import os
from datetime import datetime
import json

class PinterestDownloader:
    def __init__(self):
        self.output_dir = 'downloads/pinterest'
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url, quality):
        try:
            pin_id = self._extract_pin_id(url)
            api_url = f"https://api.pinterest.com/v3/pins/{pin_id}/"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(api_url, headers=headers)
            data = response.json()
            
            if 'resource_response' in data and 'data' in data['resource_response']:
                pin_data = data['resource_response']['data']
                image_url = self._get_image_url(pin_data, quality)
                
                if image_url:
                    filename = f"pin_{pin_id}_{quality}.jpg"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        image_response = requests.get(image_url, headers=headers)
                        f.write(image_response.content)
                    
                    return {
                        'status': 'success',
                        'pin_id': pin_id,
                        'quality': quality,
                        'filename': filename,
                        'timestamp': datetime.now().isoformat()
                    }
            
            raise Exception("Could not find image data")
        except Exception as e:
            raise Exception(f"Pinterest download failed: {str(e)}")

    def _extract_pin_id(self, url):
        # Extract pin ID from Pinterest URL
        parts = url.split('/')
        pin_part = [p for p in parts if p.startswith('pin')]
        if pin_part:
            return pin_part[0].split('-')[1]
        raise Exception("Invalid Pinterest URL")

    def _get_image_url(self, pin_data, quality):
        quality_map = {
            'Original Quality': 'original',
            'High Quality': 'high',
            'Medium Quality': 'medium'
        }
        
        if 'images' in pin_data:
            return pin_data['images'][quality_map[quality]]['url']
        return None