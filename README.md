# Meeting-Scribe API

A powerful Django REST API for meeting transcription and summarization using Azure services and OpenAI.

## 🚀 Live Demo

**Frontend Application:** [https://meeting-scribe-front.vercel.app/](https://meeting-scribe-front.vercel.app/)

## 📋 Overview

Meeting-Scribe is a comprehensive API that enables users to:

- Upload audio files from meetings
- Automatically transcribe audio using Azure Speech Services or OpenAI Whisper
- Generate intelligent summaries with key points and action items
- Manage user authentication and file storage

## ✨ Features

### 🎯 Core Features

- **Audio File Upload**: Support for multiple audio formats (MP3, WAV, M4A, etc.)
- **Automatic Transcription**: Convert speech to text using Azure Speech Services or OpenAI Whisper
- **Intelligent Summarization**: Extract key points and action items from meeting transcripts
- **User Authentication**: JWT-based authentication system
- **Cloud Storage**: Azure Blob Storage integration for file management
- **RESTful API**: Clean, well-documented API endpoints

### 🔧 Technical Features

- **Format Conversion**: Automatic audio format conversion using FFmpeg
- **Async Processing**: Background task processing for large files
- **Error Handling**: Comprehensive error handling and logging
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Production Ready**: Configured for deployment on Azure

## 🛠️ Technology Stack

### Backend

- **Django 5.2+** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **Celery + Redis** - Background task processing

### AI/ML Services

- **Azure Speech Services** - Speech-to-text transcription
- **OpenAI Whisper** - Alternative transcription service
- **Azure OpenAI** - Text summarization and analysis

### Cloud Services

- **Azure Blob Storage** - File storage
- **Azure App Service** - Hosting
- **Azure Database for PostgreSQL** - Database hosting

### Additional Tools

- **FFmpeg** - Audio processing
- **JWT Authentication** - Secure API access
- **CORS Headers** - Cross-origin support

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for background tasks)
- FFmpeg
- Azure Account
- OpenAI API Key

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/msc2024T/Meeting-Scribe-API.git
   cd Meeting-Scribe-API
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True

   # Database
   DB_NAME=meetingscribe_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432

   # Azure Blob Storage
   AZURE_BLOB_CONNECTION_STRING=your_connection_string
   AZURE_STORAGE_CONTAINER_NAME=your_container_name
   AZURE_STORAGE_ACCOUNT_NAME=your_account_name
   AZURE_STORAGE_KEY=your_storage_key

   # Azure Speech Services
   SPEECH_KEY=your_speech_key
   SERVICE_REGION=your_region

   # OpenAI
   OPENAI_API_KEY=your_openai_key
   OPENAI_API_BASE=https://your-resource.openai.azure.com/
   ```

5. **Database Setup**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

### Authentication Endpoints

```
POST /auth/register/     - User registration
POST /auth/login/        - User login
POST /auth/refresh/      - Refresh JWT token
```

### File Management

```
POST /files/             - Upload audio file
GET /files/              - List user's files
GET /files/{id}/         - Get specific file
DELETE /files/{id}/      - Delete file
```

### Transcription

```
POST /transcriptions/transcriptions/{audio_file_id}/  - Create transcription
GET /transcriptions/transcriptions/{audio_file_id}/   - Get transcription
```

### Summarization

```
POST /summarizer/summarize/{transcription_id}/        - Generate summary
GET /summarizer/summary/{transcription_id}/           - Get summary
```

### Example API Usage

**Upload Audio File:**

```bash
curl -X POST \
  http://localhost:8000/files/ \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@meeting.mp3' \
  -F 'filename=meeting.mp3'
```

**Create Transcription:**

```bash
curl -X POST \
  http://localhost:8000/transcriptions/transcriptions/AUDIO_FILE_ID/ \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json'
```

**Generate Summary:**

```bash
curl -X POST \
  http://localhost:8000/summarizer/summarize/TRANSCRIPTION_ID/ \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json'
```

## 🏗️ Project Structure

```
Meeting-Scribe-API/
├── meetingscribe/          # Django project settings
├── authentication/         # User authentication app
├── files/                  # File management app
├── transcription/          # Audio transcription app
├── summarizer/            # Text summarization app
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── README.md             # This file
```

## 🔧 Configuration

### Audio Processing

- Supports multiple audio formats
- Automatic format conversion using FFmpeg
- File size limits and validation

### Cloud Storage

- Azure Blob Storage integration
- Secure file upload and retrieval
- Automatic file cleanup

### AI Services

- Azure Speech Services for transcription
- OpenAI Whisper as alternative
- Azure OpenAI for summarization

## 🚀 Deployment

### Azure App Service

1. Create Azure App Service
2. Configure environment variables
3. Set up PostgreSQL database
4. Deploy using GitHub Actions or Azure CLI

### Environment Variables (Production)

```env
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@host:port/db
AZURE_BLOB_CONNECTION_STRING=your-connection-string
SPEECH_KEY=your-speech-key
OPENAI_API_KEY=your-openai-key
```

## 🧪 Testing

Run tests with:

```bash
python manage.py test
```

Run with coverage:

```bash
coverage run manage.py test
coverage report
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- [ ] Real-time transcription
- [ ] Multiple language support
- [ ] Speaker identification
- [ ] Meeting analytics dashboard
- [ ] Integration with calendar systems
- [ ] Mobile app support

## 🐛 Known Issues

- Large audio files may take time to process
- Some audio formats may require additional conversion
- Azure services may have rate limits

## 📞 Support

For support, email mohamad.sc66@gmail.com or create an issue on GitHub.

## 🙏 Acknowledgments

- Azure Speech Services for transcription capabilities
- OpenAI for Whisper and GPT models
- Django community for the excellent framework
- Contributors and testers

---

**Frontend Repository:** [Meeting-Scribe-Frontend](https://github.com/msc2024T/Meeting-Scribe-Frontend)

**Live Demo:** [https://meeting-scribe-front.vercel.app/](https://meeting-scribe-front.vercel.app/)
