---
layout: home
title: "Home"
description: Research website of David Millard, a Ph.D. student at the University of Rochester working in machine learning, scientific computing, controls, and audio.
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

  .home-name {
    margin: 0 0 10px;
    color: var(--site-heading);
    font-size: clamp(1.65rem, 4vw, 2.15rem);
    font-weight: 650;
    letter-spacing: -0.025em;
    line-height: 1.2;
  }

  .home-lead {
    max-width: 660px;
    margin: 0;
    color: var(--site-muted);
    font-size: 1.08rem;
    font-weight: 500;
    line-height: 1.55;
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
  <h1 class="home-name">Hey, I'm David.</h1>
  <p class="home-lead">Ph.D. researcher in machine learning, scientific computing, controls, and audio at the University of Rochester.</p>
  <div class="home-actions">
    <a href="{{ '/publications/' | relative_url }}">Explore my research</a>
    <a href="{{ '/about/' | relative_url }}">About my background</a>
  </div>
</section>
