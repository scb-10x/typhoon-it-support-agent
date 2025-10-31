# IT Support Frontend

Modern chat interface for the Typhoon IT Support system built with Next.js 16, React 19, and Tailwind CSS 4.

## Features

- 🎨 Modern, beautiful chat UI with gradients and smooth animations
- 💬 Real-time chat with IT support agent
- 🌓 Dark mode support
- 📱 Fully responsive design
- ⚡ Fast and optimized with Next.js 16
- 🎯 Type-safe with TypeScript

## Getting Started

### Prerequisites

- Node.js 18+
- pnpm (or npm/yarn)

### Installation

1. Install dependencies:
```bash
pnpm install
```

2. Create environment file:
```bash
cp .env.local.example .env.local
```

3. Update `.env.local` with your backend URL (default is `http://localhost:8000`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Run the development server:

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production

Build for production:

```bash
pnpm build
pnpm start
```

## Project Structure

```
frontend/
├── app/
│   ├── components/
│   │   └── Chat.tsx          # Main chat component
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout
│   └── page.tsx               # Home page
├── public/                    # Static assets
└── package.json
```

## Chat Component

The main chat component (`app/components/Chat.tsx`) includes:

- Message display with role-based styling
- User and assistant avatars
- Typing indicator animation
- Session management
- Clear chat functionality
- Quick suggestion buttons
- Auto-scroll to latest message
- Error handling

## API Integration

The frontend connects to the FastAPI backend at `/chat` endpoint:

```typescript
POST /chat
{
  "message": "User's question",
  "session_id": "optional-session-id"
}

Response:
{
  "message": "Assistant's response",
  "session_id": "session-id",
  "iteration": 1,
  "next_action": "continue"
}
```

## Styling

- **Tailwind CSS 4** for utility-first styling
- Custom gradient backgrounds
- Smooth animations and transitions
- Dark mode with automatic color scheme detection
- Responsive design for mobile, tablet, and desktop

## Technologies

- **Next.js 16** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **PostCSS** - CSS processing

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Development Tips

1. **Hot Reload**: Changes to components will automatically reload
2. **Type Checking**: TypeScript provides excellent IDE support
3. **Styling**: Use Tailwind classes for consistent styling
4. **Dark Mode**: Automatically follows system preferences

## Troubleshooting

### Backend Connection Issues

If you see "backend server is running" errors:

1. Make sure the FastAPI backend is running:
   ```bash
   cd ../agentic-workflow
   uv run python -m src.typhoon_it_support.api.run
   ```

2. Verify the API URL in `.env.local` matches your backend

3. Check CORS settings in the backend allow your frontend origin

### Build Errors

If you encounter build errors:

1. Clear Next.js cache:
   ```bash
   rm -rf .next
   ```

2. Reinstall dependencies:
   ```bash
   rm -rf node_modules pnpm-lock.yaml
   pnpm install
   ```

## License

MIT
