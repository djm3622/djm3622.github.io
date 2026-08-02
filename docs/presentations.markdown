---
layout: page
title: Presentations
permalink: /presentations/
description: Research presentations by David Millard, including work on self-supervised representation learning for audio information research.
---

<style>
  .presentation-card {
    margin-top: 30px;
    padding: 28px;
    background: linear-gradient(145deg, var(--site-surface-soft) 0%, var(--site-surface) 62%);
    border: 1px solid var(--site-border);
    border-radius: 16px;
    box-shadow: 0 8px 26px var(--site-shadow);
  }

  .presentation-kicker {
    margin: 0 0 8px;
    color: var(--site-accent);
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.11em;
    text-transform: uppercase;
  }

  .presentation-card h2 {
    margin: 0;
    color: var(--site-heading);
    font-size: 1.35rem;
    letter-spacing: -0.01em;
    line-height: 1.4;
  }

  .presentation-summary {
    max-width: 730px;
    margin: 12px 0 0;
    color: var(--site-muted);
    line-height: 1.65;
  }

  .presentation-embed {
    position: relative;
    width: 100%;
    padding-top: 56.25%;
    margin: 24px 0 18px;
    overflow: hidden;
    background: var(--site-surface-muted);
    border: 1px solid var(--site-border);
    border-radius: 12px;
  }

  .presentation-embed iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: 0;
  }

  .presentation-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 0;
  }

  .presentation-actions a {
    padding: 7px 13px;
    border: 1px solid var(--site-border-strong);
    border-radius: 999px;
    color: var(--site-accent-strong);
    font-size: 0.88rem;
    font-weight: 600;
    text-decoration: none;
  }

  .presentation-actions a:first-child {
    background: var(--site-accent);
    border-color: var(--site-accent);
    color: var(--site-button-text);
  }

  .presentation-actions a:hover {
    box-shadow: 0 4px 12px var(--site-shadow);
    transform: translateY(-1px);
  }

  @media (max-width: 650px) {
    .presentation-card {
      margin-top: 10px;
      padding: 20px 16px;
    }
  }
</style>

<section class="presentation-card">
  <p class="presentation-kicker">Audio information research</p>
  <h2>Self-Supervised Representation Learning for Audio Information Research</h2>
  <p class="presentation-summary">This presentation covers the development of self-supervised representation learning for audio information research, including WaveNet, wav2vec, VQ-wav2vec, wav2vec 2.0, HuBERT, and WavLM.</p>

  <div class="presentation-embed">
    <iframe
      src="{{ '/assets/presentations/maad_week3.pdf' | relative_url }}#view=FitH"
      title="Self-Supervised Representation Learning for Audio Information Research"
      loading="lazy"
      allowfullscreen>
    </iframe>
  </div>

  <p class="presentation-actions">
    <a href="{{ '/assets/presentations/maad_week3.pdf' | relative_url }}" target="_blank">Open PDF</a>
    <a href="{{ '/assets/presentations/maad_week3.pptx' | relative_url }}">Download PowerPoint</a>
  </p>
</section>
