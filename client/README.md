# client (MoleMonitor frontend)

React + TypeScript frontend for MoleMonitor. Talks to the **api** Flask backend.

## Setup

```bash
cd client
npm install
```

## Run

**Run client and API together (recommended):**

```bash
npm start
```

Starts the Vite dev server and the Flask API in one go. Client at `http://localhost:5173`, API at `http://localhost:5000`; requests to `/api` and `/uploads` are proxied to the API.

**Run client only:**

```bash
npm run dev
```

Runs at `http://localhost:5173`. Start the API separately from the repo root with `cd api && python app.py` if you need backend features.

## Build

```bash
npm run build
npm run preview
```

## Routes

- `/` — Home (upload & compare)
- `/history` — Image History
- `/instructions` — Instructions
- `/about` — About
- `/login`, `/register` — Auth (placeholders)
