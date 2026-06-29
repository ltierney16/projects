# Calculator

A full-stack calculator app with persistent calculation history. The frontend is a React (Vite) single-page app; the backend is a Spring Boot REST API backed by MySQL.

## Project structure
The frontend and backend are independent projects that communicate over HTTP — the frontend calls the backend's REST API at `http://localhost:8080`.

## Prerequisites

- Java 17+
- Node.js (with npm)
- MySQL Server + MySQL Workbench (or another MySQL client)

## Setup

### 1. Database

1. Install MySQL Server and MySQL Workbench.
2. Connect to your local MySQL instance and create the database:
```sql
   CREATE DATABASE calculatordb;
```

### 2. Backend

```bash
cd backend
cp src/main/resources/application.properties.example src/main/resources/application.properties
```

Edit `src/main/resources/application.properties` and set `spring.datasource.password` to your local MySQL password.

Then run:

```bash
./mvnw spring-boot:run
```

The backend starts on `http://localhost:8080`. Maven will pull down all dependencies automatically on first run.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server starts on `http://localhost:5173`.

## How it works

- The calculator UI runs entirely in the browser.
- Each time you press `=`, the result is saved to the backend via `POST /api/history` and stored in MySQL.
- Calculation history can be browsed using the up/down arrows next to the display, which step through past entries fetched via `GET /api/history`.