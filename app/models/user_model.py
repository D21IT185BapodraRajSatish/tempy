class User:
    # Dummy user data, replace with actual logic to fetch from a database
    users_db = {
        "testuser": {
            "username": "testuser",
            "password": "$2a$12$ATS/e8MHp/ZfKxWoZ.Ff4uTBMp6q7y3b1GrCTJpaQIKVc1VLrCjzC"  # Example hashed password
        }
    }
    
    @staticmethod
    def get_user(username: str):        
        return User.users_db.get(username)  # This returns a dictionary
