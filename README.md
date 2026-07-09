# Minor - Educational Resource Platform

A comprehensive Django-based platform for managing and sharing educational resources among college students. Organize notes, textbooks, past question papers, syllabi, and connect through a community Q&A forum.

![Django](https://img.shields.io/badge/Django-6.0-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 Features

### 📚 **Notes Management**
- Upload and organize study notes by branch, semester, and subject
- Track download counts and user engagement
- Support for PDF files and external links
- Tagged organization for easy discovery

### 📖 **Digital Book Library**
- Curated collection of textbooks and reference materials
- 5-star rating system
- Customizable cover gradients
- Links to PDF resources

### 📝 **Previous Year Questions (PYQ)**
- Past exam papers organized by:
  - Subject
  - Branch
  - Semester
  - Year
  - Exam type (Mid-Sem, End-Sem, Backlog)

### 📋 **Syllabus Management**
- Subject-wise syllabi with unit breakdowns
- JSON-based flexible structure
- PDF and link support

### ❓ **Community Doubts Forum**
- Post questions and get answers from peers
- Mark best answers
- Auto-expiry system (2 days for solved, 7 days for unsolved)
- View tracking

### 👤 **User Profiles**
- Custom user roles (Student, Super Student, Admin)
- Branch and semester association
- Profile customization (bio, avatar)

### 🔖 **Bookmarks**
- Save favorite notes for quick access
- Personalized resource management

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 6.0 |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Authentication** | Django Auth (Custom User Model) |
| **Deployment** | Cloudflare Tunnel (HTTPS) |
| **Admin Panel** | Django Admin |

---

## 📋 Prerequisites

- Python 3.9+
- pip (Python package manager)
- Git

---

0
## 📁 Project Structure

```
minor/
├── minor/                 # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL router
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
│
├── core/                  # Core app - Models and logic
│   ├── models.py         # User, Note, Book, PYQ, Syllabus, Doubt, Reply, Bookmark
│   ├── admin.py          # Admin panel configuration
│   ├── views.py          # Core views
│   └── migrations/       # Database migrations
│
├── api/                   # API endpoints
│   ├── urls.py           # API routes
│   ├── views.py          # API views
│   └── views_download_note_snippet.py
│
├── accounts/             # Authentication system
│   ├── urls.py           # Auth routes (login, register, logout)
│   ├── views.py          # Auth views
│   ├── views_auth.py     # Additional auth views
│   └── forms.py          # Login/Register forms
│
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── notes.html        # Notes listing
│   ├── books.html        # Books catalog
│   ├── pyq.html          # Past papers
│   ├── syllabus.html     # Syllabi
│   ├── doubts.html       # Q&A forum
│   ├── profile.html      # User profile
│   ├── search.html       # Search results
│   └── registration/     # Auth templates
│
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       ├── data.js       # Data management
│       ├── swipe.js      # Touch swipe support
│       └── csrf.js       # CSRF token handling
│
├── media/                # User uploads
│   ├── notes/            # PDF notes
│   ├── books/            # Book files
│   ├── pyqs/             # Question papers
│   └── syllabi/          # Syllabus files
│
├── manage.py             # Django management script
├── db.sqlite3            # SQLite database
└── README.md             # This file
```

---

## 🗄️ Database Models

### **User**
- Custom user model extending Django's AbstractUser
- Fields: role, branch, semester, college, bio, avatar

### **Branch**
- Code (e.g., 'CSE', 'ECE')
- Name (e.g., 'Computer Science')

### **Note**
- Title, subject, branch, semester, unit
- PDF file or external link
- Download count tracking
- Tags for categorization

### **Book**
- Title, author, subject, rating
- Cover gradient styling
- PDF support

### **PYQ**
- Subject, branch, semester, year
- Exam type (Mid-Sem, End-Sem, Backlog)

### **Syllabus**
- Subject code and name
- JSON-based unit structure
- Branch and semester specific

### **Doubt**
- Title, description, subject
- Question-answer format with best answer marking
- Auto-expiry functionality
- View counter

### **Reply**
- Answer to doubts
- Best answer marking
- User attribution

### **Bookmark**
- User saves for notes
- Unique per user-note pair

---

## 🔐 Security Features

- ✅ CSRF protection enabled
- ✅ Secure HTTP-only cookies
- ✅ X-Forwarded headers for Cloudflare
- ✅ SSL/TLS support (HTTPS)
- ✅ CORS configuration for trusted origins
- ✅ Role-based access control (Student, Super Student, Admin)

---

## 📍 URL Endpoints

### Authentication
- `GET/POST /accounts/login/` - User login
- `GET/POST /accounts/register/` - User registration
- `GET /accounts/logout/` - User logout

### Pages
- `GET /` - Home page
- `GET /notes/` - Notes listing
- `GET /books/` - Books catalog
- `GET /pyq/` - Past papers
- `GET /syllabus/` - Syllabi
- `GET /doubts/` - Q&A forum
- `GET /profile/` - User profile
- `GET /search/?q=query` - Search results

### API
- `GET /api/...` - API endpoints (defined in api/urls.py)

### Admin
- `GET /admin/` - Django admin panel

---

## 🚀 Deployment

### Cloudflare Tunnel
The application is configured to work with Cloudflare Tunnel for secure HTTPS access.

**Key Settings:**
- `ALLOWED_HOSTS` includes Cloudflare tunnel domain
- `CSRF_TRUSTED_ORIGINS` configured for Cloudflare
- `SECURE_PROXY_SSL_HEADER` set for HTTPS detection
- `USE_X_FORWARDED_HOST` enabled

**To Deploy:**
1. Install Cloudflare Tunnel
2. Create tunnel: `cloudflared tunnel create minor`
3. Configure `config.yml`
4. Run: `cloudflared tunnel run minor`

--
## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

## 🎯 Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced search with filters
- [ ] Student collaboration features
- [ ] AI-powered doubt resolution suggestions
- [ ] Performance optimization
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Social sharing features

---

**Happy Learning! 📚**
