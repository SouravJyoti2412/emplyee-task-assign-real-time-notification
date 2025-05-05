

## Redis Application run 
celery -A app worker --pool=solo --loglevel=info for windows

## Run asgi application
daphne -b 0.0.0.0 -p 8001 app.asgi:application

# Employee Job Tracking System (Django + Channels + Redis)

This project allows real-time tracking of employee job tasks and user updates via WebSockets, using Django REST Framework, Django Channels, and Redis.

---

## 📦 Tech Stack

- Django
- Django REST Framework
- Django Channels
- Redis
- WebSockets
- PostgreSQL/SQLite (default)

---

## 🔌 Requirements

Install via:

```bash
pip install -r requirements.txt
````

Minimum dependencies:

```text
Django>=3.2
djangorestframework
channels
channels-redis
```

Also, ensure Redis is running:

```bash
redis-server
```

---

## 🛠️ Setup

1. Clone this repo

```bash
git clone https://github.com/your-username/employee-job-tracking.git
cd employee-job-tracking
```

2. Create virtual environment

```bash
python -m venv env
source env/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run Redis server (in another terminal)

```bash
redis-server
```

6. Run ASGI server (e.g. Daphne or Uvicorn)

```bash
daphne -b 127.0.0.1 -p 8001 your_project.asgi:application
```

7. Alternatively, run development server (for REST APIs only):

```bash
python manage.py runserver
```

---

## 📁 Endpoints

These URLs are registered in your main `urls.py` like:

```python
from django.urls import path
from employee_job_tracking.views import TaskAPIView, UserSignupLoginAPIView

urlpatterns = [
    path('task/', TaskAPIView.as_view()),
    path('user/', UserSignupLoginAPIView.as_view()),
]
```

### ✅ API URLs:

* `POST /user/` — Register or log in a user
* `POST /task/` — Create a task
* `GET /task/` — List all tasks

---

## 🔁 WebSocket Endpoints

Add in `routing.py`:

```python
from django.urls import re_path
from .consumers import AdminCustomerConsumer, AdminJobConsumer

websocket_urlpatterns = [
    re_path(r"ws/admin-customer/$", AdminCustomerConsumer.as_asgi()),
    re_path(r"ws/admin-jobs/$", AdminJobConsumer.as_asgi()),
]
```

These are handled in `asgi.py` using:

```python
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from employee_job_tracking.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})
```

---

## 🔔 Real-Time Events

* When a `CustomUser` is created or updated, a message is sent to WebSocket group `admin_customer`.
* When a `Task` is created or updated, a message is sent to WebSocket group `admin_jobs`.

---

## 🧪 Test WebSocket Frontend

Basic HTML snippet to test:

```html
<script>
const socket = new WebSocket("ws://127.0.0.1:8001/ws/admin-customer/");

socket.onmessage = function(event) {
  console.log("Message:", JSON.parse(event.data));
};
</script>
```

---

## 📄 License

MIT

```

---

Would you like me to prepare a sample GitHub structure (`tree` view), or zip this as a starter project?
```
