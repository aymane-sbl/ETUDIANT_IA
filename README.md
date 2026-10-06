# 🎓 ETUDIANT-IA

ETUDIANT-IA is an independent educational platform designed to centralize academic resources for students in **Computer Science and Artificial Intelligence**.

The platform provides free access to educational materials such as:

- 📚 Courses (`COURS`)
- 📝 Tutorials / TD (`TD`)
- 🎓 Exams (`EXAM`)
- 🔎 Subject search
- 🗂️ Filtering by semester and resource type
- 📥 Direct PDF downloads

Public academic resources can currently be accessed **without creating an account**.

Administration features are separated from the public platform and protected using JWT-based authentication.

---

## 🌐 Live Application

Frontend:

`https://etudiant-ia.pages.dev`

The frontend currently communicates with the deployed API configured in:

`Frontend/js/utils/init_api.js`

Current production API:

`https://api--etudiant-ia--4rb7wvfyhphp.code.run`

---

## ✨ Features

### Public Features

Students and visitors can:

- Browse the latest academic resources
- Navigate through paginated results
- Search resources by subject name
- Filter resources by semester and resource type
- View subject, semester, academic year, resource type, and exam session
- Download PDF files directly
- Access resources without authentication

### Administration Features

Authenticated administrators can currently:

- Login to the administration area
- Upload new academic resources
- Select the associated subject
- Select semester
- Select academic year
- Select resource type
- Select exam session
- Upload PDF files
- View recently uploaded resources
- Delete resources

Uploaded files are stored using an **S3-compatible object storage service**.

---

## 🔐 Authentication

The project uses JWT authentication.

Authentication endpoint:

```http
POST /api/v1/auth/login
```

Request:

```json
{
  "email": "admin@example.com",
  "password": "password"
}
```

Successful response:

```json
{
  "success": true,
  "message": "Connexion reussie.",
  "role": "admin",
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

The JWT currently contains:

```json
{
  "sub": "user@example.com",
  "role": "admin",
  "exp": "..."
}
```

The token expires after **30 days**.

Passwords are never stored directly. They are hashed using **Argon2**.

JWT tokens use `HS256` with the secret defined through:

```env
SECRET_TOKEN=...
```

---

## 🚫 Registration Policy

Public registration is intentionally **disabled at the moment**.

This is expected behavior.

Currently, regular visitors do not need accounts because educational resources are publicly accessible.

Account creation is reserved for administration purposes.

The registration implementation still exists internally in the Backend, but its route is commented out in:

`Backend/auth/router/auth_router.py`

The registration service is also preserved in:

`Backend/auth/services/auth_service.py`

This allows registration functionality to be temporarily re-enabled when an administrator needs to create a new account.

After the required account is created, public registration can remain disabled again.

Therefore, the current authentication model is:

```text
Visitor
   │
   ├── Browse resources
   ├── Search resources
   ├── Filter resources
   └── Download resources
          │
          └── No account required


Administrator
   │
   └── Login
        │
        └── JWT Token
             │
             └── Administration area
```

The existing registration implementation should **not be considered a public user registration feature**.

> Note: the commented Backend registration route is currently named `/regiter`. If registration is formally reintroduced later, it should preferably be renamed to `/register`.

---

## 👤 Roles

The database currently supports two roles:

```text
admin
user
```

Defined as:

```sql
role ENUM("admin", "user") DEFAULT "user"
```

Administration authorization is checked using the JWT `role` field.

The current authorization helper is located at:

`Backend/admin/utils/check_admin.py`

and only accepts:

```text
role == "admin"
```

---

## 🏗️ Architecture

The project follows a separated Frontend / Backend architecture.

```text
                        ┌─────────────────────┐
                        │      Browser        │
                        │ HTML / CSS / JS     │
                        └─────────┬───────────┘
                                  │
                                  │ HTTP / JSON
                                  ▼
                        ┌─────────────────────┐
                        │      FastAPI        │
                        │      REST API       │
                        └─────────┬───────────┘
                                  │
                 ┌────────────────┼─────────────────┐
                 │                │                 │
                 ▼                ▼                 ▼
          ┌────────────┐   ┌────────────┐   ┌──────────────┐
          │   MySQL    │   │   Redis    │   │ S3 Storage   │
          │            │   │            │   │              │
          │ Metadata   │   │ Cache /    │   │ PDF files    │
          │ Users      │   │ Rate Limit │   │              │
          └────────────┘   └────────────┘   └──────────────┘
```

---

## 🛠️ Technology Stack

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- ES Modules
- Fetch API
- LocalStorage
- SweetAlert
- Responsive UI

No JavaScript frontend framework is currently required.

### Backend

- Python
- FastAPI
- Uvicorn
- Gunicorn
- Pydantic
- aiomysql
- Redis
- FastAPI Cache
- python-jose
- Argon2
- boto3
- python-dotenv

### Database

- MySQL

### Cache & Rate Limiting

- Redis

Redis is used for:

- API caching
- Authentication rate limiting
- IP rate limiting
- Language messages

### File Storage

Academic PDF files are stored using an S3-compatible service through `boto3`.

Bucket currently used by the application:

```text
etudiantia
```

---

## 📁 Project Structure

```text
ETUDIANT_IA/
│
├── Backend/
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── .env.example
│   │
│   ├── auth/
│   │   ├── router/
│   │   │   └── auth_router.py
│   │   ├── schemas/
│   │   │   └── auth_schemas.py
│   │   ├── services/
│   │   │   └── auth_service.py
│   │   └── utils/
│   │       ├── securite.py
│   │       └── email_rate_limit.py
│   │
│   ├── admin/
│   │   ├── router/
│   │   │   ├── manage_material_router.py
│   │   │   └── manage_subjects_router.py
│   │   ├── services/
│   │   │   ├── manage_material_service.py
│   │   │   └── manage_subjects_service.py
│   │   └── utils/
│   │       ├── boto3.py
│   │       └── check_admin.py
│   │
│   ├── users/
│   │   ├── router/
│   │   │   └── material_router.py
│   │   └── services/
│   │       └── material_service.py
│   │
│   ├── middleware/
│   │   └── rate_limite.py
│   │
│   ├── shared/
│   │   ├── database/
│   │   │   ├── db.py
│   │   │   └── redis.py
│   │   ├── dependencies/
│   │   ├── errors/
│   │   └── models/
│   │       ├── init_tables.py
│   │       ├── users_table.py
│   │       ├── subjects_table.py
│   │       └── material_table.py
│   │
│   └── lang/
│       └── fr.json
│
└── Frontend/
    │
    ├── index.html
    ├── robots.txt
    ├── sitemap.xml
    │
    ├── assets/
    │   └── images/
    │
    ├── css/
    │   ├── admin/
    │   ├── components/
    │   └── pages/
    │
    ├── pages/
    │   ├── a_propos.html
    │   ├── admin/
    │   │   └── materials.html
    │   └── auth/
    │       ├── login.html
    │       └── regsiter.html
    │
    └── js/
        ├── app.js
        ├── component/
        ├── services/
        ├── utils/
        └── views/
```

---

## 🗄️ Database

The Backend automatically initializes the required tables when FastAPI starts.

The initialization is handled by:

`Backend/shared/models/init_tables.py`

Three main tables currently exist.

### Users

Table: `users`

| Field | Type | Description |
|---|---|---|
| id | INT | Primary key |
| email | VARCHAR(255) | Unique email |
| password | VARCHAR(255) | Argon2 password hash |
| role | ENUM | `admin` or `user` |
| is_verified | BOOLEAN | Verification state |
| created_at | TIMESTAMP | Creation date |

The default role is `user`.

The `is_verified` field currently exists in the database schema but is not actively used by the current login flow.

### Subjects

Table: `subjects`

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| subject_name | VARCHAR(255) | Unique subject name |

A MySQL `FULLTEXT` index is created on `subject_name` and is used for resource search.

### Materials

Table: `materials`

| Field | Type | Description |
|---|---|---|
| id | INT | Primary key |
| subject_id | INT | Foreign key |
| semester | INT | Semester |
| year_academic | VARCHAR | Academic year |
| type | ENUM | COURS / TD / EXAM |
| session | ENUM | Normal / Rattrapage / none |
| file_url | TEXT | Public resource URL |

Relationship:

```text
subjects
    │
    │ 1
    │
    └────────── *
              materials
```

Deleting a subject automatically deletes the related material records because the foreign key uses:

```sql
ON DELETE CASCADE
```

---

## 🔌 API Documentation

FastAPI automatically provides interactive API documentation.

After starting the Backend:

`http://127.0.0.1:8000/docs`

### Authentication API

#### Login

```http
POST /api/v1/auth/login
```

Content-Type:

```text
application/json
```

Body:

```json
{
  "email": "admin@example.com",
  "password": "password"
}
```

Possible status codes:

```text
200  Login successful
400  Invalid authentication information
429  Too many attempts
500  Internal/database error
```

### Materials API

#### Get Materials

```http
GET /api/v1/materials/
```

Query parameters:

```text
page
limit
```

Example:

```http
GET /api/v1/materials/?page=1&limit=20
```

Default values:

```text
page = 1
limit = 20
```

The minimum accepted `limit` is currently `5`.

Example response:

```json
{
  "success": true,
  "pagination": {
    "current_page": 1,
    "limit": 20,
    "total_pages": 3,
    "total_items": 42
  },
  "data": []
}
```

#### Filter Materials

```http
GET /api/v1/materials/filter
```

Required parameters:

```text
type
semester
```

Example:

```http
GET /api/v1/materials/filter?type=EXAM&semester=3
```

Supported material types:

```text
COURS
TD
EXAM
```

### Search

```http
GET /api/v1/materials/search
```

Parameter:

```text
subject_name
```

Example:

```http
GET /api/v1/materials/search?subject_name=Python
```

The search system currently uses two strategies.

For search terms shorter than 3 characters:

```sql
LIKE
```

For search terms containing 3 or more characters:

```sql
MATCH(subject_name) AGAINST(...)
```

using the MySQL FULLTEXT index.

### Subjects

#### Get Subjects

```http
GET /api/v1/admin/subjects/
```

Returns the available subjects ordered by ID.

Example response:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "subject_name": "Algorithmique"
    }
  ]
}
```

Despite currently being located under `/admin/`, this endpoint does not require JWT authentication in the current implementation.

---

## 🛡️ Admin Materials API

### Add Material

```http
POST /api/v1/admin/materials/
```

Authentication:

```http
Authorization: Bearer <JWT_TOKEN>
```

The authenticated account must have:

```text
role = admin
```

Request type:

```text
multipart/form-data
```

Required fields:

```text
subject_id
semester
year_academic
type
session
file
```

Example:

```text
subject_id: 2
semester: 3
year_academic: 2026-2027
type: EXAM
session: Normal
file: exam.pdf
```

The uploaded document is sent to the configured S3-compatible storage and its URL is stored in MySQL.

### Delete Material

```http
DELETE /api/v1/admin/materials/?id=10
```

The endpoint deletes the corresponding database material record.

#### ⚠️ Current Security Note

Despite being an admin endpoint, the current Backend implementation does **not** apply `decode_token` or `check_is_admin` to the DELETE route.

Therefore this route should be protected before production usage.

The intended behavior should be:

```text
Request
   ↓
JWT verification
   ↓
Extract role
   ↓
role == admin ?
   ├── YES → Delete
   └── NO  → 401 / 403
```

---

## 📦 File Upload Flow

When an administrator uploads a resource:

```text
Admin form
     │
     ▼
FastAPI
     │
     ├── Validate JWT
     ├── Validate admin role
     │
     ▼
S3-compatible Storage
     │
     └── PDF uploaded
             │
             ▼
        Public file URL
             │
             ▼
          MySQL
```

Storage path format:

```text
materials/semeter_<semester>/subject_<subject_id>/<type>/<filename>
```

---

## ⚡ Redis

Redis currently has several responsibilities.

### API Cache

The following caches exist:

```text
HOME_CACHE
FILTER_CACHE
SEARCH_CACHE
SUBJECTS_CACHE
```

Current expiration times include:

```text
Materials list: 24 hours
Filter results: 24 hours
Search results: 30 minutes
Subjects: 24 hours
```

When a new material is uploaded, the application clears:

```text
HOME_CACHE
FILTER_CACHE
SEARCH_CACHE
```

### Authentication Rate Limit

Authentication attempts are limited by email.

Current limit:

```text
5 attempts / 5 minutes
```

Redis key format:

```text
ETUDIANT_IA:auth_limit:<email>
```

After exceeding the limit, the API returns:

```text
HTTP 429 Too Many Requests
```

### Global IP Rate Limit

API calls are also limited by client IP.

Current limit:

```text
50 API requests / minute / IP
```

Redis key:

```text
ETUDIANT_IA:<IP>
```

The middleware only applies to URLs beginning with `/api/`.

---

## 🌍 CORS

The Backend currently allows requests from:

```text
http://127.0.0.1:5500
https://etudiant-ia.pages.dev
```

This configuration is located in:

`Backend/main.py`

---

## ⚙️ Environment Variables

Copy:

`Backend/.env.example`

to:

`Backend/.env`

Required configuration:

```env
# MySQL
HOST=127.0.0.1
USER=root
PASSWORD=password
DB=db_name

# Redis
REDIS_URL=redis://default@127.0.0.1:6379

# S3-compatible storage
ACCESS_KEY=access_key
SECRET_KEY=secret_key
ENDPOINTS=https://your-storage-endpoint
SUBDOMAIN=https://your-public-storage-domain

# JWT
SECRET_TOKEN=your_secure_secret
```

Never commit the real `.env` file.

---

## 🚀 Running the Project Locally

### Requirements

Before starting the project, install:

- Python
- MySQL
- Redis
- A configured S3-compatible storage service

### Backend Setup

Enter the Backend directory:

```bash
cd Backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```bash
cp .env.example .env
```

Configure the environment variables.

Then start the development server:

```bash
uvicorn main:app --reload
```

Backend:

`http://127.0.0.1:8000`

Swagger:

`http://127.0.0.1:8000/docs`

The project should be started from inside the `Backend` directory because some application paths, including the language file, are currently relative to that directory.

### Frontend Setup

The Frontend is static and can be served using a local development server such as VS Code Live Server.

The Backend CORS configuration currently expects the development Frontend at:

`http://127.0.0.1:5500`

For local API development, edit:

`Frontend/js/utils/init_api.js`

Production currently uses:

```javascript
const subdomaine =
  "https://api--etudiant-ia--4rb7wvfyhphp.code.run";
```

A local URL already exists in the file as a commented line:

```javascript
// const subdomaine = "http://127.0.0.1:8000";
```

Use the local value during local Backend development.

---

## 🏭 Production

The Backend includes a `Procfile` configured to run:

```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The public Frontend is configured for:

`https://etudiant-ia.pages.dev`

SEO support currently includes:

- `robots.txt`
- `sitemap.xml`
- Open Graph metadata
- Twitter metadata
- Schema.org structured data
- Google Search Console verification

---

## 🔒 Security

The application currently implements:

- Argon2 password hashing
- JWT authentication
- Role-based admin verification for material uploads
- Authentication rate limiting
- Global IP rate limiting
- Environment-based secrets
- SQL parameter binding
- Restricted CORS origins

---

## ⚠️ Current Technical Notes

### 1. Registration is intentionally disabled

This is intentional.

The public platform currently does not require student accounts.

Registration code is preserved only so administration can temporarily create accounts when necessary.

### 2. DELETE material authorization

`DELETE /api/v1/admin/materials/` currently needs JWT + admin-role protection.

This should have high priority.

### 3. Registration route naming

The disabled route currently uses:

`/regiter`

A future implementation should preferably use:

`/register`

### 4. Register schema

`RegisterSchemas` currently contains:

```text
email
password
role
created_at
```

while the existing registration service only needs:

```text
email
password
```

If account management is redesigned as an Admin feature, it would be better to introduce a dedicated Admin user-creation endpoint and schema.

### 5. Admin page protection

Frontend redirection or checking `localStorage` should never be considered sufficient authorization.

Security-sensitive operations must always be validated by the Backend.

The material upload endpoint already follows this rule.

### 6. Cache invalidation after deletion

Adding a material clears material caches.

Deleting a material currently does not clear those caches.

This could temporarily return cached deleted resources until the cache expires.

### 7. Subjects management

The current Admin Subjects API provides `GET subjects`, but no active API for creating, updating, or deleting subjects.

Subjects therefore need to already exist in the database or be managed separately.

### 8. Database SSL

The MySQL connection currently creates an SSL context with hostname and certificate verification disabled.

This may be acceptable for some development/provider configurations, but production certificate verification should preferably be enabled when supported.

### 9. API URL configuration

The production API domain is currently hard-coded in:

`Frontend/js/utils/init_api.js`

A future improvement would be to centralize environment-specific API configuration.

---

## 🗺️ Possible Future Improvements

Potential next steps for ETUDIANT-IA include:

```text
Admin user management
        │
        ├── Create accounts
        ├── Delete accounts
        └── Change roles

Subject management
        │
        ├── Add subject
        ├── Edit subject
        └── Delete subject

Material management
        │
        ├── Upload
        ├── Update
        └── Delete

Authentication
        │
        ├── Logout
        ├── Password reset
        └── Optional student accounts

Platform
        │
        ├── Improved search
        ├── More filters
        ├── Resource statistics
        └── Admin dashboard
```

---

## 👨‍💻 Author

**Aymane Sabil Allah**

ETUDIANT-IA was created as an independent student project with the goal of centralizing and simplifying access to academic resources for Computer Science and Artificial Intelligence students.

---

## 📌 Project Status

ETUDIANT-IA is currently under active development.

The current architecture already provides:

```text
Public educational resources
          +
FastAPI REST API
          +
MySQL persistence
          +
Redis caching
          +
JWT authentication
          +
Admin resource management
          +
S3 PDF storage
```

Additional administration and account-management functionality can be introduced progressively as the platform evolves.
