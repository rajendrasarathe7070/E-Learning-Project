# Kotlin Android App Generation Prompt

This prompt is based on the current Django web project in this repository, which is an educational resource platform for notes, books, previous year questions, syllabi, doubts, and user profiles.

## Objective
Create a modern Android application in Kotlin that converts the web platform into a mobile-first experience using Jetpack Compose, MVVM architecture, Material 3, and a clean repository pattern.

## Project Summary from the Existing Web App
The current application provides:
- User authentication (login, register, logout)
- Notes upload and browsing by branch, semester, subject, and unit
- Book catalog with ratings and PDF links
- PYQ (previous year question papers) listing and filtering
- Syllabus browsing with unit breakdowns
- Community doubts forum with replies and best-answer marking
- User profile with uploads and saved notes
- Bookmarking support for notes

## Existing Backend API Reference
The backend already exposes these API endpoints:
- /api/health/
- /api/notes/
- /api/notes/upload/
- /api/notes/<id>/download/
- /api/notes/<id>/bookmark/
- /api/books/
- /api/pyqs/
- /api/syllabus/
- /api/doubts/
- /api/doubts/ask/
- /api/doubts/<id>/reply/
- /api/profile/
- /api/profile/update/
- /api/user/uploads/
- /api/user/saved/

## Kotlin App Requirements
Build an Android app that mirrors the web platform with these core screens:

1. Splash / Welcome Screen
   - App logo and branding
   - Optional onboarding flow

2. Authentication
   - Login screen
   - Register screen
   - Logout flow
   - Secure token/session handling

3. Home Dashboard
   - Cards for Notes, Books, PYQs, Syllabus, Doubts, Profile
   - Search bar
   - Quick actions

4. Notes Screen
   - List notes with title, subject, branch, semester, and tags
   - Search and filter by branch and semester
   - Open note details
   - Bookmark note
   - Open PDF from URL or local file
   - Show download count

5. Books Screen
   - Grid or list of books
   - Filter by branch and semester
   - Book detail page with description and rating
   - Open PDF link

6. PYQ Screen
   - Filter by subject, branch, semester, year, and exam type
   - Show question paper cards
   - Open PDF or external resource

7. Syllabus Screen
   - Show syllabus cards by subject and semester
   - Expand units in detail view
   - Open PDF or external link

8. Doubts Forum
   - Display doubts list
   - Create new doubt
   - View doubt details
   - Add replies
   - Allow marking a reply as best answer

9. Profile Screen
   - Show profile info, branch, semester, bio, avatar
   - Edit profile
   - Show uploaded resources
   - Show saved/bookmarked notes

## Technical Stack
Use the following stack:
- Kotlin
- Jetpack Compose for UI
- Material 3 design system
- MVVM architecture
- Repository pattern
- Retrofit + OkHttp for network calls
- Hilt for dependency injection
- Room for offline caching/local persistence
- Navigation Compose for screen navigation
- Kotlin Coroutines + StateFlow/SharedFlow
- Coil for image loading

## Functional Requirements
- Support login and registration using the existing backend
- Handle loading, error, and empty states properly
- Ensure all screens are responsive and mobile-friendly
- Provide search and filter capabilities for notes/books/PYQs
- Use secure storage for auth tokens when possible
- Add local caching so content remains accessible offline
- Support dark mode
- Show clear feedback for bookmarking, upload, and save actions

## UI/UX Requirements
- Clean, modern, student-friendly interface
- Card-based layout for resources
- Fast navigation with bottom navigation or navigation drawer
- Reusable components for list items, cards, detail screens, and forms
- Smooth transitions and polished animations

## Suggested App Architecture
- data/remote: API service and DTOs
- data/local: Room entities, DAO, database
- data/repository: repository implementations
- domain: models, use cases, repository interfaces
- ui: composables, screens, navigation, view models
- utils: constants, extensions, network helpers

## Acceptance Criteria
The app should:
- Compile successfully in Android Studio
- Support core authentication flows
- Display and browse notes/books/PYQs/syllabus/doubts
- Allow bookmarking and profile management
- Use the backend API as the primary data source
- Provide a polished and functional mobile experience

---

## Ready-to-Paste Prompt

You are an expert Android developer. Convert the existing Django-based educational web application in this repository into a modern Android app written in Kotlin.

The app should be built with Jetpack Compose, Material 3, MVVM, Retrofit, Hilt, Room, Navigation Compose, and Kotlin Coroutines. The app must preserve the core features of the web app while adapting them for mobile use.

Use the backend API endpoints already present in the project as the primary data source. The app should support:
- Login, register, and logout
- Home/dashboard with quick access to notes, books, PYQs, syllabus, doubts, and profile
- Notes listing with search and filters by branch and semester
- Note detail screen with bookmark support and ability to open PDF/document links
- Books listing and detail screen with rating display
- PYQs listing with filters by branch, semester, year, and exam type
- Syllabus listing with unit details
- Doubts forum with creating doubts, viewing posts, adding replies, and marking the best answer
- Profile screen with editable personal information, uploaded resources, and saved notes

Implement a clean architecture with separate layers for data, domain, and UI. Add loading, empty, and error states. Support offline caching with Room. Add secure token handling for authentication. Follow Android best practices and produce production-quality code with reusable composables and a polished Material 3 UI.

Generate a complete Android Studio project structure, all necessary Kotlin files, navigation setup, API integration code, view models, repositories, and UI screens. Keep the implementation realistic and maintainable. Do not just provide a summary; create the actual code structure and implementation plan.
