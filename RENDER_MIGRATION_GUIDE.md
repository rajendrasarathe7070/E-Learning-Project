# SQLite3 to PostgreSQL Migration Guide for Render (Free Tier)

## 🚀 Quick Start (3 Steps)

### Step 1: Export Your Local Data

On your **local machine**, run this command:

```bash
python manage.py dumpdata --all -o data.json
```

**What this does:**
- Exports ALL your data (Notes, Books, Syllabus, PYQ, Users, etc.)
- Creates a file called `data.json` (~few MB)

---

### Step 2: Commit & Push to GitHub

```bash
git add data.json
git commit -m "Add initial data for PostgreSQL migration"
git push origin main
```

**Render will automatically:**
1. Pull the new code
2. Install dependencies
3. Create PostgreSQL tables
4. **Load data.json into PostgreSQL** ✅

---

### Step 3: Verify Data on Render

After deployment finishes:

```bash
https://your-app.onrender.com/admin/
```

- Login with your admin account
- Check if Notes, Books, Syllabus, etc. are there ✅

---

## 📊 What Gets Migrated?

✅ All Users
✅ All Notes
✅ All Books  
✅ All Syllabus
✅ All PYQ (Previous Year Questions)
✅ All Doubts & Replies
✅ All Bookmarks
✅ Admin data

---

## ⚠️ Important Notes

1. **File Size Limit**: Render free tier can handle up to 512 MB (your data.json should be < 10 MB)

2. **After First Deploy**: 
   - You can remove `data.json` from repo if you want
   - Or keep it as backup

3. **Adding New Data**:
   - Use Admin Panel: `https://your-app.onrender.com/admin/`
   - Data will be saved to PostgreSQL permanently ✅

4. **Local Development**:
   - You can still use SQLite3 locally
   - Just switch back to SQLite in `.env` if needed

---

## 🔄 If Migration Fails

Check Render logs:
1. Go to Render Dashboard
2. Select your service
3. Go to **Logs** tab
4. Look for error messages

---

## 📝 Troubleshooting

### Q: Data not showing after deploy?
A: Check admin panel, database might be empty. Re-run migration:
```bash
python manage.py dumpdata --all -o data.json
git add data.json
git push
```

### Q: File too large?
A: Filter specific apps:
```bash
python manage.py dumpdata core accounts -o data.json
```

### Q: Want to update data later?
A: Use Admin Panel - `https://your-app.onrender.com/admin/`

---

## ✅ Success!

Once done:
- 🎉 Your app runs on PostgreSQL
- 🎉 All your data is migrated
- 🎉 Server never sleeps (health check keeps it alive)
- 🎉 Data persists between restarts ✅

---

**Need help?** Check the logs or create an issue! 🚀
