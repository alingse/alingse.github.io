---
layout: default
title: 分类
---

<div class="categories-page">
  <h2>文章分类</h2>

  {% assign categories = site.categories | sort %}
  {% if categories.size > 0 %}
    <div class="categories-list">
      {% for category in categories %}
        <div class="category-item">
          <h3 class="category-name">
            <a href="{{ '/category/' | append: category[0] | relative_url }}">{{ category[0] }}</a>
            <span class="category-count">{{ category[1].size }} 篇</span>
          </h3>
          <ul class="category-posts">
            {% for post in category[1] %}
              <li>
                <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
              </li>
            {% endfor %}
          </ul>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <p>还没有分类。</p>
  {% endif %}
</div>

<style>
.categories-page h2 {
  font-size: 28px;
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 2px solid #eaecef;
}

.category-item {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.category-name {
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-name a {
  color: #0366d6;
  text-decoration: none;
  font-size: 20px;
}

.category-name a:hover {
  text-decoration: underline;
}

.category-count {
  background-color: #0366d6;
  color: #fff;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: normal;
}

.category-posts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-posts li {
  padding: 8px 0;
  display: flex;
  align-items: center;
  gap: 15px;
}

.post-date {
  color: #666;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 14px;
  min-width: 100px;
}

.category-posts a {
  color: #333;
  text-decoration: none;
  font-size: 16px;
}

.category-posts a:hover {
  color: #0366d6;
}
</style>
