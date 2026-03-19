# MediSync Frontend - Quick Start Guide

## 🚀 Start Here

This guide will get you up and running in 5 minutes.

## System Requirements

- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher
- **Operating System**: macOS, Windows, or Linux

## Installation

### Step 1: Install Dependencies

```bash
npm install
```

This installs all required packages:
- next@16.0.0
- react@19.0.0
- react-dom@19.0.0
- tailwindcss@3.4.0
- axios@1.7.4
- typescript@5.0.0

### Step 2: Configure Environment

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and set your backend API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

Replace `http://localhost:5000` with your actual backend URL.

### Step 3: Start Development Server

```bash
npm run dev
```

The app will start on **http://localhost:3000**

## 📖 Understanding the Code Structure

All code is organized in the `/app` and `/components` directories:

### Pages (Actual Application Pages)

```
app/
├── page.tsx                  # Root page - redirects based on login status
├── login/page.tsx            # Login form
├── dashboard/page.tsx        # Patient dashboard overview
├── book-appointment/page.tsx # 4-step appointment booking
├── appointments/page.tsx     # View and manage appointments
├── invoices/page.tsx         # View and pay invoices
└── admin-dashboard/page.tsx  # Admin statistics and analytics
```

### Components (Reusable UI Elements)

```
components/
├── Sidebar.tsx               # Navigation menu
├── DashboardLayout.tsx       # Dashboard layout wrapper
├── ProtectedRoute.tsx        # Secure route protection
└── LoadingSpinner.tsx        # Loading indicator
```

### Utilities (Backend Integration)

```
lib/
├── api.ts                    # API client and all endpoints
└── types.ts                  # TypeScript type definitions
```

### Styling

```
app/
├── globals.css               # Global styles and design tokens
└── layout.tsx                # Root HTML layout
```

## 🔐 Test the Application

### Demo Credentials

Use these to test different user roles:

| Role | Email | Password |
|------|-------|----------|
| Patient | `patient@example.com` | `password123` |
| Doctor | `doctor@example.com` | `password123` |
| Admin | `admin@example.com` | `password123` |

### User Journey

**As a Patient:**
1. Login with `patient@example.com`
2. Click "Book New Appointment"
3. Follow the 4-step wizard
4. View your appointments
5. Go to Invoices and pay a bill

**As a Doctor:**
1. Login with `doctor@example.com`
2. View assigned appointments
3. Mark appointments as complete

**As an Admin:**
1. Login with `admin@example.com`
2. View dashboard with statistics
3. Monitor revenue and appointments

## 📂 Viewing Source Code

### In Your Editor

Open any file and start exploring:

```bash
# Open in VS Code
code .

# Or just open the folder in any editor
```

### Key Files to Review

**Authentication** (start here):
- `app/context/AuthContext.tsx` - How login/logout works

**Pages** (see full app features):
- `app/login/page.tsx` - Login form
- `app/dashboard/page.tsx` - Main dashboard
- `app/book-appointment/page.tsx` - Booking wizard
- `app/appointments/page.tsx` - Appointments list
- `app/invoices/page.tsx` - Invoice management
- `app/admin-dashboard/page.tsx` - Admin analytics

**API Integration** (backend communication):
- `lib/api.ts` - All API endpoints and calls

**Styling** (design system):
- `app/globals.css` - Colors and component styles
- `tailwind.config.ts` - Tailwind configuration

## 🎨 Customizing the App

### Change Colors

Edit `app/globals.css`:

```css
:root {
  --primary: #2563eb;        /* Change this to your brand color */
  --secondary: #64748b;
  --accent: #06b6d4;
  /* ... more colors ... */
}
```

### Add a New Page

1. Create folder: `app/my-page/`
2. Create file: `app/my-page/page.tsx`
3. Copy this template:

```typescript
"use client";

import DashboardLayout from "@/components/DashboardLayout";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function MyPage() {
  return (
    <ProtectedRoute>
      <DashboardLayout>
        <h1>My New Page</h1>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
```

4. Add link in `components/Sidebar.tsx`

### Add a New API Endpoint

Edit `lib/api.ts`:

```typescript
export const myAPI = {
  getData: () =>
    apiClient.get("/my-endpoint"),
  createData: (data: any) =>
    apiClient.post("/my-endpoint", data),
};
```

Then use it in your component:

```typescript
import { myAPI } from '@/lib/api';

const result = await myAPI.getData();
```

## 🚢 Building for Production

### Build Command

```bash
npm run build
```

This creates an optimized production build in the `.next` folder.

### Start Production Server

```bash
npm run start
```

The app will run on http://localhost:3000 (production optimized).

### Check Build Size

```bash
npm run build

# Output will show:
# ✓ Compiled client and server successfully
# ┌ Route (app)                    Size
# ├ ○ /                           125 B
# ├ ○ /login                      2.3 kB
# ├ ○ /dashboard                  3.5 kB
# └ ○ /appointments               2.8 kB
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t medisync-frontend .
```

### Run Container

```bash
docker run -p 3000:3000 medisync-frontend
```

### Docker Compose (Frontend + Backend)

```bash
docker-compose up
```

This starts both frontend and backend servers.

## 🔧 Troubleshooting

### Problem: "Cannot find module"

**Solution**: Run `npm install` again

```bash
npm install
rm -rf node_modules
npm install
```

### Problem: "Port 3000 already in use"

**Solution**: Kill the process using port 3000

```bash
# macOS/Linux
lsof -i :3000
kill -9 <PID>

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Problem: "API connection failed"

**Solution**: Check `.env.local`

```bash
# Make sure this is set correctly:
NEXT_PUBLIC_API_URL=http://localhost:5000/api

# And your backend is running on:
http://localhost:5000
```

### Problem: "Styles not loading"

**Solution**: Clear cache and rebuild

```bash
rm -rf .next
npm run dev
```

### Problem: "Login not working"

**Solution**: Check browser console

```javascript
// Open DevTools (F12) → Console
// Look for error messages
// Check if NEXT_PUBLIC_API_URL is correct
```

## 📚 Learn More

### Documentation Files

- **FRONTEND_README.md** - Complete documentation with all details
- **PROJECT_STRUCTURE.md** - Detailed file structure explanation
- **CODE_REFERENCE.md** - Code patterns and conventions
- **QUICK_START.md** - This file

### Official Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Axios Docs](https://axios-http.com)

## 🎯 Common Tasks

### Add Authentication to a New Page

```typescript
import ProtectedRoute from "@/components/ProtectedRoute";

export default function MyPage() {
  return (
    <ProtectedRoute requiredRole="patient">
      {/* Page content only visible to patients */}
    </ProtectedRoute>
  );
}
```

### Fetch Data from API

```typescript
import { appointmentAPI } from '@/lib/api';
import { useEffect, useState } from 'react';

export default function MyComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const result = await appointmentAPI.getMyAppointments();
        setData(result);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{/* Render data */}</div>;
}
```

### Handle Form Submission

```typescript
const [email, setEmail] = useState('');
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');

  try {
    await someAPI.submit({ email });
    // Success!
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};
```

### Add a Button with Loading State

```typescript
<button
  onClick={handleClick}
  disabled={loading}
  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
>
  {loading ? "Loading..." : "Click Me"}
</button>
```

## 🤝 Contributing

To add features:

1. Create a new branch: `git checkout -b feature/my-feature`
2. Make changes following existing patterns
3. Test thoroughly
4. Commit: `git commit -m "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Create Pull Request

## 📝 Project Checklist

- [ ] Install dependencies (`npm install`)
- [ ] Configure `.env.local`
- [ ] Start dev server (`npm run dev`)
- [ ] Test login with demo credentials
- [ ] Explore all pages
- [ ] Review source code structure
- [ ] Read FRONTEND_README.md for details
- [ ] Make first code change
- [ ] Test your changes
- [ ] Build for production (`npm run build`)

## ✅ You're Ready!

Your MediSync frontend is ready to use. Here's what you have:

✅ **7 Complete Pages**
- Login, Dashboard, Appointments, Book Appointment, Invoices, Admin Dashboard

✅ **4 Reusable Components**
- Sidebar, DashboardLayout, ProtectedRoute, LoadingSpinner

✅ **Full API Integration**
- All endpoints configured with authentication

✅ **Responsive Design**
- Works on desktop, tablet, and mobile

✅ **TypeScript**
- Type-safe code throughout

✅ **Production Ready**
- Optimized builds, Docker support, Vercel deployment

## 🚀 Next Steps

1. **Understand the Code**: Open files and read comments
2. **Make Changes**: Try adding a new feature
3. **Connect Backend**: Update API URLs
4. **Deploy**: Use Docker or Vercel
5. **Customize**: Change colors, add your branding

## 💬 Need Help?

- Check the **Troubleshooting** section above
- Read **FRONTEND_README.md** for detailed docs
- Review **PROJECT_STRUCTURE.md** for file explanations
- Check **CODE_REFERENCE.md** for patterns and examples
- Open DevTools (F12) to debug issues

## 📞 Support

For issues or questions about the code:

1. Check browser console for errors (F12)
2. Check npm output for build warnings
3. Review error messages carefully
4. Consult the documentation files
5. Ask for help from the team

Happy coding! 🎉
