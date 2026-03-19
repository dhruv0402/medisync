# MediSync Frontend - Code Reference

Quick reference to all source code files with line counts and purposes.

## Summary Statistics

- **Total Source Files**: 22
- **Total Lines of Code**: ~2,100
- **Configuration Files**: 8
- **React Components**: 4
- **App Pages**: 8
- **Utility Files**: 2
- **Documentation**: 3

## Files at a Glance

### Configuration & Setup

```
package.json                 28 lines   - Dependencies and npm scripts
tsconfig.json               28 lines   - TypeScript configuration
tailwind.config.ts          25 lines   - Tailwind theme config
next.config.ts               9 lines   - Next.js runtime config
postcss.config.js            7 lines   - PostCSS plugin setup
.env.local.example           2 lines   - Environment template
vercel.json                 16 lines   - Vercel deployment config
.gitignore                  45 lines   - Git ignore patterns
```

### Authentication & Context

```
app/context/AuthContext.tsx  94 lines   - Global auth state management
  • useAuth() hook
  • login(email, password) function
  • logout() function
  • User and loading state
  • localStorage persistence
```

### Layout & Styling

```
app/layout.tsx              25 lines   - Root layout with metadata
app/globals.css            190 lines   - CSS variables, Tailwind directives
app/providers.tsx            8 lines   - App provider wrapper
```

### Pages

```
app/page.tsx                30 lines   - Root redirect page
app/login/page.tsx         104 lines   - Login form with demo credentials
app/dashboard/page.tsx     161 lines   - Dashboard overview
app/appointments/page.tsx  199 lines   - Appointments list with filters
app/book-appointment/page.tsx 291 lines - Multi-step booking wizard
app/invoices/page.tsx      217 lines   - Invoices with payment modal
app/admin-dashboard/page.tsx 164 lines - Admin analytics dashboard
```

### Components

```
components/Sidebar.tsx              125 lines - Navigation sidebar
components/DashboardLayout.tsx       19 lines - Layout wrapper
components/ProtectedRoute.tsx        47 lines - Route protection
components/LoadingSpinner.tsx         8 lines - Loading indicator
```

### Utilities

```
lib/api.ts                   82 lines   - Axios client and endpoints
lib/types.ts                 88 lines   - TypeScript definitions
```

### Documentation

```
FRONTEND_README.md          256 lines   - Complete frontend docs
PROJECT_STRUCTURE.md        419 lines   - Detailed project guide
CODE_REFERENCE.md           (this file)
```

### Deployment

```
Dockerfile                   46 lines   - Docker image config
docker-compose.yml          41 lines   - Docker Compose setup
```

## Core Components Deep Dive

### 1. AuthContext (app/context/AuthContext.tsx)

**Purpose**: Global authentication state management

**Key Features**:
- Context provider for entire app
- Automatic localStorage persistence
- Login with email/password
- Role-based redirects
- Automatic logout on 401

**Exports**:
```typescript
AuthProvider           // Component wrapper
useAuth()             // Hook for using auth
User                  // Type definition
AuthContextType       // Type definition
```

### 2. Login Page (app/login/page.tsx)

**Purpose**: User authentication entry point

**Features**:
- Email and password inputs
- Form validation
- Error messages
- Loading state
- Demo credentials display
- Auto-redirect if already authenticated

**Includes**:
- React hook form handling
- API error management
- Navigate after successful login

### 3. Dashboard Pages

#### Patient Dashboard (app/dashboard/page.tsx)
- Shows upcoming appointments (up to 3)
- Shows recent invoices (up to 3)
- Quick action buttons
- Fetches data from API

#### Admin Dashboard (app/admin-dashboard/page.tsx)
- Revenue statistics
- Daily revenue tracking
- Pending invoices count
- Completed appointments count
- Top performing doctor
- System health indicators

### 4. Booking Wizard (app/book-appointment/page.tsx)

**4-Step Process**:
1. **Select Department** - Choose from Cardiology, Orthopedics, Pediatrics, Neurology
2. **Select Doctor** - Dynamically loaded from API based on department
3. **Select Date** - Date picker with min/max constraints
4. **Select Time Slot** - Dynamically loaded from API

**Features**:
- Progress bar showing current step
- Back navigation between steps
- Form validation
- Loading states
- Error handling
- Success confirmation

### 5. Appointments Page (app/appointments/page.tsx)

**Features**:
- Tabular display of appointments
- Filter buttons: All, Confirmed, Completed, Cancelled
- Status color-coded badges
- Role-based actions:
  - Patient: Cancel appointment
  - Doctor/Admin: Complete appointment
- Responsive table with mobile support
- Confirmation dialogs

### 6. Invoices Page (app/invoices/page.tsx)

**Features**:
- Summary cards: Total, Pending, Paid amounts
- Invoice listing with details
- Filter buttons: All, Pending, Paid
- Payment modal with confirmation
- Status indicators
- Amount formatting (₹ symbol)

### 7. Sidebar Navigation (components/Sidebar.tsx)

**Features**:
- Role-based menu items
- Mobile toggle with overlay
- Active page highlighting
- User info display
- Logout button

**Menu Items**:
- **Patient**: Dashboard, Book Appointment, My Appointments, Invoices
- **Doctor**: Dashboard, Appointments
- **Admin**: Dashboard, Appointments, Invoices

### 8. Protected Routes (components/ProtectedRoute.tsx)

**Features**:
- Checks authentication status
- Optional role validation
- Loading spinner during check
- Redirects unauthorized users
- Prevents unauthorized component rendering

## API Integration Pattern

All API calls use the centralized `lib/api.ts`:

```typescript
// Example usage
import { appointmentAPI } from '@/lib/api';

const doctors = await appointmentAPI.getDoctors(departmentId);
const slots = await appointmentAPI.getSlots(doctorId, date);
await appointmentAPI.bookAppointment(data);
```

### API Interceptors

**Request Interceptor**:
- Adds `Authorization: Bearer {token}` header
- Uses token from localStorage

**Response Interceptor**:
- Automatically logs out on 401
- Clears token and user data
- Redirects to login page
- Returns API response data directly

## State Management Pattern

### Global State (AuthContext)
```typescript
const { user, loading, isAuthenticated, login, logout } = useAuth();
```

### Local State (useState)
- Form inputs (email, password)
- Filtered data (appointments, invoices)
- UI states (modal open, loading)
- Error messages

### No Redux or Zustand
- Context API is sufficient for this app
- Simple authentication flows
- Localized component state

## Styling Architecture

### CSS Variables (Design Tokens)
```css
--primary: #2563eb       (Blue)
--secondary: #64748b     (Slate)
--accent: #06b6d4        (Cyan)
--success: #10b981       (Green)
--error: #ef4444         (Red)
--warning: #f59e0b       (Amber)
```

### Tailwind CSS Approach
- Utility-first CSS
- Responsive prefixes: `md:`, `lg:`
- Custom component classes in globals.css
- No CSS-in-JS library needed

### Component Styling Examples
```tsx
// Button styling
className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark"

// Responsive grid
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"

// Status badge
className="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-success"
```

## Form Handling Pattern

All forms follow this pattern:

```typescript
const [formData, setFormData] = useState('');
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');
  
  try {
    await apiCall(formData);
    // Success handling
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};
```

## Error Handling Pattern

```typescript
// API errors
try {
  await appointmentAPI.bookAppointment(data);
} catch (err) {
  setError("Failed to book appointment");
  console.error(err);
}

// Form validation
if (!selectedSlot) {
  setError("Please select a time slot");
  return;
}

// Display to user
{error && (
  <div className="mb-4 p-4 bg-red-50 border border-error text-error rounded-lg">
    {error}
  </div>
)}
```

## Responsive Design Pattern

```typescript
// Mobile-first approach
className="
  // Mobile (default)
  grid-cols-1 gap-4
  
  // Tablet and up
  md:grid-cols-2 md:gap-6
  
  // Desktop and up
  lg:grid-cols-4 lg:gap-8
"
```

## Type Safety

All components use TypeScript with proper typing:

```typescript
interface Appointment {
  id: string;
  doctor_name: string;
  date: string;
  time: string;
  status: 'confirmed' | 'completed' | 'cancelled' | 'pending';
  reason?: string;
}

interface User {
  id: string;
  email: string;
  name: string;
  role: 'patient' | 'doctor' | 'admin';
}
```

## Performance Features

- Code splitting by route (Next.js automatic)
- Image optimization (next/image)
- CSS minification (Tailwind)
- Tree-shaking unused styles
- Lazy component loading (React.lazy)

## Browser Compatibility

- Modern browsers (2022+)
- Chrome, Firefox, Safari, Edge
- Mobile browsers (iOS Safari, Chrome Mobile)
- ES2020 JavaScript target

## File Size Breakdown

```
Estimated Production Bundle:
- React + React-DOM:     ~40 KB (gzipped)
- Next.js Framework:     ~50 KB (gzipped)
- Tailwind CSS:          ~20 KB (gzipped)
- Application Code:      ~30 KB (gzipped)
- Axios:                 ~10 KB (gzipped)
─────────────────────────────────
Total (optimized):      ~150 KB (gzipped)
```

## Development Tools Used

- **Next.js 16**: React framework with SSR
- **React 19**: UI library
- **TypeScript 5**: Type safety
- **Tailwind CSS 3.4**: Utility-first CSS
- **Axios 1.6**: HTTP client
- **ESLint**: Code linting

## Getting Started Quick

1. **Install**: `npm install`
2. **Configure**: `cp .env.local.example .env.local` + update API URL
3. **Run**: `npm run dev`
4. **Build**: `npm run build`
5. **Deploy**: `npm run start` or Docker

## Key Decision Patterns

| Aspect | Choice | Reason |
|--------|--------|--------|
| State Mgmt | Context API | Sufficient for auth, avoids bloat |
| Styling | Tailwind CSS | Fast development, small bundle |
| HTTP Client | Axios | Interceptors for auth automation |
| Routing | Next.js App Router | Modern, better performance |
| Type Safety | TypeScript | Catch errors early, better DX |
| Form Handling | React useState | Simple, no external lib needed |

## Common Code Patterns

### Fetching with Error Handling
```typescript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState('');

useEffect(() => {
  const fetch = async () => {
    try {
      const result = await api.getData();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  fetch();
}, []);
```

### Protected Page Wrapper
```typescript
<ProtectedRoute requiredRole="patient">
  <DashboardLayout>
    {/* Page content */}
  </DashboardLayout>
</ProtectedRoute>
```

## Next Steps for Customization

1. Update colors in globals.css for branding
2. Add your logo to components/Sidebar.tsx
3. Extend tailwind.config.ts for custom fonts
4. Add more pages in app/ directory
5. Extend API endpoints in lib/api.ts
6. Add more components in components/ directory

## Checklist Before Deployment

- [ ] Update NEXT_PUBLIC_API_URL for production
- [ ] Test all authentication flows
- [ ] Verify API endpoints work
- [ ] Test on mobile devices
- [ ] Check build completes: `npm run build`
- [ ] Test production build: `npm run start`
- [ ] Review environment variables
- [ ] Test all user roles
- [ ] Verify error handling
- [ ] Check loading states
- [ ] Test with slow network
