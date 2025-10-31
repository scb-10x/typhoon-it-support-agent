# API Reference

Complete reference for the Typhoon IT Support REST API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required for local development. For production, implement:
- API keys
- JWT tokens
- OAuth2

## Endpoints

### Health Check

Check if the server is running.

```http
GET /health
```

**Response**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

**Status Codes**
- `200 OK` - Server is healthy

---

### Standard Chat

Send a message and get a complete response.

```http
POST /chat
Content-Type: application/json
```

**Request Body**
```json
{
  "message": "I need help resetting my password",
  "session_id": "user-123"  // optional
}
```

**Response**
```json
{
  "response": "สวัสดีครับ ผมจะช่วยคุณรีเซ็ตรหัสผ่าน...",
  "session_id": "user-123"
}
```

**Status Codes**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid request body
- `500 Internal Server Error` - Server error

---

### Streaming Chat

Send a message and receive streaming response tokens.

```http
POST /chat/stream
Content-Type: application/json
```

**Request Body**
```json
{
  "message": "My WiFi isn't working",
  "session_id": "user-456"  // optional
}
```

**Response**
```
Content-Type: text/event-stream

data: {"type": "token", "content": "สวัสดี"}

data: {"type": "token", "content": "ครับ"}

data: {"type": "token", "content": " "}

data: {"type": "done"}
```

**Event Types**
- `token` - Individual token from response
- `chunk` - Larger text chunk
- `error` - Error occurred
- `done` - Response complete

**Status Codes**
- `200 OK` - Streaming started
- `400 Bad Request` - Invalid request
- `500 Internal Server Error` - Server error

---

### Create Ticket

Create a new support ticket.

```http
POST /tickets
Content-Type: application/json
```

**Request Body**
```json
{
  "title": "Password reset needed",
  "description": "Cannot access email account",
  "priority": "high"
}
```

**Response**
```json
{
  "ticket_id": "TICK-0001",
  "status": "open",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Priority Levels**
- `low` - Minor issues
- `medium` - Standard issues (default)
- `high` - Important issues
- `urgent` - Critical issues

**Status Codes**
- `201 Created` - Ticket created
- `400 Bad Request` - Invalid data
- `500 Internal Server Error` - Server error

---

### Get Ticket

Retrieve a specific ticket by ID.

```http
GET /tickets/{ticket_id}
```

**Parameters**
- `ticket_id` (path) - Ticket ID (e.g., "TICK-0001")

**Response**
```json
{
  "ticket_id": "TICK-0001",
  "title": "Password reset needed",
  "description": "Cannot access email account",
  "status": "open",
  "priority": "high",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "comments": []
}
```

**Status Codes**
- `200 OK` - Ticket found
- `404 Not Found` - Ticket doesn't exist
- `500 Internal Server Error` - Server error

---

### Update Ticket Status

Update the status of a ticket.

```http
PATCH /tickets/{ticket_id}/status
Content-Type: application/json
```

**Request Body**
```json
{
  "status": "resolved"
}
```

**Status Values**
- `open` - New or active ticket
- `in_progress` - Being worked on
- `resolved` - Issue fixed
- `closed` - Ticket closed

**Response**
```json
{
  "ticket_id": "TICK-0001",
  "status": "resolved",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Status Codes**
- `200 OK` - Status updated
- `400 Bad Request` - Invalid status
- `404 Not Found` - Ticket doesn't exist
- `500 Internal Server Error` - Server error

---

### Add Ticket Comment

Add a comment to a ticket.

```http
POST /tickets/{ticket_id}/comments
Content-Type: application/json
```

**Request Body**
```json
{
  "comment": "Password reset email sent to user",
  "author": "support-agent-1"
}
```

**Response**
```json
{
  "ticket_id": "TICK-0001",
  "comment_id": "c1",
  "created_at": "2024-01-15T11:05:00Z"
}
```

**Status Codes**
- `201 Created` - Comment added
- `404 Not Found` - Ticket doesn't exist
- `500 Internal Server Error` - Server error

---

### Search Tickets

Search tickets by keyword or status.

```http
GET /tickets/search?query={query}&status={status}
```

**Query Parameters**
- `query` (optional) - Search term
- `status` (optional) - Filter by status
- `priority` (optional) - Filter by priority

**Response**
```json
{
  "tickets": [
    {
      "ticket_id": "TICK-0001",
      "title": "Password reset needed",
      "status": "open",
      "priority": "high"
    }
  ],
  "total": 1
}
```

**Status Codes**
- `200 OK` - Search complete
- `400 Bad Request` - Invalid parameters
- `500 Internal Server Error` - Server error

---

## Request/Response Models

### ChatRequest

```typescript
interface ChatRequest {
  message: string;        // User's message
  session_id?: string;    // Optional session ID
}
```

### ChatResponse

```typescript
interface ChatResponse {
  response: string;       // Assistant's response
  session_id: string;     // Session ID for follow-ups
}
```

### StreamEvent

```typescript
interface StreamEvent {
  type: "token" | "chunk" | "error" | "done";
  content?: string;       // Present for token/chunk/error
  error?: string;         // Present for error type
}
```

### Ticket

```typescript
interface Ticket {
  ticket_id: string;
  title: string;
  description: string;
  status: "open" | "in_progress" | "resolved" | "closed";
  priority: "low" | "medium" | "high" | "urgent";
  created_at: string;     // ISO 8601 timestamp
  updated_at: string;     // ISO 8601 timestamp
  comments: Comment[];
}
```

### Comment

```typescript
interface Comment {
  comment_id: string;
  ticket_id: string;
  content: string;
  author: string;
  created_at: string;     // ISO 8601 timestamp
}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

## Rate Limiting

Currently no rate limiting for local development. For production:

- Implement rate limiting (e.g., 100 requests/minute)
- Return `429 Too Many Requests` when exceeded
- Include `Retry-After` header

## CORS

CORS is enabled for:
- `http://localhost:3000` (frontend)
- Credentials: Allowed
- Methods: GET, POST, PUT, PATCH, DELETE
- Headers: Content-Type, Authorization

## Streaming Details

### Server-Sent Events (SSE)

The `/chat/stream` endpoint uses SSE protocol:

**Connection**
```javascript
const eventSource = new EventSource('/chat/stream', {
  method: 'POST',
  body: JSON.stringify({ message: 'Hello' })
});

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

**Event Format**
```
data: {"type": "token", "content": "text"}\n\n
```

**Close Connection**
```javascript
eventSource.close();
```

## Examples

### Basic Chat (cURL)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need help"}'
```

### Streaming Chat (cURL)

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need help"}'
```

### Create Ticket (JavaScript)

```javascript
const response = await fetch('http://localhost:8000/tickets', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'WiFi Issue',
    description: 'Cannot connect to WiFi',
    priority: 'medium'
  })
});

const ticket = await response.json();
console.log(ticket.ticket_id);
```

### Stream Chat (JavaScript)

```javascript
const response = await fetch('http://localhost:8000/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Help with password reset',
    session_id: 'user-123'
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      console.log(data);
    }
  }
}
```

## API Documentation

Interactive API documentation available at:

**Swagger UI**: http://localhost:8000/docs

**ReDoc**: http://localhost:8000/redoc

## Webhooks (Future)

Planned webhook support for:
- Ticket status changes
- New comments
- Escalations

Stay tuned for webhook documentation.

---

**Need help?** Check the [Getting Started](GETTING_STARTED.md) guide or [Architecture](ARCHITECTURE.md) documentation.


