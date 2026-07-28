# Setup Checklist — princeji2/princeji2

Do these in order. Test after each phase before moving to the next.

## 0. The profile repo
1. Go to github.com/new
2. Repository name: `princeji2` (exactly your username)
3. Public, tick "Add a README file" → Create
4. Upload `dark.svg` and `light.svg` to the repo root (Add file → Upload files)

## 1. Banner
Already wired into `README.md` via a `<picture>` tag pointing at
`raw.githubusercontent.com/princeji2/princeji2/main/{dark,light}.svg`.
Test: Settings → Appearance → toggle theme, reload your profile page.

File-size note: `dark.svg` is ~840KB, `light.svg` is ~1.7MB (light mode keeps
the background dithered too, per the original spec, so it has ~3x the dots).
Both are within GitHub's render limits but on the heavy side — say the word
if you'd like me to cut dot density to shrink them.

## 2. Stats cards — self-hosting (~20 min)
The public `github-readme-stats` instance is shared by thousands and returns
"API rate limit exceeded" constantly. Self-hosting fixes that permanently.

**a) Create a GitHub token**
- github.com/settings/tokens → Tokens (classic) → Generate new token (classic)
- Note: `readme-stats` · Expiration: No expiration
- Scope: tick `repo` (the whole group)
- Generate → **copy it immediately**, GitHub shows it once. Never paste this
  into a chat, a public repo, or a website — only into the Vercel field below.

**b) Fork and deploy**
1. Fork github.com/anuraghazra/github-readme-stats
2. vercel.com → Sign up with GitHub → Hobby (free) plan
3. Add New… → Project → Import your fork
4. Leave build settings untouched
5. Environment Variables → name `PAT_1`, value = your token
6. Deploy, wait ~2 min
7. Copy your instance URL: `your-instance.vercel.app`

**c) Wire it into the README**
Open `README.md`, find the two lines with `YOUR-INSTANCE.vercel.app` and
replace both with your real Vercel URL. Verify first at:
`https://your-instance.vercel.app/api?username=princeji2&show_icons=true`

## 3. Contribution snake (~10 min)
1. Repo → Settings → Actions → General → Workflow permissions → **Read and
   write permissions** → Save (this is the repo's settings, not your account's)
2. Add file → Create new file → name it exactly `.github/workflows/snake.yml`
   → paste the contents of the `snake.yml` I generated → Commit to `main`
3. Actions tab → confirm the run goes green (~1 min) and creates an `output` branch
4. Only after that branch exists, the snake `<picture>` block already in the
   README (pointing at the `output` branch) will render instead of showing broken

## 4. Badges
Already in the README: LinkedIn (brand blue, required — shields.io's LinkedIn
glyph only renders on `#0A66C2`) and Email. Let me know if you want to add a
portfolio link, Instagram, or Facebook badge — just send the URL/handle.

## 5. Final assembly
`README.md` is already the complete file — banner, streak/stats/top-langs,
snake, badges, all pointed at `princeji2`. Once you've done steps 2b/2c and 3,
drop it into the repo root and you're live.

---

### One honest caveat
Your photo has a real (blurred) background rather than a flat studio one —
the spec calls a busy background "the single biggest cause of a poor result."
I ran GrabCut segmentation to separate you from it for dark mode, and it came
out clean, but if you look at the banner and the edges look rough anywhere,
that's the reason, and it's fixable by re-cropping tighter or trying a plainer
photo.

### One simplification I made
The spec's ~3.2s "scattered intro" fade-in (a one-time reveal on first load,
via a duplicate ~180KB layer) is skipped — the banner starts directly at the
loop's resting portrait frame. Say so if you want that added back in; it's a
straightforward addition, just extra file weight.
