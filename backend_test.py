import requests
import sys
import time
from datetime import datetime

class RDPStealthAPITester:
    def __init__(self, base_url="https://54f023da-25f7-4bfb-9733-a100cc98eed3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_base}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, params=params)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, params=params)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                self.tests_failed += 1
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response: {response.text}")
                return success, {}

        except Exception as e:
            self.tests_failed += 1
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test the health check endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )

    def test_login(self, username, password, totp_code=None):
        """Test login and get token"""
        data = {"username": username, "password": password}
        if totp_code:
            data["totp_code"] = totp_code
            
        success, response = self.run_test(
            "Login",
            "POST",
            "auth/login",
            200,
            data=data
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_get_current_user(self):
        """Test getting current user info"""
        return self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )

    def test_dashboard_stats(self):
        """Test getting dashboard statistics"""
        return self.run_test(
            "Dashboard Stats",
            "GET",
            "dashboard/stats",
            200
        )

    def test_current_metrics(self):
        """Test getting current system metrics"""
        return self.run_test(
            "Current Metrics",
            "GET",
            "dashboard/metrics/current",
            200
        )

    def test_rdp_connections(self):
        """Test listing RDP connections"""
        return self.run_test(
            "List RDP Connections",
            "GET",
            "rdp/connections",
            200
        )

    def test_create_rdp_connection(self, host, username, password):
        """Test creating an RDP connection"""
        data = {
            "host": host,
            "port": 3389,
            "username": username,
            "password": password,
            "quality": "high"
        }
        return self.run_test(
            "Create RDP Connection",
            "POST",
            "rdp/connections",
            200,
            data=data
        )

    def test_active_sessions(self):
        """Test getting active sessions"""
        return self.run_test(
            "Active Sessions",
            "GET",
            "sessions/active",
            200
        )

    def test_logs(self):
        """Test getting logs"""
        return self.run_test(
            "Get Logs",
            "GET",
            "logs",
            200
        )

    def test_settings(self):
        """Test getting settings"""
        return self.run_test(
            "Get Settings",
            "GET",
            "settings",
            200
        )

    def test_file_list(self, path="/"):
        """Test listing files"""
        return self.run_test(
            "List Files",
            "GET",
            "files/list",
            200,
            params={"path": path}
        )

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*50)
        print(f"📊 Test Summary:")
        print(f"Total tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        print("="*50)
        
        return self.tests_failed == 0

def main():
    # Setup
    tester = RDPStealthAPITester()
    
    # Test health check (no auth required)
    tester.test_health_check()
    
    # Test authentication
    if not tester.test_login("admin", "admin123"):
        print("❌ Login failed, stopping tests")
        tester.print_summary()
        return 1
    
    # Test authenticated endpoints
    tester.test_get_current_user()
    tester.test_dashboard_stats()
    tester.test_current_metrics()
    tester.test_rdp_connections()
    tester.test_active_sessions()
    tester.test_logs()
    tester.test_settings()
    tester.test_file_list()
    
    # Test creating an RDP connection
    tester.test_create_rdp_connection("example.com", "rdp_user", "rdp_password")
    
    # Print summary
    success = tester.print_summary()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())