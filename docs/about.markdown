---
layout: page
title: About
permalink: /about/
description: Background, education, research interests, and contact information for David Millard, a Ph.D. student at the University of Rochester.
---

<style>
  .about-page {
    box-sizing: border-box;
    max-width: 780px;
    margin: 18px auto 36px;
  }

  .about-heading {
    margin-bottom: 20px;
  }

  .about-heading h1 {
    margin: 0 0 6px;
    font-size: clamp(1.75rem, 4vw, 2.2rem);
    font-weight: 650;
    letter-spacing: -0.025em;
    line-height: 1.2;
  }

  .about-heading p {
    margin: 0;
    color: var(--site-muted);
    font-size: 1.02rem;
  }

  .about-card {
    display: grid;
    grid-template-columns: 172px minmax(0, 1fr);
    gap: 34px;
    padding: 30px;
    background: linear-gradient(145deg, var(--site-surface-soft) 0%, var(--site-surface) 62%);
    border: 1px solid var(--site-border);
    border-radius: 18px;
    box-shadow: 0 10px 30px var(--site-shadow);
  }

  .about-profile {
    min-width: 0;
  }

  .about-photo {
    display: block;
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
    border: 1px solid var(--site-border);
    border-radius: 14px;
    background: var(--site-surface-muted);
    box-shadow: 0 4px 14px var(--site-shadow);
  }

  .about-identity {
    margin-top: 16px;
  }

  .about-name {
    margin: 0 0 4px;
    color: var(--site-heading);
    font-size: 1.08rem;
    font-weight: 650;
    line-height: 1.3;
  }

  .about-role {
    margin: 0;
    color: var(--site-muted);
    font-size: 0.9rem;
    line-height: 1.5;
  }

  .about-links {
    display: grid;
    gap: 8px;
    margin-top: 16px;
  }

  .about-links a {
    padding: 7px 11px;
    border: 1px solid var(--site-border-strong);
    border-radius: 999px;
    color: var(--site-accent-strong);
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    transition: background-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
  }

  .about-links a:first-child {
    background: var(--site-accent);
    border-color: var(--site-accent);
    color: var(--site-button-text);
  }

  .about-links a:hover {
    box-shadow: 0 4px 12px var(--site-shadow);
    text-decoration: none;
    transform: translateY(-1px);
  }

  .about-content {
    min-width: 0;
    font-size: 1.01rem;
  }

  .about-intro {
    margin: 0;
    color: var(--site-text);
    font-size: 1.06rem;
    line-height: 1.68;
  }

  .about-section {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid var(--site-border);
  }

  .about-section h2 {
    margin: 0 0 8px;
    color: var(--site-muted-soft);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
  }

  .about-section p {
    margin: 0;
    line-height: 1.68;
  }

  .about-content strong {
    color: var(--site-heading);
    font-weight: 650;
  }

  .about-content a {
    color: var(--site-accent-strong);
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
  }

  @media (max-width: 700px) {
    .about-page {
      margin-top: 8px;
    }

    .about-card {
      grid-template-columns: 140px minmax(0, 1fr);
      gap: 24px;
      padding: 24px;
    }
  }

  @media (max-width: 540px) {
    .about-heading {
      margin-bottom: 16px;
    }

    .about-card {
      grid-template-columns: 1fr;
      gap: 24px;
      padding: 20px;
    }

    .about-profile {
      display: grid;
      grid-template-columns: 104px minmax(0, 1fr);
      gap: 16px;
      align-items: center;
    }

    .about-identity {
      margin: 0;
    }

    .about-links {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      grid-column: 1 / -1;
      margin-top: 0;
    }

    .about-intro {
      font-size: 1rem;
    }
  }
</style>

<div class="about-page">
  <header class="about-heading">
    <h1>All about me</h1>
    <p>Research, education, and the work I care about.</p>
  </header>

  <div class="about-card">
    <aside class="about-profile" aria-label="Profile">
      <img
        class="about-photo"
        src="{{ '/assets/images/my_pfp.jpg' | relative_url }}"
        alt="David Millard"
        width="172"
        height="172">

      <div class="about-identity">
        <p class="about-name">David Millard</p>
        <p class="about-role">Ph.D. student<br>University of Rochester</p>
      </div>

      <div class="about-links">
        <a href="mailto:david.millard@rochester.edu">Email me</a>
        <a href="{{ '/assets/davidmillard_resume.pdf' | relative_url }}">View resume</a>
      </div>
    </aside>

    <div class="about-content">
      <p class="about-intro">
        I'm a Ph.D. student in <strong>Electrical and Computer Engineering</strong> at the University of Rochester. I am a member of the <strong>Human-Centered Computing Lab</strong>, advised by <a href="https://www.hajim.rochester.edu/ece/people/faculty/bocko_mark/index.html">Dr. Mark Bocko</a>. My research spans physical modeling, automatic music transcription, digital watermarking, and text-to-speech systems.
      </p>

      <section class="about-section">
        <h2>Background</h2>
        <p>
          I earned bachelor's degrees in <strong>Computer Science</strong> and <strong>Statistics</strong> at RIT. There, I collaborated with Dr. Arielle Carr at Lehigh University, Stéphane Gaudreault at Environment and Climate Change Canada, and Dr. Ali Baheri in the Safe AI Lab. Before Rochester, I also spent a year in RIT's master's program in <strong>Mechanical Engineering</strong>.
        </p>
      </section>

      <section class="about-section">
        <h2>Beyond research</h2>
        <p>
          Outside of academic work, I enjoy spending time with my animals, Didly and Buck, and staying active. I'm always glad to hear about potential collaborations and interesting problems.
        </p>
      </section>
    </div>
  </div>
</div>
