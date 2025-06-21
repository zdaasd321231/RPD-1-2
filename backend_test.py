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
            "logs/",
            200
        )
        
    def test_log_levels(self):
        """Test getting log levels"""
        return self.run_test(
            "Get Log Levels",
            "GET",
            "logs/levels",
            200
        )
        
    def test_log_sources(self):
        """Test getting log sources"""
        return self.run_test(
            "Get Log Sources",
            "GET",
            "logs/sources",
            200
        )
        
    def test_log_statistics(self):
        """Test getting log statistics"""
        return self.run_test(
            "Get Log Statistics",
            "GET",
            "logs/statistics",
            200,
            params={"days": 7}
        )

    def test_settings(self):
        """Test getting settings"""
        return self.run_test(
            "Get Settings",
            "GET",
            "settings/",
            200
        )
        
    def test_security_settings(self):
        """Test getting security settings"""
        return self.run_test(
            "Get Security Settings",
            "GET",
            "settings/security",
            200
        )
        
    def test_rdp_settings(self):
        """Test getting RDP settings"""
        return self.run_test(
            "Get RDP Settings",
            "GET",
            "settings/rdp",
            200
        )
        
    def test_file_settings(self):
        """Test getting file settings"""
        return self.run_test(
            "Get File Settings",
            "GET",
            "settings/files",
            200
        )
        
    def test_notification_settings(self):
        """Test getting notification settings"""
        return self.run_test(
            "Get Notification Settings",
            "GET",
            "settings/notifications",
            200
        )
        
    def test_system_settings(self):
        """Test getting system settings"""
        return self.run_test(
            "Get System Settings",
            "GET",
            "settings/system",
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
        
    def test_file_operations(self):
        """Test getting file operations"""
        return self.run_test(
            "Get File Operations",
            "GET",
            "files/operations",
            200
        )
        
    def test_storage_stats(self):
        """Test getting storage stats"""
        return self.run_test(
            "Get Storage Stats",
            "GET",
            "files/storage-stats",
            200
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
    
    # Dashboard endpoints
    tester.test_dashboard_stats()
    tester.test_current_metrics()
    
    # RDP endpoints
    tester.test_rdp_connections()
    tester.test_create_rdp_connection("example.com", "rdp_user", "rdp_password")
    
    # Session endpoints
    tester.test_active_sessions()
    
    # Logs endpoints - specifically mentioned in the test request
    tester.test_logs()
    tester.test_log_levels()
    tester.test_log_sources()
    tester.test_log_statistics()
    
    # Settings endpoints - specifically mentioned in the test request
    tester.test_settings()
    tester.test_security_settings()
    tester.test_rdp_settings()
    tester.test_file_settings()
    tester.test_notification_settings()
    tester.test_system_settings()
    
    # File management endpoints
    tester.test_file_list()
    tester.test_file_operations()
    tester.test_storage_stats()
    
    # Print summary
    success = tester.print_summary()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())