# Defense Desk Archive

A public, searchable archive of your threads, charts and historical finds. It's free to host on GitHub Pages and anyone can read it without an account.

## What's in it

- **Archive page**: search (press `/`), filter by Threads, Charts or Historical, filter by tag, and sort. Filters stay in the address, so `yoursite/?tag=artillery` is a shareable link.
- **A page for every entry**, numbered TH-0001, CH-0001 or HX-0001. When you post the link on X it shows a large preview card with your cover image.
- **Threads** are shown post by post, numbered 1/n, 2/n.
- **Charts and photos** open in a lightbox with a download button.
- **Timeline** of historical finds, ordered by year.
- **Series**: give several entries the same series name and they link to each other ("part 2 of 4").
- **Related entries** chosen by shared tags, plus Copy link and Copy citation buttons.
- **RSS feed** at `/feed.xml` and a sitemap, so followers can subscribe and search engines can find entries.

## One-time setup (about 10 minutes)

1. **Create a GitHub account** if you don't have one.
2. **Make a new repository** named `<your-username>.github.io` (public). With that name the site lives at `https://<your-username>.github.io`.
3. **Upload these files**: on the repo page click *Add file → Upload files*, drag in everything from this folder, then commit. The `.pages.yml` file starts with a dot, so check it went up.
4. **Turn on Pages**: go to *Settings → Pages*, set *Source* to "Deploy from a branch", choose the `main` branch and the `/ (root)` folder, then save. The site goes live in a minute or two.
5. **Edit `_config.yml`** (click it, then the pencil icon): set `title`, `description`, `author`, `x_handle`, `twitter.username` and `url`.
   If you named the repo something other than `<username>.github.io`, also set `baseurl: "/repo-name"`.
6. Fill in `about.md` the same way.

## Adding entries

### The easy way: Pages CMS (a form in your browser)
Go to **https://app.pagescms.org**, sign in with GitHub and pick your repo. You'll see *Archive entries* with a form: title, type, date, cover image upload, tags, sources and text. Save, and the site rebuilds in about a minute.

### By hand
Add a file to `_entries/` named like `2026-11-24-my-thread-title.md`:

```markdown
---
title: "Why 155mm output still lags demand"
type: thread            # thread | chart | historical
date: 2026-11-24
link: https://x.com/yourhandle/status/123
image: /media/155-output.png     # upload images to the media/ folder
tags: [artillery, production]
series: "Shell production"       # optional
sources:
  - "Report name, publisher, date — https://link"
---
First post of the thread.

Second post. Blank line between each one.
```

Historical finds also take `year: 1944` (for the timeline) and `era: "Second World War"`.

## Housekeeping

- **Delete the three example entries** in `_entries/` (they're marked "delete me") and `media/example-chart.png`.
- File numbers are assigned by date order within each type. To fix one permanently, add `number: 12` to that entry.
- Images: PNG or JPG around 1200×675 make the best X preview cards.
