---
layout: page
title: About
permalink: /about/
description: Background, education, research interests, and contact information for David Millard, a Ph.D. student at the University of Rochester.
---

<style>
:root {
  --about-accent: var(--site-accent);
}

.about-container {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 36px;
  margin: 28px 0 0 0;
  max-width: 900px;
  padding: 28px;
  background: linear-gradient(145deg, var(--site-surface-soft) 0%, var(--site-surface) 62%);
  border: 1px solid var(--site-border);
  border-radius: 16px;
  box-shadow: 0 8px 26px var(--site-shadow);
}

.about-photo {
  flex: 0 0 160px;
  max-width: 160px;
  min-width: 120px;
  border-radius: 10px;
  box-shadow: 0 2px 10px var(--site-shadow);
  object-fit: cover;
  border: 1px solid var(--site-border);
  background: var(--site-surface-muted);
}

.about-content {
  flex: 1 1 370px;
  min-width: 220px;
  max-width: 640px;
  font-size: 1.07em;
  color: inherit;
  margin-top: 0;
  line-height: 1.62;
  letter-spacing: 0.01em;
}

.about-content strong {
  color: var(--about-accent);
  font-weight: 600;
  letter-spacing: 0.02em;
}
.about-content a {
  color: var(--about-accent);
  text-decoration: none;
  border-bottom: 1px dotted var(--about-accent);
}
.about-content a:hover { text-decoration: underline; }
@media (max-width: 700px) {
  .about-container { flex-direction: column; gap: 18px; margin-top: 10px; padding: 20px 16px; }
  .about-photo { margin: 0 auto; }
  .about-content { padding: 0; max-width: 100%; font-size: 1rem; }
}
</style>

<div class="about-container">

  <img class="about-photo"
       src="{{ '/assets/images/my_pfp.jpg' | relative_url }}"
       alt="David Millard">

  <div class="about-content">
    <p>
      Hello! I'm <strong>David Millard</strong>, a Ph.D. student in Electrical and Computer Engineering at the University of Rochester. I am a member of the <strong>Human-Centered Computing Lab</strong>, advised by <a href="https://www.hajim.rochester.edu/ece/people/faculty/bocko_mark/index.html">Dr. Mark Bocko</a>. My research interests include physical modeling, automatic music transcription, digital watermarking, and text-to-speech systems.
    </p>
    <p>
      I attended <strong>RIT</strong> as an undergraduate, where I earned a BS in <strong>Computer Science</strong> and <strong>Statistics</strong>. During that time, I collaborated with Dr. Arielle Carr at Lehigh University, Stéphane Gaudreault at Environment and Climate Change Canada, and Dr. Ali Baheri in the Safe AI Lab. Before joining the University of Rochester, I spent one year as a master's student in <strong>Mechanical Engineering</strong> at <strong>RIT</strong>.
    </p>
    <p>
      Outside of academic work, I enjoy spending time with my animals, Didly and Buck, and staying active. For collaborations or inquiries, contact me at <a href="mailto:david.millard@rochester.edu">david.millard@rochester.edu</a>.
    </p>
  </div>
</div>
