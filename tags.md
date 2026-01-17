---
layout: default
title: 标签
---

<div class="tags-page">
  <h2>文章标签</h2>

  {% if site.tags.size > 0 %}
    <div class="tags-cloud">
      {% for tag in site.tags %}
        {% assign tag_name = tag[0] %}
        {% assign posts = tag[1] %}
        <a href="{{ '/tag/' | append: tag_name | relative_url }}" class="tag-item">
          #{{ tag_name }}
          <span class="tag-count">{{ posts.size }}</span>
        </a>
      {% endfor %}
    </div>

    <div class="tags-list">
      {% for tag in site.tags %}
        {% assign tag_name = tag[0] %}
        {% assign posts = tag[1] %}
        <div class="tag-item-detail">
          <h3 class="tag-name">
            <a href="{{ '/tag/' | append: tag_name | relative_url }}">#{{ tag_name }}</a>
            <span class="tag-count">{{ posts.size }} 篇</span>
          </h3>
          <ul class="tag-posts">
            {% for post in posts %}
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
    <p>还没有标签。</p>
  {% endif %}
</div>

<style>
.tags-page h2 {
  font-size: 28px;
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 2px solid #eaecef;
}

.tags-cloud {
  margin-bottom: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.tags-cloud .tag-item {
  display: inline-block;
  background-color: #0366d6;
  color: #fff;
  padding: 8px 16px;
  margin: 5px;
  border-radius: 20px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.tags-cloud .tag-item:hover {
  background-color: #0256c7;
}

.tag-count {
  opacity: 0.8;
  font-size: 12px;
  margin-left: 5px;
}

.tag-item-detail {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.tag-name {
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag-name a {
  color: #0366d6;
  text-decoration: none;
  font-size: 20px;
}

.tag-name a:hover {
  text-decoration: underline;
}

.tag-name .tag-count {
  background-color: #0366d6;
  color: #fff;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: normal;
}

.tag-posts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tag-posts li {
  padding: 8px 0;
  display: flex;
  align-items: center;
  gap: 15px;
}

.tag-posts .post-date {
  color: #666;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 14px;
  min-width: 100px;
}

.tag-posts a {
  color: #333;
  text-decoration: none;
  font-size: 16px;
}

.tag-posts a:hover {
  color: #0366d6;
}
</style>
