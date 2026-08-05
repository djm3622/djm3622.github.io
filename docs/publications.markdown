---
layout: page
title: Research
seo_title: Publications
permalink: /publications/
description: Research publications by David Millard in machine learning, scientific computing, control, reinforcement learning, and related areas.
---

<style>
  .research-section-title {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 34px 0 18px;
    color: var(--site-heading);
    font-size: 1.3rem;
    letter-spacing: -0.01em;
  }

  .research-section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--site-border);
  }

  .pub-entry-flex {
    display: flex;
    align-items: center;
    gap: 22px;
    margin-bottom: 14px;
    padding: 18px;
    background: var(--site-surface);
    border: 1px solid var(--site-border);
    border-radius: 14px;
    box-shadow: 0 3px 14px var(--site-shadow);
    transition: border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
  }

  .pub-entry-flex:hover {
    border-color: var(--site-border-strong);
    box-shadow: 0 8px 22px var(--site-shadow);
    transform: translateY(-2px);
  }

  .pub-image {
    display: block;
    flex: 0 0 152px;
    width: 152px;
    height: 118px;
    box-sizing: border-box;
    image-rendering: auto;
    object-fit: contain;
    object-position: center;
    padding: 8px;
    background: var(--site-surface-soft);
    border: 1px solid var(--site-border);
    border-radius: 12px;
    box-shadow: 0 3px 12px var(--site-shadow);
    transition: border-color 160ms ease, box-shadow 160ms ease, transform 200ms ease;
  }

  .pub-entry-flex:hover .pub-image {
    border-color: var(--site-border-strong);
    box-shadow: 0 5px 16px var(--site-shadow);
    transform: scale(1.015);
  }

  .pub-details {
    flex: 1;
    min-width: 0;
  }

  .pub-details strong {
    color: var(--site-accent);
    font-weight: 650;
  }

  .pub-title {
    margin: 0 0 7px;
    color: var(--site-muted);
    font-size: 0.9rem;
  }

  .pub-meta {
    margin-bottom: 0;
    color: var(--site-muted);
    font-size: 0.92rem;
    line-height: 1.55;
  }

  .pub-meta em {
    display: block;
    margin-bottom: 2px;
    color: var(--site-heading);
    font-size: 1.05rem;
    font-style: normal;
    font-weight: 650;
    line-height: 1.4;
  }

  .pub-links {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
  }

  .pub-links a {
    padding: 5px 10px;
    background: var(--site-surface-soft);
    border: 1px solid var(--site-border-strong);
    border-radius: 999px;
    color: var(--site-accent-strong);
    font-size: 0.82rem;
    font-weight: 600;
    text-decoration: none;
  }

  .pub-links a:hover {
    background: var(--site-accent-soft);
    border-color: var(--site-accent);
  }

  @media (max-width: 650px) {
    .research-section-title {
      margin-top: 26px;
    }

    .pub-entry-flex {
      flex-direction: column;
      align-items: stretch;
      gap: 16px;
      padding: 15px;
    }

    .pub-image {
      flex-basis: auto;
      width: 100%;
      height: clamp(170px, 46vw, 220px);
      max-height: none;
      padding: 10px;
    }
  }
</style>

<h2 class="research-section-title">Publications &amp; Proceedings</h2>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/policy_3_flat.png' | relative_url }}" alt="Local, mean, and barycenter policies" />
  <div class="pub-details">
    <div class="pub-title">
      <strong>David Millard</strong>, Ali Baheri
    </div>
    <div class="pub-meta">
      <em>Can Optimal Transport Improve Federated Inverse Reinforcement Learning?</em><br>
      Proceedings of the 8th Annual Learning for Dynamics and Control Conference, PMLR 331:1939&ndash;1953, 2026.
    </div>
    <div class="pub-links">
      <a href="https://proceedings.mlr.press/v331/millard26a.html" target="_blank">Proceedings</a>
      <a href="https://arxiv.org/abs/2601.00309" target="_blank">arXiv</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/trajectory_instance_0.gif' | relative_url }}" alt="Split conformal prediction in function space" />
  <div class="pub-details">
    <div class="pub-title">
      <strong>David Millard</strong>, Lars Lindemann, Ali Baheri
    </div>
    <div class="pub-meta">
      <em>Split Conformal Prediction in the Function Space via Neural Operator Learning</em><br>
      ICLR 2026 Workshop on AI and Partial Differential Equations.
    </div>
    <div class="pub-links">
      <a href="https://openreview.net/forum?id=0twOHJg60V" target="_blank">OpenReview</a>
      <a href="https://arxiv.org/abs/2509.04623" target="_blank">arXiv</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/pearl2025.png' | relative_url }}" alt="PEARL: Preconditioner Enhancement" />
  <div class="pub-details">
    <div class="pub-title">
      <strong>David Millard</strong>, Arielle Carr, Stéphane Gaudreault, Ali Baheri
    </div>
    <div class="pub-meta">
      <em>PEARL: Preconditioner Enhancement through Actor-critic Reinforcement Learning</em><br>
      2026 Joint Mathematics Meetings, SIAM Minisymposium on Recent Advances in Numerical Linear Algebra.
    </div>
    <div class="pub-links">
      <a href="https://meetings.ams.org/math/jmm2026/meetingapp.cgi/Paper/57268" target="_blank">Conference</a>
      <a href="https://arxiv.org/abs/2501.10750" target="_blank">arXiv</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/ams2025.png' | relative_url }}" alt="Deep Ritz" />
  <div class="pub-details">
    <div class="pub-title">
      Anton Selitskiy, <strong>David Millard</strong>
    </div>
    <div class="pub-meta">
      <em>Deep Ritz Method for Elliptic Differential-Difference Equations</em><br>
      Proceedings of the AMS Spring Eastern Sectional Meeting, 2025.
    </div>
    <div class="pub-links">
      <a href="https://meetings.ams.org/math/spring2025e/meetingapp.cgi/Paper/47716" target="_blank">Conference</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/bigdata2024-1.gif' | relative_url }}" alt="Koopman Operator" />
  <div class="pub-details">
    <div class="pub-title">
      <strong>David Millard</strong>, Arielle Carr, Stéphane Gaudreault
    </div>
    <div class="pub-meta">
      <em>Deep Learning for Koopman Operator Estimation in Idealized Atmospheric Dynamics</em><br>
      Proceedings of the 2024 IEEE International Conference on Big Data.
    </div>
    <div class="pub-links">
      <a href="https://arxiv.org/abs/2409.06522" target="_blank">arXiv</a>
      <a href="https://www.computer.org/csdl/proceedings-article/bigdata/2024/10825166/23ykzuKFTaw" target="_blank">IEEE Xplore</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/bigdata2024-2.gif' | relative_url }}" alt="Initial Guess Selection" />
  <div class="pub-details">
    <div class="pub-title">
      <strong>David Millard</strong>, Arielle Carr, Stéphane Gaudreault
    </div>
    <div class="pub-meta">
      <em>Data-Driven Initial Guess Selection for Numerical Weather Prediction Solvers</em><br>
      Proceedings of the 2024 IEEE International Conference on Big Data.
    </div>
    <div class="pub-links">
      <a href="https://www.computer.org/csdl/proceedings-article/bigdata/2024/10825862/23yl9opa000" target="_blank">IEEE Xplore</a>
    </div>
  </div>
</div>


<h2 class="research-section-title">Articles</h2>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/val_target_potential_centered_mse_vs_ratio.png' | relative_url }}" alt="Validation potential error across learning-rate ratios" />
  <div class="pub-details">
    <div class="pub-title">
      Anton Selitskiy, <strong>David Millard</strong>
    </div>
    <div class="pub-meta">
      <em>Stability of the Monge Map in Semi-Dual Optimal Transport</em><br>
      Preprint.
    </div>
    <div class="pub-links">
      <a href="https://arxiv.org/abs/2605.05569" target="_blank">arXiv</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/fig_cnn_vs_adv.png' | relative_url }}" alt="Comparison of CNN and neural semi-Lagrangian weather advection" />
  <div class="pub-details">
    <div class="pub-title">
      Carlos A. Pereira, St&eacute;phane Gaudreault, Valentin Dallerit, Christopher Subich, Shoyon Panday, Siqi Wei, Sasa Zhang, Siddharth Rout, Eldad Haber, Raymond J. Spiteri, <strong>David Millard</strong>, Emilia Diaconescu
    </div>
    <div class="pub-meta">
      <em>Learning to Advect: A Neural Semi-Lagrangian Architecture for Weather Forecasting</em><br>
      Preprint.
    </div>
    <div class="pub-links">
      <a href="https://arxiv.org/abs/2601.21151" target="_blank">arXiv</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/panel3_risk_barycenter.png' | relative_url }}" alt="FedAvg and risk-weighted barycenter distributions" />
  <div class="pub-details">
    <div class="pub-title">
      <strong>David Millard</strong>, Cecilia Alm, Rashid Ali, Pengcheng Shi, Ali Baheri
    </div>
    <div class="pub-meta">
      <em>Federated Distributional Reinforcement Learning with Distributional Critic Regularization</em><br>
      Preprint.
    </div>
    <div class="pub-links">
      <a href="https://arxiv.org/abs/2603.17820" target="_blank">arXiv</a>
    </div>
  </div>
</div>

<div class="pub-entry-flex">
  <img class="pub-image" src="{{ '/assets/images/Specific Humidity H600_Ensemble_Spread.gif' | relative_url }}" alt="DEF: Diffusion-augmented" />
  <div class="pub-details">
    <div class="pub-title">
      <strong>David Millard</strong>, Arielle Carr, Stéphane Gaudreault, Ali Baheri
    </div>
    <div class="pub-meta">
      <em>DEF: Diffusion-augmented Ensemble Forecasting</em><br>
      Preprint.
    </div>
    <div class="pub-links">
      <a href="https://arxiv.org/abs/2506.07324" target="_blank">arXiv</a>
    </div>
  </div>
</div>
