(function () {
  'use strict';

  function sortPlaylists(button) {
    var grid = document.querySelector('[data-playlist-grid]');
    if (!grid) return;
    var key = button.getAttribute('data-music-sort');
    var cards = Array.prototype.slice.call(grid.querySelectorAll('.playlist-xray-card'));
    cards.sort(function (left, right) {
      return Number(right.dataset[key]) - Number(left.dataset[key]);
    });
    cards.forEach(function (card) { grid.appendChild(card); });
    document.querySelectorAll('[data-music-sort]').forEach(function (control) {
      control.setAttribute('aria-pressed', control === button ? 'true' : 'false');
    });
    var status = document.getElementById('playlist-sort-status');
    if (status) status.textContent = 'Playlists sorted by ' + button.textContent.trim() + '.';
  }

  function consultOracle() {
    var options = document.querySelectorAll('.music-lab [data-track-option]');
    var link = document.querySelector('[data-oracle-link]');
    if (!options.length || !link) return;
    var option = options[Math.floor(Math.random() * options.length)];
    link.href = option.dataset.trackUrl;
    link.querySelector('[data-oracle-title]').textContent = option.dataset.trackTitle;
    link.querySelector('[data-oracle-meta]').textContent =
      option.dataset.trackArtist + ' · ' + option.dataset.trackNote;
    link.classList.remove('oracle-result-pop');
    window.requestAnimationFrame(function () { link.classList.add('oracle-result-pop'); });
  }

  document.addEventListener('click', function (event) {
    var sortButton = event.target.closest('[data-music-sort]');
    if (sortButton) {
      sortPlaylists(sortButton);
      return;
    }
    if (event.target.closest('[data-music-shuffle]')) consultOracle();
  });
}());
