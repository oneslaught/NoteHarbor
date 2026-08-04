# 🌅 NoteHarbor

A simple note-taking web app for students that was build using Python Django. This application was created as a project for my university. You can test functionality of the web site by clicking [this link](https://oneslaught.eu.pythonanywhere.com/en/).

## 📀 Video

[NoteHarbor-demo.webm](https://github.com/user-attachments/assets/d8650ad2-994e-46f2-86ab-0a6a6a843734)

## 📦 Technologies used
### Backend: 
- `Django 6`
- `Python`
- `SQLite`
### Frontend:
- `Django Templates`
- `CSS`
- `JavaScript`
- `Alpine.js`
### Development tools:
- `VS Studio`
- `Git + GitHub`
### Deploy:
- `PythonAnywhere`

## ⛵ Features

Here's what you can do with NoteHarbor:
- **Create an account:** Pretty self-explanatory

- **View Notes:** All users have rights to view written notes in the "Explore" section.
- **Filter/Search Notes:** Notes can be filtered by a variety of parameters and found by typing note title in a search bar.
- **Create Notes:** Registered users have ability to create notes in "Home" section.
- **Edit/Delete Notes:** Note owners can edit and delete their notes.
- **Fork Notes:** Users can fork other students' original notes and add changes to them.
- **Rate Notes:** Users can rate other students' notes on a scale from 1 to 5.
- **Add Notes to Favorites:** You can add your favorite notes to the dedicated section in the app. 
- **Change Web-Site Language:** By default the language is set to English, but it can be changed to Ukrainian.

## 🗒️ Development Story
I started NoteHarbor as a university practical assignment - a collaborative note-sharing platform for students. The idea was simple: create a multy-layer Model-View-Controller like web app (and pass the exam).

I started by setting up Django 6 with a PostgreSQL database locally and SQLite for deployment on PythonAnywhere. The first thing I built was the data models Course, Note, Tag, SavedNote and Rating. One early design decision was to detach tags from courses entirely, making them belong directly to notes for more flexible filtering.

Next I implemented user authentication using Django's built-in auth system, extended with a custom Profile model that adds a role system, student and admin. Profiles are created automatically via Django signals whenever a new user registers.

Then came the core note functionality: creating, editing, deleting and viewing notes. I added forking early on, where any user can fork someone else's note and create their own variant, with a traceable link back to the original. The fork logic always traces back to the root note to prevent chains of forks.

After that I built the favorites system and star ratings. Both ended up being converted to AJAX using fetch API and Alpine.js, so actions happen without page reloads.

Filtering and sorting came next as I built a reusable filter_notes and sort_notes system in filters.py that works across all pages. The tag filter uses an Alpine.js dropdown component with live search.

I then added live search using AJAX. As the user types, results appear instantly without reloading the page. The search is context-aware, meaning it searches only within the current section (favorites, my notes, etc.).

Localization was implemented using Django's standard i18n with gettext - the interface is available in English and Ukrainian with a language switcher in the bottom of a sidebar. Currently, there are only 2 languages available: English (default) and Ukrainian.

Finally I added responsive design with CSS media queries and a collapsible hamburger menu for mobile. Finishing touch was deploying the whole website to PythonAnywhere, from where it can be available for people to check out.

## 📜 What I Learned

During this project, I have picked up some important skills and overall have better understanding of:

### ⛓️ Django ORM
Before this project I thought of databases in terms of raw SQL. Working with QuerySets taught me to think in terms of chained filters and lazy evaluation; the database isn't touched until you actually iterate over results, which changed how I structure my views entirely.
### 📚 Django i18n
I never implemented localization before. It was pretty easy to add another language using django-parler library, not that scary as I thought it might be.
### 📢 Django signals
I had no idea Django had an event system. Discovering post_save and building automatic Profile creation on user registration felt like blessing because here it's not mandatory to connect third-party tool to provide this functionality.
### 🔐 Security mindset
This one is the most important of them all. Working with ALLOWED_HOSTS, .env files and understanding why passwords must never be stored in plain text shifted how I think about my web apps - not just "does it work" but "is it safe".
### ⚙️ MVC architecture 
Separating concerns between models, views and templates felt abstract at first, but, by the end, having reusable filters.py, partials in templates and clean views made the codebase genuinely easier to extend and reason about.

## 📈 Overall Growth
This project pushed me from knowing Python syntax to actually building and shipping a full-stack web application. While working on this project, I was able to understand how a real system is structured: how data flows from the database through business logic to the user interface, how authentication and permissions work, how to handle multiple languages, and how to deploy something that other people can actually use. But I must say that most importantly, I have improved at breaking a complex problem into smaller pieces and solving them one at a time.

## 💡 How this project can be improved?
- Replace the plain textarea with a Markdown or WYSIWYG editor (like TipTap or Quill) to make notes significantly more readable and structured.
- Implement ability of tracking edit history so users can see what changed between versions of a note, similar to how Git tracks code.
- Currently only admins can create courses. Letting verified users propose new courses would make the platform more self-sufficient.
- Make search improvements - implement full-text search across note content (not just titles).
- Add more languages to reach a wider audience of users.
- Allow users to export notes as PDFs so that they can study and repeat material online.
