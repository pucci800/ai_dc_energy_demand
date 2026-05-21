# ETL Pipeline Project – Error & Fix Log

Documenting the most important trials and lessons learned while building the **AI Data Center Energy Demand** ETL pipeline.

_Last updated: June 15, 2025_

---

## Git & GitHub Issues

### 1. 403 Permission Denied
- Error: `Permission to repo denied`
- **Cause**: GitHub deprecated username/password login.
- **Fix**: Created a Personal Access Token (PAT) and configured it using `git config --global credential.helper osxkeychain`.

### 2. Push Rejected (non-fast-forward)
- **Error**: `Updates were rejected...`
- **Cause**: Remote repo had commits not present locally.
- **Fix**: Pulled with `git pull origin main --rebase` and then pushed successfully.

### 3. .gitignore Ignored Critical Files
- **Error**: `The following paths are ignored by .gitignore: screenshots/`
- **Fix**: Removed `screenshots/` from `.gitignore`, then committed and pushed screenshot files.

---

## Tableau Dashboard Issues

### 4. Broken Tableau Link (404 Error)
- **Error**: "Where's the viz?" page on Tableau Public
- **Cause**: Linked to a worksheet or profile URL instead of the dashboard
- **Fix**: Re-published directly from the dashboard tab and copied the `/views/...` URL

### 5. Overwriting Without Verifying Visibility
- **Error**: Dashboard appeared but wouldn't load in README
- **Fix**: Verified overwrite prompt was accepted in Tableau → published correctly → used direct view URL

---

## 📁 Structural or Process Errors

### 6. Screenshot Not Showing in README
- **Error**: Screenshot images didn't render
- **Cause**: GitHub paths or image names mismatched or blocked by .gitignore
- **Fix**: Correctly added to repo and used relative markdown paths

---

## ✅ Final Best Practices

- Always run `git status` and `git log` before `git push`
- Use **Tableau dashboard tab** when publishing, not worksheet view
- Never trust your `.gitignore` blindly — verify what's being committed
- Markdown preview in GitHub before pushing README changes
- Maintain a `/logs` folder for long-term learning and transparency

---

You made it through. These mistakes are your **battle scars** — wear them with pride.
