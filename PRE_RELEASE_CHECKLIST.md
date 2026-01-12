# 🚀 Pre-Release Checklist

Follow these steps **before every release** to catch errors early:

## 📋 Before Committing

### 1. Test Notebooks Execute Cleanly
```powershell
nbdev_test --path nbs/
```
**What it does:** Executes all notebooks from scratch (same as GitHub Actions)  
**Why:** Catches execution errors that cached outputs hide

### 2. Run Full Preparation
```powershell
nbdev_prepare
```
**What it does:** Runs `nbdev_export` + `nbdev_test` + `nbdev_clean` + `nbdev_readme`  
**Why:** Ensures everything is in sync before pushing

### 3. Preview Docs Locally
```powershell
nbdev_preview
```
**What it does:** Starts local docs server  
**Why:** Visual check that docs look correct

---

## 🔄 Push to GitHub

```powershell
git add -A
git commit -m "Your descriptive message"
git push
```

---

## ✅ Verify GitHub Actions

1. **Check build status:**  
   https://github.com/abhisheksreesaila/fh-matui/actions

2. **Wait for green checkmark** ✓

3. **Verify docs deployed:**  
   https://abhisheksreesaila.github.io/fh-matui/

---

## 📦 Release (only after GitHub Actions pass)

Run the release script:
```powershell
.\release_cmd.ps1
```

Or manually:
```powershell
# 1. Load GitHub token
$env:GITHUB_TOKEN = [Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")

# 2. Create GitHub release
nbdev_release_git

# 3. Build package
Remove-Item -Recurse -Force dist
python -m build

# 4. Upload to PyPI
twine upload dist/*
```

---

## 🐛 Common Issues

### "show_doc(X) failed"
- `show_doc()` only works on classes/functions, not instances
- Remove `show_doc()` calls on instances like `ButtonT`, `AT`, etc.

### "Import error: socket/subprocess/time"
- These imports should be in `#| eval: false` cells only
- Never put them in `#| export` cells

### "File already exists" on PyPI
- Bump version in `settings.ini` before releasing
- PyPI doesn't allow re-uploading same version

---

## 💡 Quick Reference

| Command | Purpose |
|---------|---------|
| `nbdev_test --path nbs/` | Execute all notebooks fresh |
| `nbdev_prepare` | Full pre-commit check |
| `nbdev_preview` | Local docs server |
| `nbdev_docs` | Rebuild docs |
| `nbdev_release_git` | Create GitHub release |
| `python -m build` | Build Python package |
| `twine upload dist/*` | Upload to PyPI |
