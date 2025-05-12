# 🧠 Git Command Cheatsheet for This Project

Use this reference to manage version control for your forecasting dashboard project.

---

## 🔧 Setup

```bash
git init                                 # Initialize Git in project
git remote add origin <repo_url>         # Connect to GitHub
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## 📥 Adding & Committing Changes

```bash
git add .                                # Stage all changes
git commit -m "Meaningful message"       # Save a snapshot
```

---

## 📤 Pushing to GitHub

```bash
git push -u origin main                  # First time push
git push                                 # Next time (same branch)
```

---

## 🌱 Branching (Recommended for Each Phase)

```bash
git checkout -b phase-1                  # Create new branch
git switch phase-1                       # (or use checkout)
```

To merge when done:

```bash
git checkout main
git merge phase-1
git push
```

---

## 🔄 Pulling Updates from GitHub

```bash
git pull origin main                     # Get latest changes
```

---

## 🏷 Tagging Releases (Optional but Useful)

```bash
git tag -a v1.0 -m "Finish Phase 1"
git push origin v1.0
```

---

## ✅ Useful Tips

- `git status` — see what’s changed
- `git log` — view commit history
- `git diff` — see file differences

---

📁 Save this file as `git_command_cheatsheet.md` in your project root.
