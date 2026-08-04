(function () {
  'use strict';

  var metricConfig = {
    tracks: { label: 'library size', suffix: '', useFullScale: false },
    focus: { label: 'artist focus', suffix: '%', useFullScale: true },
    artists: { label: 'artist variety', suffix: '', useFullScale: false },
    explicit: { label: 'explicit share', suffix: '%', useFullScale: true }
  };

  function updatePlaylistMetric(button) {
    var chart = document.querySelector('[data-playlist-chart]');
    var metric = button.getAttribute('data-playlist-metric');
    var config = metricConfig[metric];
    if (!chart || !config) return;

    var rows = Array.prototype.slice.call(chart.querySelectorAll('[data-playlist-select]'));
    var maximum = config.useFullScale ? 100 : Math.max.apply(null, rows.map(function (row) {
      return Number(row.dataset[metric]);
    }));

    rows.sort(function (left, right) {
      return Number(right.dataset[metric]) - Number(left.dataset[metric]);
    });
    rows.forEach(function (row) {
      var value = Number(row.dataset[metric]);
      row.querySelector('.listen-chart-track span').style.width = (value / maximum * 100) + '%';
      row.querySelector('[data-metric-value]').textContent = value + config.suffix;
      chart.appendChild(row);
    });

    document.querySelectorAll('[data-playlist-metric]').forEach(function (control) {
      control.setAttribute('aria-pressed', control === button ? 'true' : 'false');
    });
    var status = document.querySelector('[data-playlist-status]');
    if (status) status.textContent = 'Playlists are now ranked by ' + config.label + '.';
  }

  function selectPlaylist(row) {
    var detail = document.querySelector('[data-playlist-detail]');
    if (!detail) return;

    document.querySelectorAll('[data-playlist-select]').forEach(function (control) {
      var selected = control === row;
      control.classList.toggle('is-selected', selected);
      control.setAttribute('aria-pressed', selected ? 'true' : 'false');
    });

    detail.querySelector('[data-detail-cover]').src = row.dataset.cover;
    detail.querySelector('[data-detail-name]').textContent = row.dataset.name;
    detail.querySelector('[data-detail-link]').href = row.dataset.url;
    detail.querySelector('[data-detail-link]').setAttribute(
      'aria-label', 'Open ' + row.dataset.name + ' on Spotify'
    );
    detail.querySelector('[data-detail-tracks]').textContent = row.dataset.tracks;
    detail.querySelector('[data-detail-artists]').textContent = row.dataset.artists;
    detail.querySelector('[data-detail-explicit]').textContent = row.dataset.explicit + '%';
    detail.querySelector('[data-detail-duration]').textContent = row.dataset.duration;

    var summary = detail.querySelector('[data-detail-summary]');
    summary.textContent = '';
    var artist = document.createElement('strong');
    artist.textContent = row.dataset.topArtist;
    summary.appendChild(artist);
    summary.appendChild(document.createTextNode(
      ' accounts for ' + row.dataset.focus + '% of the visible tracks.'
    ));
    detail.querySelector('[data-detail-coverage]').textContent =
      row.dataset.coverage + '% of this playlist is represented in the authenticated snapshot.';
  }

  function filterGems(button) {
    var selected = button.getAttribute('data-gem-filter');
    var threshold = selected === 'all' ? Infinity : Number(selected);
    var visible = 0;
    document.querySelectorAll('[data-gem-item]').forEach(function (item) {
      item.hidden = Number(item.dataset.plays) >= threshold;
      if (!item.hidden) visible += 1;
    });
    document.querySelectorAll('[data-gem-filter]').forEach(function (control) {
      control.setAttribute('aria-pressed', control === button ? 'true' : 'false');
    });
    var status = document.querySelector('[data-gem-status]');
    if (status) {
      status.textContent = selected === 'all'
        ? 'Showing all ' + visible + ' overlooked tracks in the sample.'
        : 'Showing ' + visible + ' tracks under ' + Math.round(threshold / 1000) + 'K plays.';
    }
  }

  function pickTrack() {
    var catalog = readMusicCatalog();
    var options = catalog ? catalog.tracks : [];
    var link = document.querySelector('[data-oracle-link]');
    if (!options.length || !link) return;
    var option = options[Math.floor(Math.random() * options.length)];
    link.href = option.url;
    link.querySelector('[data-oracle-title]').textContent = option.title;
    link.querySelector('[data-oracle-meta]').textContent =
      option.artist + ' · ' + option.duration_label + ' · ' + option.playlist;
    link.classList.remove('listen-result-pop');
    window.requestAnimationFrame(function () { link.classList.add('listen-result-pop'); });
  }

  var musicCatalog = null;
  var gravityState = null;
  var gravityFrame = null;

  var gravityMetricConfig = {
    songs: {
      primary: { button: 'Recent plays', label: 'captured personal plays', value: function (item) { return item.recent_play_count || 0; }, format: formatPersonalCount },
      time: { button: 'Duration', label: 'track duration', value: function (item) { return item.duration_ms; }, format: formatDuration },
      odd: { button: 'Title length', label: 'title length', value: function (item) { return item.title.length; }, format: function (value) { return value + ' characters'; } }
    },
    artists: {
      primary: { button: 'Track count', label: 'tracks in the catalog', value: function (item) { return item.tracks; }, format: function (value) { return value + (value === 1 ? ' track' : ' tracks'); } },
      time: { button: 'Catalog time', label: 'catalog time', value: function (item) { return item.duration_ms; }, format: formatCatalogTime },
      odd: { button: 'Explicit share', label: 'explicit-track share', value: function (item) { return item.explicit_pct; }, format: function (value) { return value + '% explicit'; } }
    },
    playlists: {
      primary: { button: 'Library size', label: 'playlist size', value: function (item) { return item.total_tracks; }, format: function (value) { return value + ' tracks'; } },
      time: { button: 'Sampled time', label: 'sampled catalog time', value: function (item) { return item.duration_hours; }, format: function (value) { return value + ' hours'; } },
      odd: { button: 'Artist focus', label: 'top-artist concentration', value: function (item) { return item.top_artist_share_pct; }, format: function (value) { return value + '% one artist'; } }
    }
  };

  function readMusicCatalog() {
    var node = document.querySelector('[data-music-catalog]');
    if (!node) return null;
    if (musicCatalog && node === musicCatalog.node) return musicCatalog.data;
    try {
      musicCatalog = { node: node, data: JSON.parse(node.textContent) };
      return musicCatalog.data;
    } catch (error) {
      return null;
    }
  }

  function formatCount(value) {
    if (!value) return 'public count unavailable';
    if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M plays';
    if (value >= 1000) return (value / 1000).toFixed(1) + 'K plays';
    return value + ' plays';
  }

  function formatPersonalCount(value) {
    return value + (value === 1 ? ' captured play' : ' captured plays');
  }

  function formatDuration(value) {
    var seconds = Math.round(value / 1000);
    return Math.floor(seconds / 60) + ':' + String(seconds % 60).padStart(2, '0');
  }

  function formatCatalogTime(value) {
    var minutes = Math.round(value / 60000);
    var hours = Math.floor(minutes / 60);
    return hours ? hours + 'h ' + String(minutes % 60).padStart(2, '0') + 'm' : minutes + 'm';
  }

  function shuffledSample(items, count) {
    var pool = items.slice();
    for (var index = pool.length - 1; index > 0; index -= 1) {
      var swapIndex = Math.floor(Math.random() * (index + 1));
      var value = pool[index];
      pool[index] = pool[swapIndex];
      pool[swapIndex] = value;
    }
    return pool.slice(0, count);
  }

  function gravityLabel(item, entity) {
    if (entity === 'songs') return item.title;
    return item.name;
  }

  function gravitySecondary(item, entity) {
    if (entity === 'songs') return item.artist + ' · ' + item.playlist;
    if (entity === 'artists') return item.tracks + ' tracks · ' + item.duration_label;
    return item.distinct_primary_artists + ' artists · ' + item.top_artist + ' leads';
  }

  function gravityPool(catalog, entity) {
    if (entity === 'songs') return catalog.tracks;
    return entity === 'artists'
      ? catalog.artists.filter(function (artist) { return artist.image_kind === 'artist'; })
      : catalog.playlists;
  }

  function updateGravityMetricLabels(entity) {
    document.querySelectorAll('[data-gravity-metric]').forEach(function (button) {
      button.textContent = gravityMetricConfig[entity][button.dataset.gravityMetric].button;
    });
  }

  function setGravityDetail(item, entity, metric) {
    var detail = document.querySelector('[data-gravity-detail]');
    if (!detail) return;
    var config = gravityMetricConfig[entity][metric];
    var label = gravityLabel(item, entity);
    var metricValue = config.format(config.value(item));
    var content = document.createElement(item.url ? 'a' : 'div');
    if (item.url) {
      content.href = item.url;
      content.target = '_blank';
      content.rel = 'noopener';
    }
    var title = document.createElement('strong');
    var meta = document.createElement('span');
    title.textContent = label;
    meta.textContent = gravitySecondary(item, entity) + ' · ' + metricValue;
    content.appendChild(title);
    content.appendChild(meta);
    detail.textContent = '';
    detail.appendChild(content);
  }

  function resetGravityDetail(entity) {
    var detail = document.querySelector('[data-gravity-detail]');
    if (!detail) return;
    var label = document.createElement('span');
    var prompt = document.createElement('strong');
    label.textContent = 'Explore ' + entity;
    prompt.textContent = 'Drag, flick, or tap artwork to reveal what is orbiting.';
    detail.textContent = '';
    detail.appendChild(label);
    detail.appendChild(prompt);
  }

  function stopGravity() {
    if (gravityFrame) window.cancelAnimationFrame(gravityFrame);
    gravityFrame = null;
  }

  function drawGravityFrame(timestamp) {
    if (!gravityState || !gravityState.stage.isConnected) {
      stopGravity();
      return;
    }
    if (!gravityState.visible) {
      gravityFrame = null;
      return;
    }
    var elapsed = gravityState.lastTime ? Math.min((timestamp - gravityState.lastTime) / 16.67, 2) : 1;
    gravityState.lastTime = timestamp;
    var width = gravityState.stage.clientWidth;
    var height = gravityState.stage.clientHeight;
    var balls = gravityState.balls;
    var centerX = width / 2;
    var centerY = height / 2;
    var attraction = 0.00016;

    balls.forEach(function (ball) {
      if (ball.dragging) return;
      var ballX = ball.x + ball.radius;
      var ballY = ball.y + ball.radius;
      ball.vx += (centerX - ballX) * attraction * elapsed;
      ball.vy += (centerY - ballY) * attraction * elapsed;
      ball.vx *= 0.9994;
      ball.vy *= 0.9994;
      ball.x += ball.vx * elapsed;
      ball.y += ball.vy * elapsed;
      if (ball.x < 0) { ball.x = 0; ball.vx = Math.abs(ball.vx) * 0.72; }
      if (ball.x + ball.size > width) { ball.x = width - ball.size; ball.vx = -Math.abs(ball.vx) * 0.72; }
      if (ball.y < 0) { ball.y = 0; ball.vy = Math.abs(ball.vy) * 0.72; }
      if (ball.y + ball.size > height) { ball.y = height - ball.size; ball.vy = -Math.abs(ball.vy) * 0.72; }
    });

    for (var leftIndex = 0; leftIndex < balls.length; leftIndex += 1) {
      for (var rightIndex = leftIndex + 1; rightIndex < balls.length; rightIndex += 1) {
        var left = balls[leftIndex];
        var right = balls[rightIndex];
        if (left.dragging || right.dragging) continue;
        var dx = right.x + right.radius - left.x - left.radius;
        var dy = right.y + right.radius - left.y - left.radius;
        var distance = Math.sqrt(dx * dx + dy * dy) || 0.01;
        var minimum = left.radius + right.radius + 2;
        if (distance >= minimum) continue;
        var overlap = (minimum - distance) / 2;
        var nx = dx / distance;
        var ny = dy / distance;
        left.x -= nx * overlap;
        left.y -= ny * overlap;
        right.x += nx * overlap;
        right.y += ny * overlap;
        var relativeVelocity = (right.vx - left.vx) * nx + (right.vy - left.vy) * ny;
        if (relativeVelocity < 0) {
          var impulse = relativeVelocity * 0.72;
          left.vx += impulse * nx;
          left.vy += impulse * ny;
          right.vx -= impulse * nx;
          right.vy -= impulse * ny;
        }
      }
    }

    balls.forEach(function (ball) {
      ball.node.style.transform = 'translate3d(' + ball.x.toFixed(1) + 'px,' + ball.y.toFixed(1) + 'px,0)';
    });
    gravityFrame = window.requestAnimationFrame(drawGravityFrame);
  }

  function selectGravityBall(ball) {
    if (!gravityState) return;
    gravityState.balls.forEach(function (candidate) {
      candidate.node.classList.toggle('is-selected', candidate === ball);
    });
    setGravityDetail(ball.item, gravityState.entity, gravityState.metric);
  }

  function attachGravityInteraction(ball) {
    ball.node.addEventListener('pointerdown', function (event) {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        selectGravityBall(ball);
        return;
      }
      var bounds = gravityState.stage.getBoundingClientRect();
      ball.dragging = true;
      ball.pointerId = event.pointerId;
      ball.pointerOffsetX = event.clientX - bounds.left - ball.x;
      ball.pointerOffsetY = event.clientY - bounds.top - ball.y;
      ball.lastPointerX = event.clientX;
      ball.lastPointerY = event.clientY;
      ball.lastPointerTime = event.timeStamp;
      ball.vx = 0;
      ball.vy = 0;
      ball.node.setPointerCapture(event.pointerId);
      ball.node.classList.add('is-dragging');
      selectGravityBall(ball);
    });

    ball.node.addEventListener('pointermove', function (event) {
      if (!ball.dragging || event.pointerId !== ball.pointerId) return;
      var bounds = gravityState.stage.getBoundingClientRect();
      var nextX = event.clientX - bounds.left - ball.pointerOffsetX;
      var nextY = event.clientY - bounds.top - ball.pointerOffsetY;
      var elapsed = Math.max(8, event.timeStamp - ball.lastPointerTime) / 16.67;
      ball.vx = Math.max(-9, Math.min(9, (event.clientX - ball.lastPointerX) / elapsed));
      ball.vy = Math.max(-9, Math.min(9, (event.clientY - ball.lastPointerY) / elapsed));
      ball.x = Math.max(0, Math.min(bounds.width - ball.size, nextX));
      ball.y = Math.max(0, Math.min(bounds.height - ball.size, nextY));
      ball.lastPointerX = event.clientX;
      ball.lastPointerY = event.clientY;
      ball.lastPointerTime = event.timeStamp;
      ball.node.style.transform = 'translate3d(' + ball.x.toFixed(1) + 'px,' + ball.y.toFixed(1) + 'px,0)';
    });

    function releaseBall(event) {
      if (!ball.dragging || event.pointerId !== ball.pointerId) return;
      ball.dragging = false;
      ball.node.classList.remove('is-dragging');
      if (ball.node.hasPointerCapture(event.pointerId)) {
        ball.node.releasePointerCapture(event.pointerId);
      }
    }

    ball.node.addEventListener('pointerup', releaseBall);
    ball.node.addEventListener('pointercancel', releaseBall);
    ball.node.addEventListener('dragstart', function (event) { event.preventDefault(); });
  }

  function renderGravity(preserveRecords) {
    var catalog = readMusicCatalog();
    var stage = document.querySelector('[data-gravity-stage]');
    if (!catalog || !stage) return;
    stopGravity();
    var entity = gravityState ? gravityState.entity : 'songs';
    var metric = gravityState ? gravityState.metric : 'time';
    var pool = gravityPool(catalog, entity);
    var limit = entity === 'playlists' ? pool.length : Math.min(32, pool.length);
    var records = preserveRecords && gravityState && gravityState.records.length
      ? gravityState.records.slice()
      : (entity === 'playlists' ? pool.slice() : shuffledSample(pool, limit));
    var config = gravityMetricConfig[entity][metric];
    var values = records.map(config.value);
    var minimum = Math.min.apply(null, values);
    var maximum = Math.max.apply(null, values);
    var span = maximum - minimum || 1;
    var width = stage.clientWidth || 760;
    var height = stage.clientHeight || 420;

    stage.textContent = '';
    var core = document.createElement('div');
    core.className = 'listen-gravity-core';
    core.setAttribute('aria-hidden', 'true');
    stage.appendChild(core);
    var balls = records.map(function (item, index) {
      var ratio = Math.sqrt(Math.max(0, (config.value(item) - minimum) / span));
      var size = Math.round(42 + ratio * 56);
      var angle = index / records.length * Math.PI * 2 + (Math.random() - 0.5) * 0.45;
      var orbitRadius = Math.min(width, height) * (0.19 + Math.random() * 0.29);
      var centerX = width / 2;
      var centerY = height / 2;
      var speed = Math.sqrt(0.00016) * orbitRadius * (0.78 + Math.random() * 0.34);
      var node = document.createElement('button');
      node.type = 'button';
      node.className = 'listen-gravity-ball';
      node.dataset.gravityBall = String(index);
      node.style.width = size + 'px';
      node.style.height = size + 'px';
      node.setAttribute('aria-label', gravityLabel(item, entity) + ', ' + config.format(config.value(item)));
      var image = document.createElement('img');
      image.src = item.image_url;
      image.alt = '';
      image.loading = 'lazy';
      image.decoding = 'async';
      image.draggable = false;
      node.appendChild(image);
      stage.appendChild(node);
      var ball = {
        item: item,
        node: node,
        size: size,
        radius: size / 2,
        x: Math.max(0, Math.min(width - size, centerX + Math.cos(angle) * orbitRadius - size / 2)),
        y: Math.max(0, Math.min(height - size, centerY + Math.sin(angle) * orbitRadius - size / 2)),
        vx: -Math.sin(angle) * speed,
        vy: Math.cos(angle) * speed,
        dragging: false
      };
      attachGravityInteraction(ball);
      return ball;
    });

    gravityState = { stage: stage, entity: entity, metric: metric, balls: balls, records: records, visible: true, lastTime: 0 };
    resetGravityDetail(entity);
    var summary = document.querySelector('[data-gravity-summary]');
    if (summary) {
      summary.textContent = (entity === 'playlists' ? 'All ' : limit + '-object orbit from ') + pool.length + ' ' + entity + ' · object size represents ' + config.label + '.';
    }
    updateGravityMetricLabels(entity);
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      stage.classList.add('is-static');
      balls.forEach(function (ball, index) {
        ball.node.style.position = 'relative';
        ball.node.style.transform = 'none';
        ball.node.style.order = String(index);
      });
    } else {
      stage.classList.remove('is-static');
      gravityFrame = window.requestAnimationFrame(drawGravityFrame);
    }
  }

  function initializeGravity() {
    var stage = document.querySelector('[data-gravity-stage]');
    if (!stage || (gravityState && gravityState.stage === stage)) return;
    gravityState = { stage: stage, entity: 'songs', metric: 'time', balls: [], records: [], visible: true, lastTime: 0 };
    renderGravity();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        if (!gravityState || gravityState.stage !== stage) return;
        gravityState.visible = entries[0].isIntersecting;
        if (gravityState.visible && !gravityFrame && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          gravityState.lastTime = 0;
          gravityFrame = window.requestAnimationFrame(drawGravityFrame);
        }
      }, { rootMargin: '120px' }).observe(stage);
    }
  }

  function jumpToSection(link) {
    var targetId = link.getAttribute('href').slice(1);
    var target = document.getElementById(targetId);
    if (!target) return;
    window.history.pushState({}, '', '#' + targetId);
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
    target.scrollIntoView({
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
      block: 'start'
    });
    target.addEventListener('blur', function removeJumpFocus() {
      target.removeAttribute('tabindex');
    }, { once: true });
  }

  document.addEventListener('click', function (event) {
    var sectionLink = event.target.closest('[data-section-jump]');
    if (sectionLink) {
      event.preventDefault();
      jumpToSection(sectionLink);
      return;
    }

    var metricButton = event.target.closest('[data-playlist-metric]');
    if (metricButton) {
      updatePlaylistMetric(metricButton);
      return;
    }

    var playlistRow = event.target.closest('[data-playlist-select]');
    if (playlistRow) {
      selectPlaylist(playlistRow);
      return;
    }

    var gemButton = event.target.closest('[data-gem-filter]');
    if (gemButton) {
      filterGems(gemButton);
      return;
    }

    var gravityEntity = event.target.closest('[data-gravity-entity]');
    if (gravityEntity) {
      initializeGravity();
      gravityState.entity = gravityEntity.dataset.gravityEntity;
      gravityState.metric = 'time';
      document.querySelectorAll('[data-gravity-entity]').forEach(function (button) {
        button.setAttribute('aria-pressed', button === gravityEntity ? 'true' : 'false');
      });
      document.querySelectorAll('[data-gravity-metric]').forEach(function (button) {
        button.setAttribute('aria-pressed', button.dataset.gravityMetric === 'time' ? 'true' : 'false');
      });
      renderGravity();
      return;
    }

    var gravityMetric = event.target.closest('[data-gravity-metric]');
    if (gravityMetric) {
      initializeGravity();
      gravityState.metric = gravityMetric.dataset.gravityMetric;
      document.querySelectorAll('[data-gravity-metric]').forEach(function (button) {
        button.setAttribute('aria-pressed', button === gravityMetric ? 'true' : 'false');
      });
      renderGravity(true);
      return;
    }

    if (event.target.closest('[data-gravity-remix]')) {
      initializeGravity();
      renderGravity();
      return;
    }

    var gravityBall = event.target.closest('[data-gravity-ball]');
    if (gravityBall && gravityState) {
      var ballIndex = Number(gravityBall.dataset.gravityBall);
      document.querySelectorAll('[data-gravity-ball]').forEach(function (button) {
        button.classList.toggle('is-selected', button === gravityBall);
      });
      setGravityDetail(gravityState.records[ballIndex], gravityState.entity, gravityState.metric);
      return;
    }

    if (event.target.closest('[data-music-shuffle]')) pickTrack();
  });

  window.addEventListener('site:navigation-complete', initializeGravity);
  initializeGravity();
}());
