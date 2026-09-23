# Frontend UI/UX Improvement Plan

## Goal
Polish the SignLearn frontend to look like a modern AI-powered learning platform inspired by the reference dashboard, while preserving 100% of existing functionality. **UI and CSS only** — no backend, API, business logic, state, or routing changes.

## Constraints
- No new dependencies (React 19, Vite 8, React Router 7, Recharts only)
- No backend / API / database / auth / JWT changes
- No new functionality or fake data
- Use only existing assets, icons, and components
- Copy the reference logo asset (`app-logo-master.png`) from `sign-frontend/public/` to `public/` — this is an existing asset, not new

---

## Phase 1: Global Design System (Foundation)

### File: `Frontend/src/index.css`

**1.1 Color palette refinements**
- Keep the existing dark theme palette (`--paper`, `--panel`, `--ink`, `--moss`, `--accent`, `--gold`, `--violet`, `--clay`)
- Add `--paper-alt` surface variant for secondary cards (slightly lighter than `--paper`)
- Add `--panel-card` for card backgrounds (slightly lighter than `--panel`)
- Add focus ring / glow utilities: `--focus-ring: rgba(47, 212, 143, 0.3)` (moss) and `--focus-ring-accent: rgba(255, 122, 89, 0.35)` (accent)
- Ensure all text meets WCAG AA contrast (4.5+ on dark backgrounds) — adjust `--muted` if needed

**1.2 Typography system**
- Add CSS variables for heading sizes: `--text-xs`, `--text-sm`, `--text-base`, `--text-lg`, `--text-xl`, `--text-2xl`, `--text-3xl`
- Add `--font-mono` for code-like labels
- Set consistent line-height scale (1.5 for body, 1.2 for headings)

**1.3 Spacing & radius tokens**
- Already has `--radius: 12px` — add `--radius-sm: 8px`, `--radius-lg: 16px`
- Already has spacing values — just document/normalize usage

**1.4 Core utility classes** (add to `index.css`)
- `.card` — base card style: `background: var(--panel)`, `border: 1px solid var(--line)`, `border-radius: var(--radius)`, `padding: 22px`
- `.card-hover` — add hover lift + border glow
- `.section-title` — consistent section heading style with icon support
- `.text-gradient` — gradient text utility (moss→violet)
- `.glass-panel` — subtle frosted effect for overlays

---

## Phase 2: SignLearn Branding & Logo Treatment

### Assets to copy:
- Copy `Frontend/sign-frontend/public/app-logo-master.png` → `Frontend/public/app-logo-master.png`
- Copy `Frontend/sign-frontend/public/lesson_map_bg.png` → `Frontend/public/lesson_map_bg.png` (for decorative backgrounds)

### Files to modify:

**`Frontend/src/components/layout/Sidebar.jsx`**
- Replace the "SL" text badge (`<div className="mark">SL</div>`) with the logo image (`<img src="/app-logo-master.png" alt="SignLearn logo" />`)
- Add nav icons using inline SVG (hand/sign motifs) before each link label — use simple SVGs, no new icon library
- Add a subtle "role badge" at the bottom showing the current user's role
- Ensure sidebar gradient stays but deepen the purple for a richer feel

**`Frontend/src/components/layout/Navbar.jsx`**
- Replace the "SL" mark in navbar with the logo image too
- Make the title dynamic: use `useLocation()` to show the current page name instead of hardcoded "Overview"
- Improve the user-chip: add colored avatar background based on role (learner=moss, instructor=violet, admin=accent, trainer=gold)
- Add a user avatar circle with initials

**`Frontend/src/index.css`** (auth brand)
- Update `.auth-brand .mark` to use the logo image instead of "SL" text
- Keep the auth-shell radial gradient background
- Add a subtle `<div className="hand-motif">` decorative element on auth pages (using 🤟 emoji at low opacity)

**`Frontend/src/pages/Login.jsx`, `Register.jsx`, `ForgotPassword.jsx`**
- No logic changes
- Add decorative hand motif SVG in the background (low opacity)
- Already well-styled — minor tweaks only

---

## Phase 3: Sidebar Enhancement

### File: `Frontend/src/components/layout/Sidebar.jsx`

**3.1 Nav link icons**
- Add inline SVG icons before each link:
  - Dashboard: chart bar icon
  - Lessons: book icon
  - Practice: hand icon
  - Word Practice: hand icon (variant)
  - Reports: document icon
  - Certification: trophy icon
  - Leaderboard: podium icon
  - Profile: user icon
  - Admin: shield icon
  - Instructor: graduation icon
  - Trainer: accessibility icon

**3.2 Active state styling**
- Active link gets a left border gradient (moss → accent)
- Active link gets a subtle background glow
- Hover links get a smooth transition

**3.3 Group labels**
- Separate learner pages from role-specific pages with a subtle divider and label (e.g., "Learner", "Management")

---

## Phase 4: Top Navigation Enhancement

### File: `Frontend/src/components/layout/Navbar.jsx` + `Frontend/src/index.css`

**4.1 Dynamic page title**
- Import `useLocation` from react-router-dom
- Map route paths to display names: `/dashboard` → "Dashboard", `/lessons` → "Lessons", etc.

**4.2 User avatar**
- Replace the `user-chip` div with a proper avatar: colored circle with user initials
- Show full name on hover (keep existing text as well)
- Add a small "role" indicator dot with role color

**4.3 Notification bell visual**
- Already well-implemented — add a subtle badge pulse animation for unread notifications

---

## Phase 5: Shared Cards & Buttons Standardization

### File: `Frontend/src/index.css`

**5.1 Button system** (already has `btn-primary`, `btn-accent`, `btn-secondary`, `btn-inline`)
- Add `btn-sm` and `btn-lg` size variants
- Add `btn-icon` for icon-only buttons (used in tables for edit/delete)
- Standardize `btn-secondary` hover behavior across all pages

**5.2 Card system**
- Ensure all `.stat-card`, `.lesson-card`, `.chart-card`, `.report-panel`, `.badge-card`, `.recommendation-item` use consistent:
  - Padding: 22px
  - Border: 1px solid var(--line)
  - Border-radius: var(--radius)
  - Background: var(--panel) with subtle gradient overlay
  - Hover: transform + shadow lift
- Standardize `.panel-title` style (uppercase label, muted, small) across Reports, Admin, Instructor, Trainer

**5.3 Table system**
- Standardize `.attempts-table` styling: consistent header styling, row hover states, current-user highlighting
- Add `.status-pill` variants for all status types (already has active/inactive)
- Standardize `.weak-letter-badge` and `.letter-chip` usage

**5.4 Form fields**
- Consistent input/select styling (already exists — ensure Admin page inputs use `.field` class instead of raw inputs)

---

## Phase 6: Page-by-Page Visual Polish (Using Existing Data)

### 6.1 Dashboard (`pages/Dashboard.jsx`)

**Current state**: Stats grid (3 stat cards), Badges & Streaks section, Recommended Signs
**Improvements**:
- Add a hero header area with a subtle gradient background or decorative blob behind the stats
- Wrap stat cards in a `.card` container with consistent styling
- Add the existing `AccuracyOverTimeChart` and `LessonsCompletedChart` components (they already exist but are not currently used on Dashboard — the Dashboard only shows stats, not charts)
  - **Note**: Charts use mock data comments — use the data that's already fetched (`stats`). If no chart data is available, show empty state
  - Actually, `getAnalyticsSummary` returns stats but not weekly chart data. `getWeeklyAnalytics` exists in api.js but is not called. **Do NOT wire it up** — just add chart components below stat cards if data exists, otherwise the existing layout stays
- Add a "Welcome back, {name}" header with the date
- Badges section already well-implemented — add a subtle container header style
- Recommendations box already styled well — add a "View all" or section header consistency

### 6.2 Lessons (`pages/Lessons.jsx`)

**Current state**: Grid of lesson cards with status, stars, accuracy
**Improvements**:
- Already very polished with `.lesson-grid` and `.lesson-card`
- Add a header section like Dashboard with page title
- Add a "Start Practice" CTA button for the first unlocked lesson in empty state
- Ensure lesson cards use `.lift-hover` class (currently inline style on cursor)

### 6.3 Practice (`pages/Practice.jsx`)

**Current state**: Letter picker, video frame, timer, attempt progress, check button, results
**Improvements**:
- Already very well-styled
- Move inline styles to CSS classes (the `style={{ cursor: "pointer" }}` should become a class)
- The results section already has good styling — just ensure consistency
- Add the practice header to include a "Back to Lessons" button

### 6.4 Reports (`pages/Reports.jsx`)

**Current state**: Stats grid, attempted letters, weak letters, recommendations, certificate section, download buttons
**Improvements**:
- Remove the `style={{ padding: 30 }}` inline style on the root div — use `.page-body` class instead (it's already in the layout)
- Add section dividers or spacing consistency
- Certificate section already well-styled — ensure consistent with `.chart-card` style
- Download buttons already use `btn-secondary` — ensure consistent sizing

### 6.5 Certification (`pages/Certification.jsx`)

**Current state**: Level cards (exam selection), exam flow (camera + target letter), result display
**Improvements**:
- Level cards already use `.lesson-card` styling — good
- Add `badge-beginner`, `badge-intermediate`, `badge-advanced`, `badge-professional` CSS classes for the level badges (currently inline `<span className="badge badge-beginner">` which doesn't have CSS defined)
- Exam progress: add a visual step indicator ("Question 1 of 5")
- Result section: add a summary card with score visualization

### 6.6 Leaderboard (`pages/Leaderboard.jsx`)

**Current state**: ChampionsRise podium component, toggle buttons, data table
**Improvements**:
- Already very well-styled with ChampionsRise.css
- Add a subtle container around the podium + table
- Ensure table hover states are consistent
- Add a "Your rank" highlight if user is in the list (already done with `current-user-row`)

### 6.7 Profile (`pages/Profile.jsx`)

**Current state**: Account details form, password change form in cards
**Improvements**:
- Already uses `.reference-card` and `.lift-hover` — good
- Add a page header consistent with other pages
- Ensure form buttons use consistent sizing

### 6.8 Admin (`pages/Admin.jsx`)

**Current state**: Users table (with local-only toggle), lessons list with add/edit/delete
**Improvements**:
- The Admin page uses raw `<input>` and `<textarea>` elements without `.field` wrapper classes
- Add `.field` wrappers with proper labels for the add/edit lesson form
- Add `badge-beginner`, `badge-intermediate` etc. CSS classes for role badges
- Add status pill colors (active/inactive already styled)
- Improve the "Add Lesson" form to use consistent input styling

### 6.9 Instructor (`pages/Instructor.jsx`)

**Current state**: Student list (left panel), student detail (right panel)
**Improvements**:
- Already uses `.report-panel` — good
- Add consistent header
- Ensure student row hover states are consistent
- Add avatar/initials for student names

### 6.10 Trainer (`pages/trainer.jsx`)

**Current state**: Learner list (left), learner details (right) with engagement, skill, assessment, certification
**Improvements**:
- Same as Instructor — add header consistency
- The summary rows already use `.summary-row` class — good
- Add section dividers for Engagement/Skill Development/Assessment/Certification subsections

### 6.11 Word Lessons (`pages/WordLessons.jsx`)

**Current state**: Grid of word cards
**Improvements**:
- Already uses `.lesson-grid` and `.lesson-card` — good
- Add a header section
- Improve the "Word Sign" badge styling

### 6.12 Dynamic Practice (`pages/DynamicPractice.jsx`)

**Current state**: Word practice with camera, prediction display
**Improvements**:
- Already reuses practice styles — good
- Remove inline styles where CSS classes exist
- Add a header consistent with Practice page

---

## Files to Change (Complete List)

### CSS Files
1. **`Frontend/src/index.css`** — Global design system, utilities, component styles (~2627 lines, additions only)
2. **`Frontend/src/components/leaderboard/ChampionsRise.css`** — Minor refinements (already well-styled)

### JSX Component Files
3. **`Frontend/src/components/layout/Sidebar.jsx`** — Logo, icons, role grouping
4. **`Frontend/src/components/layout/Navbar.jsx`** — Dynamic title, avatar, logo
5. **`Frontend/src/components/layout/AppLayout.jsx`** — No changes needed (already clean)
6. **`Frontend/src/components/layout/NotificationBell.jsx`** — No logic changes, maybe CSS class tweaks only

### Page Files (styling only, no logic changes)
7. **`Frontend/src/pages/Dashboard.jsx`** — Add header, wrap sections in consistent containers
8. **`Frontend/src/pages/Lessons.jsx`** — Minor card consistency
9. **`Frontend/src/pages/Practice.jsx`** — Move inline styles to CSS
10. **`Frontend/src/pages/Reports.jsx`** — Remove inline padding, use consistent classes
11. **`Frontend/src/pages/Certification.jsx`** — Add badge CSS classes, progress indicator
12. **`Frontend/src/pages/Leaderboard.jsx`** — Container wrapper
13. **`Frontend/src/pages/Profile.jsx`** — Header consistency
14. **`Frontend/src/pages/Admin.jsx`** — Form field wrappers, badge classes
15. **`Frontend/src/pages/Instructor.jsx`** — Minor consistency
16. **`Frontend/src/pages/Trainer.jsx`** — Minor consistency (lowercase filename)
17. **`Frontend/src/pages/WordLessons.jsx`** — Header, badge styling
18. **`Frontend/src/pages/DynamicPractice.jsx`** — Inline style removal, header

### Asset Files
19. **`Frontend/public/app-logo-master.png`** — Copy from sign-frontend
20. **`Frontend/public/lesson_map_bg.png`** — Copy from sign-frontend

### Config Files
21. **`Frontend/index.html`** — Update `<title>` from "sign-frontend" to "SignLearn"
22. **`Frontend/vite.config.js`** — No changes needed

---

## Validation Plan
- Run `npm run dev` (or `npm run build`) to verify no build errors
- Visually verify all 13 pages render correctly
- Verify auth flow (login → dashboard, logout → login) still works
- Verify role-based routing still works (each role sees correct sidebar items)
- Verify all existing functionality (camera practice, predictions, reports, certificates, leaderboard, admin user management) still works
- Run `npm run lint` (oxlint) to verify code quality

## Priority Order
1. Design system tokens + utilities (index.css)
2. Logo asset + sidebar + navbar branding
3. Shared card/button standardization
4. Dashboard + Lessons visual polish
5. Practice + Reports + Certification
6. Leaderboard + Profile + Admin + Instructor + Trainer
7. WordLessons + DynamicPractice
8. index.html title fix
```

