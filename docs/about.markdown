---
layout: page
title: About
permalink: /about/
---

<style>
:root {
  --about-accent: #337ecc;
  --about-dark: #15171a;
  --about-light: #f7f7f7;
}

.about-container {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 36px;
  margin: 28px 0 0 0;
  max-width: 900px;
  padding-bottom: 20px;
}

.about-photo {
  flex: 0 0 160px;
  max-width: 160px;
  min-width: 120px;
  border-radius: 10px;
  box-shadow: 0 2px 10px 0 #0001;
  object-fit: cover;
  border: 1px solid #23272f44;
  background: var(--about-dark);
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
  .about-container { flex-direction: column; gap: 16px; }
  .about-photo { margin: 0 auto; }
  .about-content { padding: 0; max-width: 98vw; }
}
</style>

<div class="about-container">

  <img class="about-photo"
       src="{{ '/assets/images/my_pfp.jpg' | relative_url }}"
       alt="David Millard">

  <div class="about-content">
    <p>
      Hello! I'm <strong>David Millard</strong>, a Ph.D. student in Mechanical and Industrial Engineering at the Rochester Institute of Technology (<strong>RIT</strong>), working in probabilistic machine learning, reinforcement learning, and physics-informed neural networks. I am currently a member of the <strong>Safe AI Lab (SAIL)</strong>, advised by Ali Baheri.
    </p>
    <p>
      I also attended <strong>RIT</strong> for my undergraduate, where I earned a BS <strong>Computer Science</strong> and <strong>Statistics</strong>. During my time in undergraduate I collaborated with various labs: Dr. Arielle Carr at Lehigh University, Stéphane Gaudreault at Environment and Climate Change Canada, and SAIL with Ali Baheri.
    </p>
    <p>
      Outside of academic work, I enjoy spending time with my animals, Didly and Buck, and staying active. For collaborations or inquiries, contact me @ <a href="mailto:djm3622@rit.edu">djm3622@rit.edu</a>.
    </p>
  </div>
</div>

