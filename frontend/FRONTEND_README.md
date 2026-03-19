# MediSync Frontend

Modern hospital appointment and billing management system built with Next.js, React, and Tailwind CSS.

## Features

### Patient Dashboard
- View upcoming appointments
- Book new appointments with step-by-step flow
- Cancel appointments
- View and manage invoices
- Pay invoices online

### Doctor Dashboard
- View assigned appointments
- Mark appointments as completed
- Manage availability

### Admin Dashboard
- View revenue statistics
- Track pending invoices
- Monitor completed appointments
- View top performing doctors
- System health monitoring

## Tech Stack

- **Framework**: Next.js 16
- **UI Library**: React 19
- **Styling**: Tailwind CSS 3
- **HTTP Client**: Axios
- **State Management**: React Context API

## Installation

### Prerequisites
- Node.js 18+
- npm or yarn

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/dhruv0402/medisync.git
cd medisync
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Configure environment variables**
```bash
cp .env.local.example .env.local
```

Update `.env.local` with your backend API URL:
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

4. **Run the development server**
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
app/
├── layout.tsx              # Root layout with metadata
├── page.tsx                # Root redirect page
├── globals.css             # Global styles and design tokens
├── context/
│   └── AuthContext.tsx     # Authentication context and hooks
├── login/
│   └── page.tsx            # Login page
├── dashboard/
│   └── page.tsx            # Patient/Doctor/Admin dashboard
├── appointments/
│   └── page.tsx            # Appointments listing page
├── book-appointment/
│   └── page.tsx            # Multi-step appointment booking
├── invoices/
│   └── page.tsx            # Invoices listing and payment
└── admin-dashboard/
    └── page.tsx            # Admin analytics dashboard

components/
├── Sidebar.tsx             # Navigation sidebar
├── ProtectedRoute.tsx      # Route protection wrapper
├── DashboardLayout.tsx     # Dashboard layout wrapper
└── LoadingSpinner.tsx      # Loading indicator component

lib/
└── api.ts                  # API client and endpoints

public/
└── (static assets)
```

## API Integration

All API calls are handled through `/lib/api.ts` which provides:

- **Authentication**: Login endpoint
- **Appointments**: Book, view, cancel, complete
- **Invoices**: View and pay invoices
- **Admin**: Dashboard statistics

The API client automatically:
- Adds authentication tokens to requests
- Handles 401 errors by redirecting to login
- Transforms API responses

## Authentication Flow

1. User enters email and password on login page
2. `AuthContext.login()` calls `/api/auth/login`
3. Token stored in localStorage
4. User data stored in localStorage
5. Redirected to dashboard based on role
6. Token automatically attached to all subsequent requests

## Key Components

### AuthContext
Manages global authentication state and provides:
- `user`: Current logged-in user object
- `isAuthenticated`: Boolean flag
- `login()`: Login function
- `logout()`: Logout function

### ProtectedRoute
Wrapper component that:
- Checks authentication status
- Verifies user role (optional)
- Redirects unauthorized users

### DashboardLayout
Provides sidebar navigation and layout structure for authenticated pages.

## Role-Based Access

The system supports three user roles:

### Patient
- View own appointments
- Book new appointments
- Cancel appointments
- View own invoices
- Pay invoices

### Doctor
- View assigned appointments
- Complete appointments
- Manage availability

### Admin
- View all appointments
- View revenue statistics
- Manage invoices
- System monitoring

## Design System

### Colors
- **Primary**: `#2563eb` (Blue)
- **Secondary**: `#64748b` (Slate)
- **Accent**: `#06b6d4` (Cyan)
- **Success**: `#10b981` (Green)
- **Error**: `#ef4444` (Red)
- **Warning**: `#f59e0b` (Amber)

### Component Classes
- `.btn-primary`: Primary action buttons
- `.btn-secondary`: Secondary action buttons
- `.btn-outline`: Outlined buttons
- `.input-field`: Form input styling
- `.card`: Card components
- `.table-row`: Table row styling

## Building for Production

```bash
npm run build
npm run start
```

The application will be optimized and ready for deployment on Vercel or any Node.js hosting platform.

## Deployment

### Vercel (Recommended)
1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically on push

### Docker
```bash
docker build -t medisync-frontend .
docker run -p 3000:3000 medisync-frontend
```

## Development Tips

### Adding New Pages
1. Create folder under `app/` directory
2. Add `page.tsx` file
3. Wrap with `ProtectedRoute` if needed
4. Use `DashboardLayout` for authenticated pages

### Adding New API Endpoints
1. Add function to `/lib/api.ts`
2. Use existing `apiClient` instance
3. Handle errors appropriately

### Styling Guidelines
- Use Tailwind classes for styling
- Extend theme in `tailwind.config.ts` if needed
- Define reusable component classes in `globals.css`
- Maintain responsive design with `md:` and `lg:` prefixes

## Troubleshooting

### API Connection Issues
- Ensure backend server is running on port 5000
- Check `NEXT_PUBLIC_API_URL` environment variable
- Verify CORS is enabled on backend

### Authentication Errors
- Clear localStorage and try logging in again
- Check browser console for error messages
- Verify credentials match backend database

### Styling Issues
- Run `npm install` to ensure Tailwind is installed
- Clear `.next` folder: `rm -rf .next`
- Rebuild: `npm run dev`

## License

This project is part of MediSync Hospital Management System.

## Support

For issues and questions, please open an issue on the GitHub repository.
