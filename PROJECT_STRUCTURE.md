# MediSync Frontend - Complete Project Structure

This document provides a complete overview of all files and their purposes in the MediSync frontend application.

## Directory Structure

```
medisync-frontend/
├── app/                          # Next.js App Router directory
│   ├── layout.tsx                # Root layout with global metadata
│   ├── page.tsx                  # Root page (redirects based on auth)
│   ├── globals.css               # Global styles and CSS variables
│   ├── providers.tsx             # App providers wrapper (AuthProvider)
│   ├── context/
│   │   └── AuthContext.tsx       # Authentication context, hooks, state management
│   ├── login/
│   │   └── page.tsx              # Login page with email/password form
│   ├── dashboard/
│   │   └── page.tsx              # Patient/Doctor dashboard with summary
│   ├── appointments/
│   │   └── page.tsx              # Appointments list with filters and actions
│   ├── book-appointment/
│   │   └── page.tsx              # Multi-step appointment booking wizard
│   ├── invoices/
│   │   └── page.tsx              # Invoices list with payment modal
│   └── admin-dashboard/
│       └── page.tsx              # Admin dashboard with statistics
├── components/                   # Reusable React components
│   ├── Sidebar.tsx               # Navigation sidebar with role-based menus
│   ├── DashboardLayout.tsx       # Layout wrapper for dashboard pages
│   ├── ProtectedRoute.tsx        # Route protection with auth and role checks
│   └── LoadingSpinner.tsx        # Loading indicator component
├── lib/                          # Utility functions and API client
│   ├── api.ts                    # Axios API client with interceptors
│   └── types.ts                  # TypeScript type definitions
├── public/                       # Static assets (images, fonts, etc.)
│   └── (static files)
├── package.json                  # Project dependencies and scripts
├── tailwind.config.ts            # Tailwind CSS configuration
├── next.config.ts                # Next.js configuration
├── tsconfig.json                 # TypeScript configuration
├── postcss.config.js             # PostCSS configuration
├── .env.local.example            # Environment variables template
├── vercel.json                   # Vercel deployment configuration
├── Dockerfile                    # Docker image configuration
├── docker-compose.yml            # Docker Compose setup
├── FRONTEND_README.md            # Frontend documentation
├── PROJECT_STRUCTURE.md          # This file
├── .gitignore                    # Git ignore patterns
└── README.md                     # Main project README

```

## File Descriptions

### Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | NPM dependencies, scripts, and project metadata |
| `tailwind.config.ts` | Tailwind CSS theme configuration and content paths |
| `next.config.ts` | Next.js runtime configuration |
| `tsconfig.json` | TypeScript compiler options and path aliases |
| `postcss.config.js` | PostCSS plugin configuration |
| `vercel.json` | Vercel deployment configuration |
| `.env.local.example` | Environment variables template |
| `.gitignore` | Git ignore patterns |

### App Files

#### Authentication
- **`app/context/AuthContext.tsx`** (94 lines)
  - Provides global auth state via React Context
  - Methods: `login()`, `logout()`
  - Persists token and user data to localStorage
  - Handles auto-logout on 401 errors

- **`app/login/page.tsx`** (104 lines)
  - Email and password login form
  - Shows demo credentials
  - Redirects to dashboard on successful login
  - Error handling and loading states

#### Pages (Dashboard)
- **`app/page.tsx`** (30 lines)
  - Root redirect page
  - Redirects authenticated users to dashboard
  - Redirects unauthenticated users to login

- **`app/dashboard/page.tsx`** (161 lines)
  - Patient/Doctor/Admin dashboard overview
  - Shows upcoming appointments and recent invoices
  - Quick action buttons
  - Fetches real-time data from API

#### Pages (Patient Features)
- **`app/book-appointment/page.tsx`** (291 lines)
  - Multi-step appointment booking (4 steps)
  - Step 1: Select department
  - Step 2: Select doctor
  - Step 3: Select date
  - Step 4: Select time slot
  - Dynamic doctor and slot loading from API

- **`app/appointments/page.tsx`** (199 lines)
  - List all appointments with filtering
  - Status filters: all, confirmed, completed, cancelled
  - Role-based actions (cancel for patients, complete for doctors)
  - Responsive table with mobile support

- **`app/invoices/page.tsx`** (217 lines)
  - List invoices with summary cards
  - Shows total, pending, and paid amounts
  - Payment modal with confirmation
  - Status-based filtering

#### Pages (Admin)
- **`app/admin-dashboard/page.tsx`** (164 lines)
  - Revenue statistics and KPIs
  - Displays total revenue, daily revenue, pending invoices
  - Top performing doctor
  - System status indicators

#### Layout & Styles
- **`app/layout.tsx`** (25 lines)
  - Root layout wrapper
  - Metadata configuration
  - Providers setup

- **`app/globals.css`** (190 lines)
  - Global Tailwind directives
  - CSS custom properties (design tokens)
  - Utility classes
  - Animations and transitions
  - Form and button styles

### Components

- **`components/Sidebar.tsx`** (125 lines)
  - Navigation sidebar with role-based menus
  - Mobile responsive with toggle
  - User info display
  - Logout button

- **`components/DashboardLayout.tsx`** (19 lines)
  - Layout wrapper for dashboard pages
  - Integrates sidebar and main content area
  - Mobile hamburger menu toggle

- **`components/ProtectedRoute.tsx`** (47 lines)
  - Route protection wrapper
  - Checks authentication and user role
  - Shows loading spinner during auth check
  - Redirects unauthorized users

- **`components/LoadingSpinner.tsx`** (8 lines)
  - Animated loading indicator
  - Full-height centered spinner with text

### Utilities

- **`lib/api.ts`** (82 lines)
  - Axios HTTP client with base URL
  - Request interceptor: adds auth tokens
  - Response interceptor: handles 401 errors
  - API endpoint methods organized by resource:
    - `authAPI`: Login
    - `appointmentAPI`: Book, view, cancel, complete appointments
    - `invoiceAPI`: View and pay invoices
    - `adminAPI`: Dashboard data

- **`lib/types.ts`** (88 lines)
  - User interface with role enum
  - Department, Doctor, TimeSlot types
  - Appointment and Invoice types
  - Invoice status: pending, paid, overdue
  - AdminDashboard interface
  - API response and error types

### Deployment & Containerization

- **`Dockerfile`** (46 lines)
  - Multi-stage build for optimization
  - Node.js base image
  - Development and production stages
  - Environment variables setup

- **`docker-compose.yml`** (41 lines)
  - Frontend service on port 3000
  - Backend service on port 5000
  - Environment configuration
  - Full stack setup

### Documentation

- **`FRONTEND_README.md`** (256 lines)
  - Feature overview
  - Tech stack description
  - Installation instructions
  - Project structure explanation
  - API integration guide
  - Authentication flow
  - Role-based access control
  - Design system documentation
  - Deployment guides
  - Troubleshooting section

## Key Features

### Authentication
- Email/password login
- JWT token-based sessions
- localStorage persistence
- Automatic token injection in requests
- Auto-logout on unauthorized (401)

### Role-Based Access Control
- **Patient**: Can book, view, and cancel appointments; manage invoices
- **Doctor**: Can view assigned appointments and mark as complete
- **Admin**: Full access to all features including analytics and reports

### Appointment System
- Browse doctors by department
- View available time slots
- Multi-step booking wizard
- Cancel and complete appointment actions
- Status tracking (confirmed, completed, cancelled, pending)

### Invoice Management
- View all invoices with summary
- Filter by status (pending, paid)
- Payment modal with confirmation
- Status badges and formatting

### Admin Dashboard
- Revenue statistics and KPIs
- Daily and total revenue tracking
- Pending invoices count
- Completed appointments count
- Top performing doctor metrics
- System health monitoring

## Design System

### Color Variables (CSS Custom Properties)
```css
--background: #ffffff
--foreground: #0f172a
--primary: #2563eb (Blue)
--secondary: #64748b (Slate)
--accent: #06b6d4 (Cyan)
--success: #10b981 (Green)
--error: #ef4444 (Red)
--warning: #f59e0b (Amber)
--border: #e2e8f0
```

### Typography
- Font Family: System fonts (San Francisco, Segoe UI, Roboto)
- Tailwind CSS for responsive text sizes

### Component Classes
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button
- `.btn-outline` - Outlined button
- `.input-field` - Form input with focus styles
- `.card` - Card container with shadow
- `.table-row` - Table row with hover effect

## API Endpoints

### Authentication
- `POST /auth/login` - User login

### Appointments
- `GET /appointments/doctors?department_id={id}` - Get doctors by department
- `GET /appointments/slots?doctor_id={id}&date={date}` - Get available slots
- `POST /appointments/book` - Book appointment
- `GET /appointments/my` - Get user's appointments
- `DELETE /appointments/{id}` - Cancel appointment
- `PUT /appointments/complete/{id}` - Complete appointment

### Invoices
- `GET /invoices` - Get all invoices
- `POST /invoices/pay/{id}` - Pay invoice

### Admin
- `GET /admin/dashboard` - Get dashboard statistics

## Development Workflow

### 1. Setup
```bash
npm install
cp .env.local.example .env.local
```

### 2. Configure
Update `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

### 3. Run
```bash
npm run dev
```

### 4. Build
```bash
npm run build
npm run start
```

## Technologies Used

- **Framework**: Next.js 16
- **Runtime**: React 19
- **Styling**: Tailwind CSS 3.4
- **HTTP Client**: Axios 1.6
- **Language**: TypeScript 5
- **CSS**: PostCSS with Autoprefixer

## Scripts

| Script | Purpose |
|--------|---------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance Considerations

- Image optimization via Next.js
- Automatic code splitting by route
- Server-side rendering for pages
- Client-side hydration
- Optimized CSS with Tailwind
- Tree-shaking for unused styles

## Security Features

- JWT token-based authentication
- HTTP-only localStorage storage
- CSRF protection via token
- SQL injection prevention (parameterized queries on backend)
- XSS protection via React's built-in escaping

## Responsive Design

- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Flexible layouts using Flexbox and Grid
- Touch-friendly interactive elements
- Responsive navigation with mobile menu

## Testing

To add tests (not included in current setup):
1. Install Jest and React Testing Library
2. Create `__tests__` folders parallel to components
3. Follow existing component patterns

## Future Enhancements

- Dark mode support
- Real-time notifications
- Appointment reminders
- Patient medical history
- Doctor availability calendar
- Advanced payment options
- Analytics and reporting
- Multi-language support (i18n)
- PWA features
- Offline support

## Troubleshooting

### Port 3000 already in use
```bash
lsof -i :3000
kill -9 <PID>
```

### Clear Next.js cache
```bash
rm -rf .next
npm run dev
```

### Update dependencies
```bash
npm update
npm install
```

## Contributing

1. Create a feature branch
2. Make changes following existing patterns
3. Test thoroughly
4. Create pull request

## License

Part of MediSync Hospital Management System

## Support

For issues and questions, please refer to FRONTEND_README.md or contact the development team.
