# 🚀 Deployment Guide - Cyber Threat Detection System

This guide explains how to deploy the application to production using **Render** (Backend) and **Vercel** (Frontend).

## 1. Prerequisites
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account (for cloud database)
- [Render](https://render.com/) account (for Flask API)
- [Vercel](https://vercel.com/) account (for React Frontend)
- Project pushed to GitHub

## 2. Database Setup (MongoDB Atlas)
1. Create a new cluster on MongoDB Atlas.
2. In **Network Access**, allow access from anywhere (`0.0.0.0/0`) or Render's IP.
3. In **Database Access**, create a user and password.
4. Copy your **Connection String** (e.g., `mongodb+srv://user:pass@cluster.mongodb.net/dbname`).

## 3. Backend Deployment (Render)
1. Log in to [Render](https://render.com/).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Configure the service:
   - **Name**: `cyber-threat-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Advanced** and add **Environment Variables**:
   - `MONGO_URI`: (Your MongoDB Atlas connection string)
   - `SECRET_KEY`: (A random secure string)
   - `JWT_SECRET_KEY`: (A random secure string)
   - `DEBUG`: `False`
   - `EMAIL_ALERTS_ENABLED`: `true` (if using email)
   - `SENDER_EMAIL`: (Your email)
   - `SENDER_PASSWORD`: (Your app password)
6. Click **Create Web Service**.

## 4. Frontend Deployment (Vercel)
1. Log in to [Vercel](https://vercel.com/).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. Configure the project:
   - **Project Name**: `cyber-threat-dashboard`
   - **Framework Preset**: `Create React App`
   - **Root Directory**: `frontend`
5. Add **Environment Variables**:
   - `REACT_APP_API_URL`: `https://your-api-url.onrender.com/api` (Copy this from Render after it deploys)
6. Click **Deploy**.

## 5. Final Connection
- Once the backend is deployed, copy its URL from Render.
- Go back to Vercel project settings > **Environment Variables**.
- Update `REACT_APP_API_URL` with your Render URL + `/api`.
- Redeploy the frontend.

---
**Note on AI Model**: The backend uses `torch` and `transformers`. If Render's free tier (512MB RAM) fails, you may need to upgrade to a "Starter" plan or use a specialized AI provider like Hugging Face Spaces for the model inference.
