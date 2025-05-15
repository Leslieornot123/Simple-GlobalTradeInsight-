import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv

load_dotenv()

class Auth:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
        self.users_file = 'users.json'
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_token(self, username):
        """Create JWT token"""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['username']
        except:
            return None
    
    def register(self, username, password, email):
        """Register new user"""
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = {
            'password': self.hash_password(password),
            'email': email,
            'created_at': datetime.now().isoformat()
        }
        self.save_users()
        return True, "Registration successful"
    
    def login(self, username, password):
        """Login user"""
        if username not in self.users:
            return False, "Invalid username or password"
        
        if self.users[username]['password'] != self.hash_password(password):
            return False, "Invalid username or password"
        
        token = self.create_token(username)
        return True, token
    
    def get_user(self, username):
        """Get user details"""
        return self.users.get(username)
    
    def update_user(self, username, **kwargs):
        """Update user details"""
        if username not in self.users:
            return False, "User not found"
        
        for key, value in kwargs.items():
            if key == 'password':
                self.users[username][key] = self.hash_password(value)
            else:
                self.users[username][key] = value
        
        self.save_users()
        return True, "User updated successfully"
    
    def delete_user(self, username):
        """Delete user"""
        if username not in self.users:
            return False, "User not found"
        
        del self.users[username]
        self.save_users()
        return True, "User deleted successfully"

    def guest_login(self):
        """Create a guest user session"""
        guest_username = "guest_" + datetime.now().strftime("%Y%m%d%H%M%S")
        guest_token = self.create_token(guest_username)
        return True, guest_token 