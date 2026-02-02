import requests

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api", timeout=10):
        self.base_url = base_url
        self.token = None
        self.timeout = timeout
        self.session = requests.Session()
    
    def set_token(self, token):
        """Set authentication token"""
        self.token = token
        self.session.headers.update({'Authorization': f'Token {token}'})
    
    def clear_token(self):
        """Clear authentication token"""
        self.token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    # Auth endpoints
    def login(self, username, password):
        """Login and get token"""
        response = self.session.post(
            f"{self.base_url}/auth/login/",
            json={'username': username, 'password': password},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        self.set_token(data['token'])
        return data
    
    def register(self, username, email, password):
        """Register new user"""
        response = self.session.post(
            f"{self.base_url}/auth/register/",
            json={'username': username, 'email': email, 'password': password},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        self.set_token(data['token'])
        return data
    
    def logout(self):
        """Logout and clear token"""
        try:
            self.session.post(f"{self.base_url}/auth/logout/", timeout=self.timeout)
        except:
            pass
        self.clear_token()
    
    def get_profile(self):
        """Get user profile"""
        response = self.session.get(f"{self.base_url}/auth/profile/", timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    # Data endpoints
    def get_history(self):
        """Get upload history"""
        response = self.session.get(f"{self.base_url}/history/", timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def upload_file(self, file_path):
        """Upload CSV file"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(
                f"{self.base_url}/upload/",
                files=files,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
    
    def get_summary(self, batch_id):
        """Get dataset summary and data"""
        response = self.session.get(
            f"{self.base_url}/summary/{batch_id}/",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
    
    def get_report_url(self, batch_id):
        """Get PDF report URL"""
        return f"{self.base_url}/report/{batch_id}/"

    def download_report(self, batch_id, save_path=None):
        """Download PDF report for batch_id and save to save_path.

        If save_path is None, returns raw bytes.
        """
        url = self.get_report_url(batch_id)
        resp = self.session.get(url, stream=True, timeout=self.timeout)
        resp.raise_for_status()

        if save_path is None:
            return resp.content

        # Stream to file
        with open(save_path, 'wb') as fd:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    fd.write(chunk)
        return save_path
