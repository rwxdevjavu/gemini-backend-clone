# gemini backend clone

This project is a scalable backend API that allows users to send chat messages and receive AI-generated responses (via Google Gemini) using RQ (Redis Queue) for background task processing and Redis for task/result storage.

---

## 🔧 Tech Stack

- **FastAPI** — RESTful web framework
- **RQ (Redis Queue)** — Simple Python job queue using Redis
- **Redis** — Used as both a queue and result storage
- **SQLAlchemy** — ORM for database operations
- **Google Gemini API** — AI response generation

---
## 🚀 How It Works

1. **User sends a message** via `POST /{id}/message`
2. Message is saved to the database
3. Task is enqueued in RQ to get AI response from Gemini
4. Once generated, the response is:
   - Stored in the database
   - Cached in Redis using `chat_response:{chatroom_id}`
5. User polls `GET /{id}/message/response` to get the response

---
## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/chatroom-ai.git
cd chatroom-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure your `requirements.txt` includes:

### 3. Configure `.env` or environment variables

```env
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_api_key_here
```
### 4. Run Redis Server

```bash
redis-server
```

### 5. Start FastAPI App

```bash
uvicorn main:app --reload
```

### 6. Start RQ Worker

```bash
rq worker --with-scheduler --url redis://localhost:6379/0 default
```

---

### 4. Run Redis Server

```bash
redis-server
```

### 5. Start FastAPI App

```bash
uvicorn main:app --reload
```

### 6. Start RQ Worker

```bash
rq worker --with-scheduler --url redis://localhost:6379/0 default
```

---
---

### 7. Stripe Sandbox Payment Setup

1. **Create a Stripe account**  
   [https://dashboard.stripe.com/register](https://dashboard.stripe.com/register)

2. **Get API keys (test mode)**  
   Go to **Developers → API Keys**, and copy your:
   - `STRIPE_SECRET_KEY`

3. **Add to `.env` file**

   ```env
   STRIPE_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXXXXXX
   ```

## 🌐 Deployment Notes

1. **Deploy FastAPI app** as a **Web Service** on [Render](https://render.com), connected to your GitHub repo.
2. **Add Redis** and **PostgreSQL** from Render's managed services.
3. Set environment variables in your Web Service:
- `DATABASE_URL`, `REDIS_URL`, `STRIPE_SECRET_KEY`, etc.
4. **Create a Background Worker** (new Render service) with start command:
```bash
rq worker --with-scheduler --url $REDIS_URL

---


