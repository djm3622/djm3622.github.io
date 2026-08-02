---
layout: home
title: "Home"
---

<style>
  .home-intro {
    max-width: 760px;
    margin: 30px 0 52px;
    padding: 34px 36px;
    background: linear-gradient(135deg, var(--site-hero-start) 0%, var(--site-hero-end) 72%);
    border: 1px solid var(--site-border);
    border-radius: 18px;
    box-shadow: 0 10px 30px var(--site-shadow);
  }

  .home-kicker {
    margin: 0 0 10px;
    color: var(--site-accent);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .home-lead {
    max-width: 660px;
    margin: 0;
    color: var(--site-heading);
    font-size: clamp(1.35rem, 3vw, 1.85rem);
    font-weight: 560;
    line-height: 1.35;
  }

  .home-summary {
    max-width: 650px;
    margin: 18px 0 0;
    color: var(--site-muted);
    font-size: 1.05rem;
    line-height: 1.7;
  }

  .home-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 24px;
  }

  .home-actions a {
    padding: 8px 14px;
    border: 1px solid var(--site-border-strong);
    border-radius: 999px;
    color: var(--site-accent-strong);
    font-size: 0.92rem;
    font-weight: 600;
    text-decoration: none;
  }

  .home-actions a:first-child {
    background: var(--site-accent);
    border-color: var(--site-accent);
    color: var(--site-button-text);
  }

  .home-actions a:hover {
    box-shadow: 0 4px 12px var(--site-shadow);
    transform: translateY(-1px);
  }

  .home-updates {
    margin: 8px 0 36px;
  }

  .modern-section-heading {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 18px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--site-border);
  }

  .modern-section-heading h2 {
    margin: 0;
    color: var(--site-heading);
    font-size: 1.35rem;
    letter-spacing: -0.01em;
  }

  .modern-section-heading span {
    color: var(--site-muted-soft);
    font-size: 0.88rem;
  }

  .modern-post-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin: 0;
    list-style: none;
  }

  .modern-post-list li {
    padding: 18px;
    background: var(--site-surface);
    border: 1px solid var(--site-border);
    border-radius: 12px;
    transition: border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
  }

  .modern-post-list li:hover {
    border-color: var(--site-border-strong);
    box-shadow: 0 8px 22px var(--site-shadow);
    transform: translateY(-2px);
  }

  .modern-post-list .post-meta {
    display: block;
    margin-bottom: 7px;
    color: var(--site-muted-soft);
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .modern-post-list .post-link {
    color: var(--site-heading);
    font-size: 1rem;
    font-weight: 650;
    line-height: 1.4;
    text-decoration: none;
  }

  @media (max-width: 650px) {
    .home-intro {
      margin: 10px 0 34px;
      padding: 24px 20px;
    }
    .modern-post-list { grid-template-columns: 1fr; }
    .modern-post-list li { padding: 16px; }
    .modern-section-heading { align-items: flex-start; flex-direction: column; gap: 4px; }
    .home-updates { margin-bottom: 26px; }
  }
</style>

<section class="home-intro">
  <p class="home-kicker">David Millard</p>
  <p class="home-lead">Research at the intersection of machine learning, controls, scientific computing, and audio.</p>
  <p class="home-summary">My interests include probabilistic ML, physical modeling, automatic music transcription, digital watermarking, and text-to-speech systems.</p>
  <div class="home-actions">
    <a href="{{ '/publications/' | relative_url }}">Explore my research</a>
    <a href="{{ '/about/' | relative_url }}">About my background</a>
  </div>
</section>
