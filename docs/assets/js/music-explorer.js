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
      row.dataset.coverage + '% of this playlist was visible to the public sampler.';
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
    var options = document.querySelectorAll('.listen-page [data-track-option]');
    var link = document.querySelector('[data-oracle-link]');
    if (!options.length || !link) return;
    var option = options[Math.floor(Math.random() * options.length)];
    link.href = option.dataset.trackUrl;
    link.querySelector('[data-oracle-title]').textContent = option.dataset.trackTitle;
    link.querySelector('[data-oracle-meta]').textContent =
      option.dataset.trackArtist + ' · ' + option.dataset.trackNote;
    link.classList.remove('listen-result-pop');
    window.requestAnimationFrame(function () { link.classList.add('listen-result-pop'); });
  }

  document.addEventListener('click', function (event) {
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

    if (event.target.closest('[data-music-shuffle]')) pickTrack();
  });
}());
