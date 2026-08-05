---
layout: page
title: Music
permalink: /music/
description: A playful tour through David Millard's playlists, recent favorites, and listening habits.
---

{%- assign music = site.data.music_analytics -%}
{%- assign playlists_by_size = music.playlists | sort: "total_tracks" | reverse -%}
{%- assign initial_playlist = playlists_by_size[0] -%}
{%- assign max_playlist_tracks = initial_playlist.total_tracks -%}

<div class="listen-page">
  <section class="listen-hero" aria-labelledby="music-heading">
    <div class="listen-hero-copy">
      <p class="listen-kicker">Music · what I have been listening to</p>
      <h1 id="music-heading">Even more about me.</h1>
      <p>
        Music is usually playing somewhere in my day. This is a tour through the playlists,
        artists, and songs I love to hear.
      </p>
      <div class="listen-hero-links">
        <a class="listen-button" href="#playlist-explorer" data-section-jump>Explore the playlists</a>
        <a href="#listening-activity" data-section-jump>See listening activity</a>
        <a href="#hidden-gems" data-section-jump>Find overlooked tracks</a>
      </div>
    </div>
    <div class="listen-signal" aria-label="A quick look at my music collection">
      <div class="listen-signal-main">
        <span>{{ music.overview.unique_tracks }}</span>
        <small>songs across my playlists</small>
      </div>
      <div class="listen-signal-grid">
        <p><strong>{{ music.methodology.playlist_count }}</strong> playlists</p>
        <p><strong>{{ music.overview.distinct_primary_artists }}</strong> artists</p>
        <p><strong>{{ music.overview.sampled_hours }}h</strong> of music</p>
        <p><strong>{{ music.overview.median_duration_label }}</strong> typical song</p>
      </div>
    </div>
  </section>

  <section class="listen-insights" aria-label="Key findings">
    <article>
      <span class="listen-insight-icon" aria-hidden="true">01</span>
      <div><strong>A playlist for every mood</strong><p>Some are built for a single feeling; others wander across artists and eras.</p></div>
    </article>
    <article>
      <span class="listen-insight-icon" aria-hidden="true">02</span>
      <div><strong>Some playlists go deep on one artist</strong><p>{{ playlists_by_size[0].top_artist | escape }} appears more than anyone else in my largest playlist.</p></div>
    </article>
    <article>
      <span class="listen-insight-icon" aria-hidden="true">03</span>
      <div><strong>Quick hits and long listens</strong><p>The songs range from {{ music.oddities.shortest[0].duration_label }} to {{ music.oddities.longest[0].duration_label }}.</p></div>
    </article>
  </section>

  <section class="listen-section listen-activity" id="listening-activity" aria-labelledby="activity-heading">
    <header class="listen-section-heading">
      <div>
        <p class="listen-kicker">Listening lately</p>
        <h2 id="activity-heading">What has been on repeat.</h2>
      </div>
      <p>A glimpse at when I tend to listen and which songs and artists have been filling my headphones.</p>
    </header>

    {%- if music.activity.enabled -%}
      <div class="listen-activity-stats" aria-label="Recent listening at a glance">
        <article><strong>{{ music.activity.captured_plays }}</strong><span>recent plays</span></article>
        <article><strong>{{ music.activity.captured_hours }}h</strong><span>of music</span></article>
        <article><strong>{{ music.activity.distinct_tracks }}</strong><span>different songs</span></article>
        <article><strong>{{ music.activity.distinct_artists }}</strong><span>different artists</span></article>
      </div>

      <div class="listen-activity-grid">
        <article class="listen-hour-card">
          <div class="listen-card-heading">
            <div><span>Time of day</span><h3>A day in music</h3></div>
            <small>Eastern Time</small>
          </div>
          <div class="listen-hour-chart" aria-label="Listening plays by hour of day">
            {%- for hour in music.activity.hour_bins -%}
              <div title="{{ hour.label }}: {{ hour.plays }} plays">
                <span style="height: {{ hour.height_pct }}%"></span>
                {%- assign hour_mod = forloop.index0 | modulo: 6 -%}
                <small>{% if hour_mod == 0 %}{{ hour.label | replace: " ", "" }}{% endif %}</small>
              </div>
            {%- endfor -%}
          </div>
        </article>

        <article class="listen-week-card">
          <div class="listen-card-heading">
            <div><span>Across the week</span><h3>Listening by day</h3></div>
          </div>
          <div class="listen-week-chart">
            {%- for day in music.activity.weekday_bins -%}
              <div>
                <span>{{ day.label }}</span>
                <i aria-hidden="true"><b style="width: {{ day.width_pct }}%"></b></i>
                <strong>{{ day.plays }}</strong>
              </div>
            {%- endfor -%}
          </div>
        </article>
      </div>

      <div class="listen-affinity">
        <article>
          <div class="listen-card-heading">
            <div><span>Last four weeks</span><h3>Top tracks</h3></div>
          </div>
          <ol>
            {%- for track in music.activity.top_tracks.four_weeks limit: 5 -%}
              <li>
                <a href="{{ track.url }}" target="_blank" rel="noopener">
                  <span>{{ track.rank }}</span>
                  <img src="{{ track.image_url }}" alt="" loading="lazy">
                  <div><strong>{{ track.name | escape }}</strong><small>{{ track.artist | escape }}</small></div>
                </a>
              </li>
            {%- endfor -%}
          </ol>
        </article>
        <article>
          <div class="listen-card-heading">
            <div><span>Last four weeks</span><h3>Top artists</h3></div>
          </div>
          <ol>
            {%- for artist in music.activity.top_artists.four_weeks limit: 5 -%}
              <li>
                <a href="{{ artist.url }}" target="_blank" rel="noopener">
                  <span>{{ artist.rank }}</span>
                  <img src="{{ artist.image_url }}" alt="" loading="lazy">
                  <div><strong>{{ artist.name | escape }}</strong><small>one of my recent favorites</small></div>
                </a>
              </li>
            {%- endfor -%}
          </ol>
        </article>
      </div>
      <p class="listen-activity-window">A look at my listening from {{ music.activity.history_start | date: "%B %-d, %Y" }} to {{ music.activity.history_end | date: "%B %-d, %Y" }}.</p>
    {%- else -%}
      <div class="listen-activity-pending">
        <strong>More listening highlights are coming soon.</strong>
        <p>Once there is something worth sharing, this space will fill with recent favorites and listening patterns.</p>
      </div>
    {%- endif -%}
  </section>

  <section class="listen-section" id="playlist-explorer" aria-labelledby="playlist-heading">
    <header class="listen-section-heading">
      <div>
        <p class="listen-kicker">Playlist tour</p>
        <h2 id="playlist-heading">Browse my playlists.</h2>
      </div>
      <p>Choose what you want to compare, then pick a playlist for a closer look.</p>
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
          <div><dt>Typical song</dt><dd data-detail-duration>{{ initial_playlist.median_duration_label }}</dd></div>
        </dl>
        <p data-detail-summary>
          <strong>{{ initial_playlist.top_artist | escape }}</strong> appears more often than any other artist here.
        </p>
      </aside>
    </div>
  </section>

  <section class="listen-section listen-gems" id="hidden-gems" aria-labelledby="gems-heading">
    <header class="listen-section-heading">
      <div>
        <p class="listen-kicker">Hidden gems</p>
        <h2 id="gems-heading">The quieter corner.</h2>
      </div>
      <p>A few lesser-known songs from my playlists, based on their public play counts.</p>
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
          data-plays="{{ track.playcount }}"
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
      <h2 id="discovery-heading">Pick a random song from list.</h2>
      <p>Every pick comes from the {{ music.discovery_tracks.size }} songs gathered here, not just the obvious favorites.</p>
    </div>
    <div class="listen-picker" aria-live="polite">
      <div>
        <span>Suggested track</span>
        <a href="{{ music.discovery_tracks[0].url }}" target="_blank" rel="noopener" data-oracle-link>
          <strong data-oracle-title>{{ music.discovery_tracks[0].title | escape }}</strong>
          <small data-oracle-meta>{{ music.discovery_tracks[0].artist | escape }} · {{ music.discovery_tracks[0].duration_label }} · {{ music.discovery_tracks[0].playlist | escape }}</small>
        </a>
      </div>
      <button type="button" data-music-shuffle>Pick another <span aria-hidden="true">↻</span></button>
    </div>
  </section>

  <section class="listen-section listen-gravity" id="listening-gravity" aria-labelledby="gravity-heading">
    <header class="listen-section-heading">
      <div>
        <p class="listen-kicker">Music in motion</p>
        <h2 id="gravity-heading">Catch an orbit.</h2>
      </div>
      <p>Album artwork drifts around the page. Switch between songs, artists, and playlists, then drag or tap anything that catches your eye.</p>
    </header>

    <div class="listen-gravity-toolbar">
      <div class="listen-gravity-control" aria-label="Gravity subjects">
        <span>Explore</span>
        <div>
          <button type="button" data-gravity-entity="songs" aria-pressed="true">Songs</button>
          <button type="button" data-gravity-entity="artists" aria-pressed="false">Artists</button>
          <button type="button" data-gravity-entity="playlists" aria-pressed="false">Playlists</button>
        </div>
      </div>
      <div class="listen-gravity-control" aria-label="Ball size metric">
        <span>Size by</span>
        <div>
          <button type="button" data-gravity-metric="primary" aria-pressed="false">Recent plays</button>
          <button type="button" data-gravity-metric="time" aria-pressed="true">Duration</button>
          <button type="button" data-gravity-metric="odd" aria-pressed="false">Title length</button>
        </div>
      </div>
      <button class="listen-gravity-remix" type="button" data-gravity-remix>Remix orbit <span aria-hidden="true">↻</span></button>
    </div>

    <p class="listen-gravity-summary" data-gravity-summary aria-live="polite"></p>
    <div class="listen-gravity-stage" data-gravity-stage aria-label="Interactive music artwork"></div>
    <div class="listen-gravity-detail" data-gravity-detail aria-live="polite">
      <span>Choose an object</span>
      <strong>Drag, flick, or tap artwork to reveal what is orbiting.</strong>
    </div>
  </section>

  <section class="listen-range" aria-labelledby="range-heading">
    <div>
      <p class="listen-kicker">One useful oddity</p>
      <h2 id="range-heading">The range of duration.</h2>
      <p>Among the songs here, the shortest one also has one of the longest titles.</p>
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
    <summary>A quick note about these numbers</summary>
    <div>
      <p>
        The songs and totals on this page will change as my playlists do. A song may
        appear in more than one playlist, and public play counts are not available for every track.
        Last updated {{ music.generated_on | date: "%B %-d, %Y" }}.
      </p>
    </div>
  </details>

  <script type="application/json" data-music-catalog>
    {"tracks":{{ music.discovery_tracks | jsonify }},"artists":{{ music.artists | jsonify }},"playlists":{{ music.playlists | jsonify }}}
  </script>
</div>
