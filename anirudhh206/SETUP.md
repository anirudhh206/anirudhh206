# Setup (about 10 minutes)

This file lives in the repo but is not shown on your profile. Only `README.md` is.

## 1. Push this folder to `anirudhh206/anirudhh206`

The repo must be **public** and named exactly like your username. If it already exists, push this folder's contents to its default branch (`main`).

## 2. Count private contributions

GitHub → Settings → Public profile → Contributions & activity → tick **Include private contributions on my profile**. Without it the streak and 3D city show less than you really did.

## 3. Create the `GH_PAT` secret

1. GitHub → Settings → Developer settings → Personal access tokens → **Tokens (classic)** → Generate new token.
2. Scopes: `repo` and `read:user`. Expiry: the longest you are comfortable with (put the renewal date in your calendar).
3. In the profile repo: Settings → Secrets and variables → Actions → **New repository secret** → name `GH_PAT`, paste the token.

Never paste the token into chat or commit it to a file.

The workflows fall back to the built-in `GITHUB_TOKEN` if `GH_PAT` is missing. They still run, but they only see public stats, and the keep-alive commit may not reset GitHub's 60-day inactivity timer.

## 4. Run each workflow once

Actions tab → pick each workflow → **Run workflow**:

1. **Update profile cards** (stats, languages, streak)
2. **GitHub-Profile-3D-Contrib** (the 3D city)

Until they run, the README shows dark "Initialising" placeholders in those slots. After the first run they are replaced and then refresh daily.

## 5. Keep it alive

GitHub disables scheduled workflows after 60 days without repository activity. The **Keep alive** workflow makes one small commit a month using `GH_PAT`. Still glance at the Actions tab every month or two and re-enable anything marked disabled.

## Editing the design

Everything hand-designed comes from `tools/generate_assets.py`. Change text, colours, project descriptions or chips in the CONFIG block at the top, then run:

```
python3 tools/generate_assets.py
```

and commit the updated `assets/`. It needs only Python 3, no packages. It never overwrites real stats cards that the workflows have already generated.

## Notes

- SVG text uses system fonts (Inter if installed, otherwise Segoe UI / SF / Helvetica). GitHub blocks external fonts inside README images.
- Animated pieces: hero aurora, the glow dot on the price line, the typing line, and the divider dot. All honour "reduce motion".
- To use the contribution snake instead of the 3D city, add a workflow with `Platane/snk/svg-only@v3` and swap the image in the README.
