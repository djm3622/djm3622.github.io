---
layout: page
title: Music
permalink: /music/
description: An interactive look at David Millard's Spotify playlists, favorite artists, and overlooked tracks.
---

{%- assign music = site.data.music_analytics -%}
{%- assign playlists_by_size = music.playlists | sort: "total_tracks" | reverse -%}
{%- assign initial_playlist = playlists_by_size[0] -%}
{%- assign max_playlist_tracks = initial_playlist.total_tracks -%}

<div class="listen-page">
  <section class="listen-hero" aria-labelledby="music-heading">
    <div class="listen-hero-copy">
      <p class="listen-kicker">Music · playlist analysis</p>
      <h1 id="music-heading">Listening, mapped.</h1>
      <p>
        An interactive look through the patterns in my Spotify playlists—from intensely
        single-artist collections to tracks with surprisingly small audiences.
      </p>
      <div class="listen-hero-links">
        <a class="listen-button" href="#playlist-explorer" data-section-jump>Explore the playlists</a>
        <a href="#hidden-gems" data-section-jump>Find overlooked tracks</a>
      </div>
    </div>
    <div class="listen-signal" aria-label="Summary of the analyzed music library">
      <div class="listen-signal-main">
        <span>{{ music.overview.unique_tracks }}</span>
        <small>unique tracks sampled</small>
      </div>
      <div class="listen-signal-grid">
        <p><strong>{{ music.methodology.playlist_count }}</strong> public playlists</p>
        <p><strong>{{ music.overview.distinct_primary_artists }}</strong> primary artists</p>
        <p><strong>{{ music.overview.sampled_hours }}h</strong> of music</p>
        <p><strong>{{ music.overview.median_duration_label }}</strong> median track</p>
      </div>
    </div>
  </section>

  <section class="listen-insights" aria-label="Key findings">
    <article>
      <span class="listen-insight-icon" aria-hidden="true">01</span>
      <div><strong>No cross-playlist repeats</strong><p>All {{ music.overview.unique_tracks }} visible tracks have exactly one home.</p></div>
    </article>
    <article>
      <span class="listen-insight-icon" aria-hidden="true">02</span>
      <div><strong>Some playlists are artist studies</strong><p><em>void</em> is 96% Lil Tecca; <em>this u?</em> is 77% Playboi Carti.</p></div>
    </article>
    <article>
      <span class="listen-insight-icon" aria-hidden="true">03</span>
      <div><strong>Wide listening range</strong><p>The sampled catalog runs from 0:58 to 8:06.</p></div>
    </article>
  </section>

  <section class="listen-section" id="playlist-explorer" aria-labelledby="playlist-heading">
    <header class="listen-section-heading">
      <div>
        <p class="listen-kicker">Interactive explorer</p>
        <h2 id="playlist-heading">Compare the playlists</h2>
      </div>
      <p>Change the lens, then select any playlist for its profile.</p>
    </header>

    <div class="listen-metric-tabs" aria-label="Playlist comparison metric">
      <button type="button" data-playlist-metric="tracks" aria-pressed="true">Library size</button>
      <button type="button" data-playlist-metric="focus" aria-pressed="false">Artist focus</button>
      <button type="button" data-playlist-metric="artists" aria-pressed="false">Variety</button>
      <button type="button" data-playlist-metric="explicit" aria-pressed="false">Explicit share</button>
    </div>
    <p class="sr-only" data-playlist-status aria-live="polite"></p>

    <div class="listen-explorer">
      <div class="listen-playlist-chart" data-playlist-chart>
        {%- for playlist in playlists_by_size -%}
          <button
            class="listen-playlist-row{% if forloop.first %} is-selected{% endif %}"
            type="button"
            data-playlist-select
            data-name="{{ playlist.name | escape }}"
            data-url="{{ playlist.url }}"
            data-cover="{{ playlist.image_url }}"
            data-tracks="{{ playlist.total_tracks }}"
            data-focus="{{ playlist.top_artist_share_pct }}"
            data-artists="{{ playlist.distinct_primary_artists }}"
            data-explicit="{{ playlist.explicit_pct }}"
            data-duration="{{ playlist.median_duration_label }}"
            data-top-artist="{{ playlist.top_artist | escape }}"
            data-top-artist-tracks="{{ playlist.top_artist_tracks }}"
            data-coverage="{{ playlist.sample_coverage_pct }}"
            aria-pressed="{% if forloop.first %}true{% else %}false{% endif %}"
          >
            <img src="{{ playlist.image_url }}" alt="" loading="lazy">
            <span class="listen-playlist-name">{{ playlist.name | escape }}</span>
            <span class="listen-chart-track" aria-hidden="true">
              <span style="width: {{ playlist.total_tracks | times: 100.0 | divided_by: max_playlist_tracks }}%"></span>
            </span>
            <strong data-metric-value>{{ playlist.total_tracks }}</strong>
          </button>
        {%- endfor -%}
      </div>

      <aside class="listen-playlist-detail" data-playlist-detail>
        <div class="listen-detail-cover">
          <img src="{{ initial_playlist.image_url }}" alt="" data-detail-cover>
        </div>
        <div class="listen-detail-title">
          <div>
            <span>Selected playlist</span>
            <h3 data-detail-name>{{ initial_playlist.name | escape }}</h3>
          </div>
          <a href="{{ initial_playlist.url }}" target="_blank" rel="noopener" data-detail-link aria-label="Open selected playlist on Spotify">↗</a>
        </div>
        <dl>
          <div><dt>Tracks</dt><dd data-detail-tracks>{{ initial_playlist.total_tracks }}</dd></div>
          <div><dt>Artists</dt><dd data-detail-artists>{{ initial_playlist.distinct_primary_artists }}</dd></div>
          <div><dt>Explicit</dt><dd data-detail-explicit>{{ initial_playlist.explicit_pct }}%</dd></div>
          <div><dt>Median</dt><dd data-detail-duration>{{ initial_playlist.median_duration_label }}</dd></div>
        </dl>
        <p data-detail-summary>
          <strong>{{ initial_playlist.top_artist | escape }}</strong> accounts for
          {{ initial_playlist.top_artist_share_pct }}% of the visible tracks.
        </p>
        <small data-detail-coverage>{{ initial_playlist.sample_coverage_pct }}% of this playlist was visible to the public sampler.</small>
      </aside>
    </div>
  </section>

  <section class="listen-section listen-gems" id="hidden-gems" aria-labelledby="gems-heading">
    <header class="listen-section-heading">
      <div>
        <p class="listen-kicker">Hidden gems</p>
        <h2 id="gems-heading">The quieter corner</h2>
      </div>
      <p>Tracks with the smallest public Spotify play counts in the visible sample.</p>
    </header>

    <div class="listen-gem-controls" aria-label="Filter hidden gems by play count">
      <button type="button" data-gem-filter="100000" aria-pressed="true">Under 100K</button>
      <button type="button" data-gem-filter="175000" aria-pressed="false">Under 175K</button>
      <button type="button" data-gem-filter="all" aria-pressed="false">Show all</button>
    </div>
    <p class="listen-gem-status" data-gem-status aria-live="polite">Showing the least-played tracks under 100K plays.</p>

    <div class="listen-gem-list">
      {%- for track in music.underrated -%}
        <article
          class="listen-gem-row"
          data-gem-item
          data-track-option
          data-plays="{{ track.playcount }}"
          data-track-title="{{ track.title | escape }}"
          data-track-artist="{{ track.artist | escape }}"
          data-track-url="{{ track.url }}"
          data-track-note="{{ track.playcount_label }} Spotify plays"
          {% if track.playcount >= 100000 %}hidden{% endif %}
        >
          <span class="listen-gem-number">{{ forloop.index | prepend: '0' | slice: -2, 2 }}</span>
          <div>
            <strong>{{ track.title | escape }}</strong>
            <span>{{ track.artist | escape }}</span>
          </div>
          <span class="listen-gem-plays">{{ track.playcount_label }} plays</span>
          <span class="listen-gem-time">{{ track.duration_label }}</span>
          <a href="{{ track.url }}" target="_blank" rel="noopener" aria-label="Open {{ track.title | escape }} on Spotify">↗</a>
        </article>
      {%- endfor -%}
    </div>
  </section>

  <section class="listen-discovery" aria-labelledby="discovery-heading">
    <div class="listen-discovery-copy">
      <p class="listen-kicker">Discovery mix</p>
      <h2 id="discovery-heading">Pick something I might defend too enthusiastically.</h2>
      <p>Drawn from the overlooked tracks above.</p>
    </div>
    <div class="listen-picker" aria-live="polite">
      <div>
        <span>Suggested track</span>
        <a href="{{ music.underrated[0].url }}" target="_blank" rel="noopener" data-oracle-link>
          <strong data-oracle-title>{{ music.underrated[0].title | escape }}</strong>
          <small data-oracle-meta>{{ music.underrated[0].artist | escape }} · {{ music.underrated[0].playcount_label }} Spotify plays</small>
        </a>
      </div>
      <button type="button" data-music-shuffle>Pick another <span aria-hidden="true">↻</span></button>
    </div>
  </section>

  <section class="listen-range" aria-labelledby="range-heading">
    <div>
      <p class="listen-kicker">One useful oddity</p>
      <h2 id="range-heading">The duration range</h2>
      <p>The shortest sampled track also has one of the longest titles.</p>
    </div>
    <div class="listen-range-chart">
      <div class="listen-range-line" aria-hidden="true"><span></span></div>
      <div class="listen-range-labels">
        <a href="{{ music.oddities.shortest[0].url }}" target="_blank" rel="noopener">
          <strong>{{ music.oddities.shortest[0].duration_label }}</strong>
          <span>{{ music.oddities.shortest[0].title | escape }}</span>
          <small>{{ music.oddities.shortest[0].artist | escape }}</small>
        </a>
        <a href="{{ music.oddities.longest[0].url }}" target="_blank" rel="noopener">
          <strong>{{ music.oddities.longest[0].duration_label }}</strong>
          <span>{{ music.oddities.longest[0].title | escape }}</span>
          <small>{{ music.oddities.longest[0].artist | escape }}</small>
        </a>
      </div>
    </div>
  </section>

  <details class="listen-method" id="method">
    <summary>About the data and its limitations</summary>
    <div>
      <p>{{ music.methodology.note }}</p>
      <p>
        This snapshot covers {{ music.methodology.sampled_slots }} of {{ music.methodology.catalog_slots }}
        public playlist slots ({{ music.methodology.coverage_pct }}%). Two collaboration playlists were not
        readable from Spotify’s signed-out pages and are excluded. This describes playlist composition,
        not private listening history or skip behavior. Snapshot: {{ music.generated_on | date: "%B %-d, %Y" }}.
      </p>
    </div>
  </details>
</div>
