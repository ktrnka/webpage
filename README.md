# Personal Webpage

A fast and lightweight personal webpage built with Jekyll and the Minimal theme.

## Design Principles

- **Fast and Light**: Minimal JavaScript, primarily HTML and CSS
- **No Custom Fonts**: Uses system fonts for better performance
- **No Analytics Trackers**: Privacy-focused
- **Based on Minimal Theme**: Clean and simple design

## Structure

- `/webpage/` - Jekyll site source files
- `.github/workflows/jekyll.yml` - GitHub Actions workflow for automatic deployment

## Local Development

To run the site locally:

```bash
cd webpage
bundle install
bundle exec jekyll serve --livereload
```

Then visit http://localhost:4000

## Deployment

The site is automatically deployed to GitHub Pages when changes are merged to the `main` branch via GitHub Actions.

## Maintenance

### Updating & pinning GitHub Actions

Actions in `.github/workflows/` are pinned to commit SHAs (with `# vX.Y.Z` comments) to defend against tag-retargeting attacks. To bump them to the latest releases and re-pin, run from the repo root:

```bash
npx actions-up            # interactive: pick which to update, re-pins to SHA
npx actions-up --dry-run  # preview available updates without changing files
npx actions-up --yes      # apply all updates non-interactively
```

[`actions-up`](https://github.com/azat-io/actions-up) scans the workflows, finds newer releases, and rewrites each `uses:` to `@<sha> # <tag>`. Review every SHA change before committing — a changed SHA is exactly what a retargeting attack looks like. Re-run when you see Node-version deprecation warnings in Actions logs.

## License

The Jekyll Minimal theme is licensed under CC0 1.0 Universal.
