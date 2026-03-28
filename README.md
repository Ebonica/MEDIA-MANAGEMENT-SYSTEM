🎬 MediaHub – Media Management System

A full-stack Media Management System designed to manage, organize, and analyze multimedia content efficiently. This platform enables users to upload videos, manage channels, create playlists, and gain insights through analytics dashboards.

🚀 Project Overview

In today’s digital era, multimedia content plays a crucial role in communication, education, and entertainment. However, existing platforms like YouTube do not provide full control over content and analytics.

MediaHub solves this by offering:
Secure content management
Customizable platform for institutions
Detailed analytics insights
Full ownership of data

🎯 Objectives
Provide a secure platform for managing multimedia content
Enable structured organization via channels and playlists
Support user interaction (likes, comments, subscriptions)
Deliver analytics for performance tracking
Build using scalable and open-source technologies

🧠 System Architecture

The system follows a 3-tier architecture:

1. Presentation Layer (Frontend)
Built using Streamlit
Handles user interaction and UI
Displays analytics using Plotly

3. Application Layer (Backend)
Developed in Python
Handles:
Authentication
Business logic
Data processing
Role-based access control

4. Database Layer
Uses MongoDB (NoSQL)

Stores:
Users
Channels
Videos
Comments
Playlists

🛠️ Tech Stack
Language: Python 3.11
Frontend: Streamlit
Backend: Python
Database: MongoDB
Visualization: Plotly
Libraries: PyMongo, Pandas, NumPy

📦 Features

👤 User Management
Registration & Login
Role-based access (Viewer / Creator)
Profile management

📺 Channel Management
Create, update, delete channels
Track subscribers and views

🎥 Video Management
Upload videos
Add metadata (title, duration, description)
View engagement metrics

💬 Comment System
Add, edit, delete comments
Threaded discussions

📂 Playlist Management
Create and manage playlists
Organize videos efficiently

🔍 Search & Filter
Keyword-based search
Filter by category, creator, date

📊 Analytics Dashboard
View statistics:
Views
Likes
Engagement
Interactive charts using Plotly

🗄️ Database Design
The system is based on an Enhanced Entity Relationship (EER) Model including:

Main Entities:
User (Creator / Viewer)
Channel
Video
Playlist
Comment

Key Relationships:
User → Channel (1:N)
Channel → Video (1:N)
User → Playlist (1:N)
User ↔ Channel (M:N - Subscription)
Video → Comment (1:N)

⚙️ Installation & Setup
# Clone the repository
git clone https://github.com/your-username/mediahub.git

# Navigate to project folder
cd mediahub

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

📸 Screens Included
Login Page
Registration Page
Home Dashboard
Channel Management
Video Upload & Management
Comments Section
Playlist Management
Analytics Dashboard
Account Settings

🔮 Future Enhancements
Video streaming optimization
AI-based recommendations
Advanced analytics (ML models)
Mobile application support
Cloud deployment

📌 Conclusion
MediaHub provides a scalable, flexible, and user-friendly platform for managing multimedia content with complete control and analytics, making it ideal for educational institutions and organizations.

👩‍💻 Author
Ebonica Saleth V
LinkedIn https://www.linkedin.com/in/ebonica-saleth-92b268224/
📜 License
This project is developed for academic and educational purposes.
