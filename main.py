import requests
import json
import time
from typing import List, Dict
import logging
import sys

class ZealyNotifier:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://api.zealy.io"
        self.telegram_base_url = "https://api.telegram.org"
        self.previous_tasks = {}
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup(self) -> bool:
        """Initial setup and configuration"""
        try:
            # Get user inputs
            self.cookie = input("Enter Zealy cookie header string: ")
            self.telegram_token = input("Enter Telegram bot API token: ")
            self.chat_id = input("Enter Telegram chat ID: ")
            
            communities = input("Enter community names (comma-separated): ")
            self.communities = [c.strip() for c in communities.split(",")]
            
            # Validate inputs
            if not all([self.cookie, self.telegram_token, self.chat_id, self.communities]):
                raise ValueError("All inputs are required")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Setup failed: {str(e)}")
            return False

    def login(self) -> bool:
        """Login to Zealy using cookie"""
        try:
            headers = {
                "Cookie": self.cookie,
                "User-Agent": "Mozilla/5.0"
            }
            self.session.headers.update(headers)
            
            # Test login by getting user profile
            response = self.session.get(f"{self.base_url}/v1/users/me")
            if response.status_code == 200:
                user_data = response.json()
                self.username = user_data.get("username")
                self.logger.info(f"Logged in as: {self.username}")
                return True
            else:
                self.logger.error("Login failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            return False

    def test_telegram_bot(self) -> bool:
        """Test Telegram bot connection"""
        try:
            url = f"{self.telegram_base_url}/bot{self.telegram_token}/getMe"
            response = requests.get(url)
            
            if response.status_code == 200:
                self.logger.info("Telegram bot connection successful")
                return True
            else:
                self.logger.error("Telegram bot connection failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Telegram bot test failed: {str(e)}")
            return False

    def send_telegram_message(self, message: str):
        """Send message to Telegram"""
        try:
            url = f"{self.telegram_base_url}/bot{self.telegram_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data)
            
            if response.status_code != 200:
                self.logger.error("Failed to send Telegram message")
                
        except Exception as e:
            self.logger.error(f"Telegram send error: {str(e)}")

    def get_community_tasks(self, community: str) -> List[Dict]:
        """Get tasks for a specific community"""
        try:
            response = self.session.get(f"{self.base_url}/v1/communities/{community}/quests")
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception as e:
            self.logger.error(f"Error getting tasks for {community}: {str(e)}")
            return []

    def monitor_tasks(self):
        """Main monitoring loop"""
        self.logger.info("Starting task monitoring...")
        
        while True:
            try:
                for community in self.communities:
                    current_tasks = self.get_community_tasks(community)
                    
                    if community not in self.previous_tasks:
                        self.previous_tasks[community] = current_tasks
                        continue
                    
                    # Check for new tasks
                    new_tasks = [task for task in current_tasks 
                               if task not in self.previous_tasks[community]]
                    
                    # Check for removed tasks
                    removed_tasks = [task for task in self.previous_tasks[community] 
                                   if task not in current_tasks]
                    
                    # Send notifications
                    if new_tasks:
                        for task in new_tasks:
                            message = (
                                f"🆕 New task in {community}:\n"
                                f"Title: {task['title']}\n"
                                f"XP: {task['xp']}"
                            )
                            self.send_telegram_message(message)
                    
                    if removed_tasks:
                        for task in removed_tasks:
                            message = (
                                f"❌ Removed task in {community}:\n"
                                f"Title: {task['title']}\n"
                                f"XP: {task['xp']}"
                            )
                            self.send_telegram_message(message)
                    
                    self.previous_tasks[community] = current_tasks
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")
                time.sleep(60)  # Wait before retrying

def main():
    notifier = ZealyNotifier()
    
    # Initial setup
    if not notifier.setup():
        sys.exit(1)
    
    # Login check
    if not notifier.login():
        sys.exit(1)
    
    # Test Telegram bot
    if not notifier.test_telegram_bot():
        sys.exit(1)
    
    # Start monitoring
    notifier.monitor_tasks()

if __name__ == "__main__":
    main()
