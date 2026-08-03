---
layout: page
title: Music
permalink: /music/
description: A playful, data-driven field guide to David Millard's Spotify playlists.
---

{%- assign music = site.data.music_analytics -%}

<div class="music-lab">
  <section class="music-hero" aria-labelledby="music-heading">
    <div class="music-hero-copy">
      <p class="music-eyebrow">The listening lab · field report 001</p>
      <h1 id="music-heading">There is a system <br>in the <em>shuffle.</em></h1>
      <p class="music-deck">
        A mildly forensic tour through {{ music.methodology.requested_playlist_count }} playlists:
        part taste profile, part statistical portrait, part investigation into why one 58-second song
        needs a 75-character title.
      </p>
      <div class="music-hero-actions">
        <a class="music-primary-link" href="#underrated">Find the hidden gems <span aria-hidden="true">↓</span></a>
        <a class="music-text-link" href="#method">How this was measured</a>
      </div>
    </div>
    <div class="music-record" aria-label="A typographic record showing the analysis sample">
      <div class="music-record-ring music-record-ring--one"></div>
      <div class="music-record-ring music-record-ring--two"></div>
      <div class="music-record-label">
        <span>{{ music.overview.unique_tracks }}</span>
        <small>unique tracks</small>
      </div>
      <p>PPDUNDER<br>LISTENING<br>ARCHIVE</p>
    </div>
  </section>

  <section class="music-ticker" aria-label="Listening overview">
    <div><strong>{{ music.methodology.playlist_count }}</strong><span>public playlists</span></div>
    <div><strong>{{ music.overview.sampled_hours }}</strong><span>sampled hours</span></div>
    <div><strong>{{ music.overview.distinct_primary_artists }}</strong><span>primary artists</span></div>
    <div><strong>{{ music.overview.explicit_pct }}%</strong><span>explicit tracks</span></div>
    <div><strong>{{ music.overview.median_duration_label }}</strong><span>median track</span></div>
  </section>

  <section class="music-thesis" aria-labelledby="thesis-heading">
    <div>
      <p class="music-section-index">01 / The thesis</p>
      <h2 id="thesis-heading">Your playlists are borders,<br>not suggestions.</h2>
    </div>
    <div class="music-thesis-stat">
      <strong>{{ music.overview.repeat_track_count }}</strong>
      <span>repeated tracks</span>
    </div>
    <p class="music-thesis-copy">
      Across {{ music.overview.unique_tracks }} visible tracks, not one appears in two playlists.
      That is unusually tidy genre filing: when a track gets a home, it stays there. “Shuffle” may
      be chaotic; the archive absolutely is not.
    </p>
  </section>

  <section class="music-section artist-gravity" aria-labelledby="gravity-heading">
    <header class="music-section-heading">
      <div>
        <p class="music-section-index">02 / Artist gravity</p>
        <h2 id="gravity-heading">Who bends the library<br>around themselves?</h2>
      </div>
      <p>Track appearances in the visible playlist windows. Collaborations are credited to the primary artist.</p>
    </header>

    <div class="artist-gravity-layout">
      <ol class="artist-bars">
        {%- assign max_artist_tracks = music.top_artists[0].tracks -%}
        {%- for artist in music.top_artists limit: 10 -%}
          <li>
            <span class="artist-rank">{{ forloop.index | prepend: '0' | slice: -2, 2 }}</span>
            <span class="artist-name">{{ artist.name | escape }}</span>
            <span class="artist-bar-track" aria-hidden="true">
              <span style="--artist-width: {{ artist.tracks | times: 100.0 | divided_by: max_artist_tracks }}%"></span>
            </span>
            <strong>{{ artist.tracks }}</strong>
          </li>
        {%- endfor -%}
      </ol>
      <aside class="music-margin-note">
        <span>Observed phenomenon</span>
        <strong>The artist monograph</strong>
        <p><b>yeatpilled</b> is 74/97 Yeat. <b>this u?</b> is 54/70 Playboi Carti. <b>void</b> is 27/28 Lil Tecca. These are playlists in the same way a dissertation is “some notes.”</p>
      </aside>
    </div>
  </section>

  <section class="music-section playlist-atlas" aria-labelledby="atlas-heading">
    <header class="music-section-heading">
      <div>
        <p class="music-section-index">03 / Playlist atlas</p>
        <h2 id="atlas-heading">Eleven little sonic countries.</h2>
      </div>
      <div class="playlist-sort" aria-label="Sort playlist cards">
        <span>Sort by</span>
        <button type="button" data-music-sort="tracks" aria-pressed="true">size</button>
        <button type="button" data-music-sort="explicit">spice</button>
        <button type="button" data-music-sort="artists">variety</button>
        <button type="button" data-music-sort="duration">length</button>
      </div>
    </header>
    <p class="sr-only" id="playlist-sort-status" aria-live="polite"></p>

    <div class="playlist-xray-grid" data-playlist-grid>
      {%- for playlist in music.playlists -%}
        <article
          class="playlist-xray-card"
          data-tracks="{{ playlist.total_tracks }}"
          data-explicit="{{ playlist.explicit_pct }}"
          data-artists="{{ playlist.distinct_primary_artists }}"
          data-duration="{{ playlist.median_duration_ms }}"
        >
          <a class="playlist-cover" href="{{ playlist.url }}" target="_blank" rel="noopener" aria-label="Open {{ playlist.name | escape }} on Spotify">
            <img src="{{ playlist.image_url }}" alt="" loading="lazy">
            <span aria-hidden="true">↗</span>
          </a>
          <div class="playlist-card-heading">
            <h3>{{ playlist.name | escape }}</h3>
            <span>{{ playlist.sample_coverage_pct }}% scanned</span>
          </div>
          <dl>
            <div><dt>tracks</dt><dd>{{ playlist.total_tracks }}</dd></div>
            <div><dt>explicit</dt><dd>{{ playlist.explicit_pct }}%</dd></div>
            <div><dt>median</dt><dd>{{ playlist.median_duration_label }}</dd></div>
          </dl>
          <p><span>center of gravity</span>{{ playlist.top_artist | escape }} · {{ playlist.top_artist_tracks }} tracks</p>
        </article>
      {%- endfor -%}
    </div>
  </section>

  <section class="music-section underrated-section" id="underrated" aria-labelledby="underrated-heading">
    <header class="music-section-heading music-section-heading--light">
      <div>
        <p class="music-section-index">04 / The underrated department</p>
        <h2 id="underrated-heading">Good songs,<br>quiet numbers.</h2>
      </div>
      <p>Lowest global Spotify play counts among the {{ music.methodology.playcount_sample }} tracks whose public pages exposed that metric. “Underrated” here means less-traveled—not objectively better, which would require a much more dangerous model.</p>
    </header>

    <ol class="underrated-list">
      {%- for track in music.underrated limit: 8 -%}
        <li data-track-option data-track-title="{{ track.title | escape }}" data-track-artist="{{ track.artist | escape }}" data-track-url="{{ track.url }}" data-track-note="{{ track.playcount_label }} Spotify plays">
          <span class="underrated-rank">{{ forloop.index | prepend: '0' | slice: -2, 2 }}</span>
          <a href="{{ track.url }}" target="_blank" rel="noopener">
            <strong>{{ track.title | escape }}</strong>
            <span>{{ track.artist | escape }}</span>
          </a>
          <span class="underrated-plays"><b>{{ track.playcount_label }}</b> plays</span>
          <span class="underrated-duration">{{ track.duration_label }}</span>
        </li>
      {%- endfor -%}
    </ol>
  </section>

  <section class="music-section oddities-section" aria-labelledby="oddities-heading">
    <header class="music-section-heading">
      <div>
        <p class="music-section-index">05 / Statistical oddities</p>
        <h2 id="oddities-heading">The fun part of the spreadsheet.</h2>
      </div>
    </header>

    <div class="oddity-grid">
      <article class="oddity-card oddity-card--hero" data-track-option data-track-title="{{ music.oddities.shortest[0].title | escape }}" data-track-artist="{{ music.oddities.shortest[0].artist | escape }}" data-track-url="{{ music.oddities.shortest[0].url }}" data-track-note="Shortest sampled track · {{ music.oddities.shortest[0].duration_label }}">
        <p>Shortest song / longest explanation</p>
        <strong>{{ music.oddities.shortest[0].duration_label }}</strong>
        <h3>“{{ music.oddities.shortest[0].title | escape }}”</h3>
        <span>{{ music.oddities.shortest[0].artist | escape }} fit {{ music.oddities.longest_titles[1].characters }} title characters into less than a minute. The title occupies roughly 1.3 characters per second.</span>
        <a href="{{ music.oddities.shortest[0].url }}" target="_blank" rel="noopener">Inspect the evidence ↗</a>
      </article>

      <article class="oddity-card">
        <p>Parental advisory index</p>
        <strong>{{ music.overview.explicit_pct }}%</strong>
        <h3>Less a warning,<br>more a house style.</h3>
        <span>Three visible playlists are effectively 100% explicit: <b>void</b>, <b>he on something</b>, and <b>this u?</b>.</span>
      </article>

      <article class="oddity-card">
        <p>Title typography desk</p>
        <strong>{{ music.overview.punctuation_title_pct }}%</strong>
        <h3>Contain ?, !, (), or [].</h3>
        <span>Another {{ music.overview.lowercase_title_pct }}% are strictly lowercase alphabetic titles. The shift key is apparently an aesthetic decision.</span>
      </article>

      <article class="oddity-card oddity-card--wide" data-track-option data-track-title="{{ music.oddities.longest[0].title | escape }}" data-track-artist="{{ music.oddities.longest[0].artist | escape }}" data-track-url="{{ music.oddities.longest[0].url }}" data-track-note="Longest sampled track · {{ music.oddities.longest[0].duration_label }}">
        <div>
          <p>Duration whiplash</p>
          <h3>The library can move from a 58-second digital seizure to eight minutes of Justin Timberlake.</h3>
        </div>
        <div class="duration-duel" aria-label="Shortest and longest sampled tracks">
          <span style="--duration-width: 12%"><b>{{ music.oddities.shortest[0].duration_label }}</b> {{ music.oddities.shortest[0].artist | escape }}</span>
          <span style="--duration-width: 100%"><b>{{ music.oddities.longest[0].duration_label }}</b> {{ music.oddities.longest[0].title | escape }}</span>
        </div>
      </article>
    </div>
  </section>

  <section class="shuffle-oracle" aria-labelledby="oracle-heading">
    <div>
      <p class="music-section-index">06 / The shuffle oracle</p>
      <h2 id="oracle-heading">Let the dataset pick.</h2>
      <p>A tiny recommendation machine drawing from the underrated and statistically peculiar corners above.</p>
    </div>
    <div class="oracle-machine">
      <button type="button" data-music-shuffle>Consult the oracle <span aria-hidden="true">↻</span></button>
      <div class="oracle-result" aria-live="polite">
        <span>Your next track</span>
        <a href="{{ music.underrated[0].url }}" target="_blank" rel="noopener" data-oracle-link>
          <strong data-oracle-title>{{ music.underrated[0].title | escape }}</strong>
          <small data-oracle-meta>{{ music.underrated[0].artist | escape }} · {{ music.underrated[0].playcount_label }} Spotify plays</small>
        </a>
      </div>
    </div>
  </section>

  <section class="music-method" id="method" aria-labelledby="method-heading">
    <p class="music-section-index">07 / Method, caveats & receipts</p>
    <div>
      <h2 id="method-heading">No fake precision.</h2>
      <p>{{ music.methodology.note }}</p>
      <p>This snapshot covers {{ music.methodology.sampled_slots }} of {{ music.methodology.catalog_slots }} public playlist slots ({{ music.methodology.coverage_pct }}%). Two supplied collaboration playlists could not be read from Spotify’s signed-out public pages and are excluded. Counts are a snapshot from {{ music.generated_on | date: "%B %-d, %Y" }} and will drift as playlists and global play totals change.</p>
    </div>
    <div class="method-receipt">
      <span>Source</span>
      <strong>Spotify public playlist + embed pages</strong>
      <span>Unit of analysis</span>
      <strong>Visible playlist slots, deduplicated by track ID where noted</strong>
      <span>Not included</span>
      <strong>Private listening history, skip rate, audio features, or inferred mood</strong>
    </div>
  </section>
</div>
