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
bundle exec jekyll serve
```

Then visit http://localhost:4000

## Deployment

The site is automatically deployed to GitHub Pages when changes are merged to the `main` branch via GitHub Actions.

## Customization

1. Edit `webpage/_config.yml` to update site title and description
2. Edit `webpage/index.md` to update the homepage content
3. Add new pages as `.md` files in the `webpage/` directory
4. Custom styling can be modified in `webpage/_sass/minimal-custom.scss`

## License

The Jekyll Minimal theme is licensed under CC0 1.0 Universal.
