# UI/UX Design

## Design Language

- Clean, modern SaaS aesthetic
- Color-coded score visualization (red/yellow/green)
- Circular score gauges for instant readability
- Responsive layout (sidebar collapses on mobile)

## Pages

### Login / Register
- Centered card layout with email/password form
- Links between login and register
- Error states for invalid credentials
- Loading states on form submission

### Dashboard
- "My Resumes" heading with upload CTA button
- Resume list with filename, date, size, status badge
- Actions: Analyze (triggers AI) / Delete (confirmation modal)
- Empty state when no resumes exist
- Skeleton loading placeholders

### Upload
- Drag-and-drop zone with click-to-browse fallback
- File type and size validation with inline errors
- Upload progress indicator
- Auto-navigates to analysis results on success

### Analysis Results
- Animated circular score gauges (2x2 grid)
- Color-coded by score range
- Summary text below gauges
- Pulsing "processing" indicator during analysis
- Auto-polls every 3 seconds, stops on completion
- Error state with retry on failure

### Profile
- Read-only email and role display
- Editable full name field
- Save with success/error feedback

### DBN Standards (Recruiter)
- Active standard display with criteria list
- Create new standard form (name, version)
- Criteria cards showing weight and max score

## States Coverage

Every page handles:
- **Loading**: Skeleton placeholders or spinners
- **Empty**: Illustration + message + CTA
- **Error**: Error message + retry button
- **Data**: Full content display