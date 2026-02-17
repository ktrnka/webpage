---
layout: default
title: Blog
---

<style>
article.post {
  margin-bottom: 3em; /* Largest space: between posts */
}

article.post h2 {
  margin-bottom: 0.25em; /* Smallest space: between title and date */
}

article.post time {
  display: block;
  margin-bottom: 1em; /* Medium space: between date and excerpt */
  color: #666;
}
</style>

{% for post in site.posts %}
<article class="post">
  <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
  <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
  {% if post.excerpt %}
  <p>{{ post.excerpt | strip_html | truncatewords: 50 }}</p>
  {% endif %}
</article>
{% endfor %}
