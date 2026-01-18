---
layout: default
title: 归档
---

<div class="archive">
  <h2>文章归档</h2>

  {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}

  {% for year_group in posts_by_year %}
    <div class="archive-year">
      <h3>{{ year_group.name }}</h3>
      {% assign posts_by_month = year_group.items | group_by_exp: "post", "post.date | date: '%B'" %}
      {% for month_group in posts_by_month %}
        <div class="archive-month">
          <h4>{{ month_group.name }}</h4>
          <ul class="archive-list">
            {% for post in month_group.items %}
              <li>
                <span class="archive-date">{{ post.date | date: "%m-%d" }}</span>
                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                {% if post.categories %}
                <span class="archive-categories">
                  {% for category in post.categories %}
                    <a href="{{ '/categories/#' | append: category | relative_url }}" class="category-tag">{{ category }}</a>
                  {% endfor %}
                </span>
                {% endif %}
              </li>
            {% endfor %}
          </ul>
        </div>
      {% endfor %}
    </div>
  {% endfor %}

  {% if site.posts.size == 0 %}
    <p>还没有发布任何文章。</p>
  {% endif %}
</div>

<style>
.archive h2 {
  font-size: 28px;
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 2px solid #eaecef;
}

.archive-year {
  margin-bottom: 40px;
}

.archive-year h3 {
  font-size: 24px;
  color: #0366d6;
  margin-bottom: 15px;
}

.archive-month {
  margin-left: 20px;
  margin-bottom: 20px;
}

.archive-month h4 {
  font-size: 18px;
  color: #666;
  margin-bottom: 10px;
}

.archive-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.archive-list li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.archive-date {
  color: #666;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 14px;
  min-width: 50px;
}

.archive-list a {
  color: #333;
  text-decoration: none;
  font-size: 16px;
}

.archive-list a:hover {
  color: #0366d6;
}

.category-tag {
  display: inline-block;
  background-color: #f6f8fa;
  color: #0366d6;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  margin-left: 5px;
  text-decoration: none;
}

.category-tag:hover {
  background-color: #e1e4e8;
}
</style>
