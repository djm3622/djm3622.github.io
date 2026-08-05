(function () {
  'use strict';

  var player = document.getElementById('site-player');
  var playerFrame = document.getElementById('spotify-embed');
  var playerStorageKey = 'david-millard-player-open';
  var navigationInProgress = false;

  function setStoredPlayerState(isOpen) {
    try {
      if (isOpen) {
        sessionStorage.setItem(playerStorageKey, 'true');
      } else {
        sessionStorage.removeItem(playerStorageKey);
      }
    } catch (error) {
      // The player remains functional when browser storage is unavailable.
    }
  }

  function openPlayer(shouldFocus) {
    if (!player || !playerFrame) return;
    player.hidden = false;
    if (!playerFrame.getAttribute('src')) {
      playerFrame.setAttribute('src', player.getAttribute('data-embed-src'));
    }
    setStoredPlayerState(true);
    if (shouldFocus !== false) playerFrame.focus();
  }

  function closePlayer() {
    if (!player || !playerFrame) return;
    // Removing the source stops playback immediately instead of hiding audible media.
    playerFrame.removeAttribute('src');
    player.hidden = true;
    setStoredPlayerState(false);
  }

  function restorePlayerState() {
    if (!player) return;
    try {
      if (sessionStorage.getItem(playerStorageKey) === 'true') openPlayer(false);
    } catch (error) {
      // A fresh, closed player is the privacy-preserving fallback.
    }
  }

  function samePageHash(url) {
    return (
      url.pathname === window.location.pathname &&
      url.search === window.location.search &&
      Boolean(url.hash)
    );
  }

  function isNavigablePage(anchor, url) {
    if (
      anchor.hasAttribute('download') ||
      anchor.getAttribute('target') ||
      anchor.hasAttribute('data-full-navigation') ||
      url.origin !== window.location.origin ||
      samePageHash(url)
    ) {
      return false;
    }
    var lastSegment = url.pathname.split('/').pop() || '';
    return !lastSegment.includes('.') || lastSegment.endsWith('.html');
  }

  function updateMetadata(nextDocument) {
    document.title = nextDocument.title;
    var selectors = [
      'link[rel="canonical"]',
      'meta[name="description"]',
      'meta[property^="og:"]',
      'meta[name^="twitter:"]'
    ];
    selectors.forEach(function (selector) {
      var currentElements = document.head.querySelectorAll(selector);
      var nextElements = nextDocument.head.querySelectorAll(selector);
      currentElements.forEach(function (element, index) {
        if (!nextElements[index]) return;
        if (element.tagName === 'LINK') {
          element.setAttribute('href', nextElements[index].getAttribute('href'));
        } else {
          element.setAttribute('content', nextElements[index].getAttribute('content'));
        }
      });
    });
  }

  function updatePageStyles(nextDocument) {
    var pageStyleSelector = 'link[data-page-style], link[href$="/assets/css/plugins.css"]';
    document.head.querySelectorAll(pageStyleSelector).forEach(function (stylesheet) {
      stylesheet.remove();
    });
    nextDocument.head.querySelectorAll(pageStyleSelector).forEach(function (stylesheet) {
      document.head.appendChild(stylesheet.cloneNode(true));
    });
  }

  function activateContentScripts(container) {
    container.querySelectorAll('script').forEach(function (script) {
      var activeScript = document.createElement('script');
      Array.from(script.attributes).forEach(function (attribute) {
        activeScript.setAttribute(attribute.name, attribute.value);
      });
      activeScript.textContent = script.textContent;
      script.replaceWith(activeScript);
    });
  }

  function updateNavigation(url) {
    var links = document.querySelectorAll('.site-nav .page-link');
    var foundExactMatch = false;
    links.forEach(function (link) {
      var linkUrl = new URL(link.href, window.location.href);
      var isActive = linkUrl.pathname === url.pathname;
      foundExactMatch = foundExactMatch || isActive;
      link.classList.toggle('active', isActive);
      if (isActive) {
        link.setAttribute('aria-current', 'page');
      } else {
        link.removeAttribute('aria-current');
      }
    });
    if (!foundExactMatch && links.length > 0) {
      links[0].classList.add('active');
      links[0].setAttribute('aria-current', 'page');
    }
    var navTrigger = document.getElementById('nav-trigger');
    if (navTrigger) navTrigger.checked = false;
  }

  function announceNavigation(main, title) {
    main.setAttribute('tabindex', '-1');
    main.focus({ preventScroll: true });
    main.addEventListener('blur', function removeTemporaryTabIndex() {
      main.removeAttribute('tabindex');
    }, { once: true });
    var announcement = document.getElementById('navigation-announcement');
    if (announcement) announcement.textContent = title + ' loaded';
  }

  function navigate(url, addHistory) {
    if (navigationInProgress) return;
    navigationInProgress = true;
    fetch(url.href, { headers: { 'X-Requested-With': 'site-navigation' } })
      .then(function (response) {
        if (!response.ok) throw new Error('Navigation request failed');
        return response.text();
      })
      .then(function (html) {
        var nextDocument = new DOMParser().parseFromString(html, 'text/html');
        var currentMain = document.querySelector('main.page-content');
        var nextMain = nextDocument.querySelector('main.page-content');
        if (!currentMain || !nextMain) throw new Error('Page content was not found');

        currentMain.innerHTML = nextMain.innerHTML;
        updateMetadata(nextDocument);
        updatePageStyles(nextDocument);
        activateContentScripts(currentMain);
        updateNavigation(url);
        if (addHistory) window.history.pushState({}, '', url.href);
        window.scrollTo(0, 0);
        announceNavigation(currentMain, nextDocument.title);
        window.dispatchEvent(new CustomEvent('site:navigation-complete'));
      })
      .catch(function () {
        window.location.assign(url.href);
      })
      .finally(function () {
        navigationInProgress = false;
      });
  }

  document.addEventListener('click', function (event) {
    var listenButton = event.target.closest('[data-spotify-listen]');
    if (listenButton) {
      event.preventDefault();
      openPlayer(true);
      return;
    }

    var closeButton = event.target.closest('.site-player-close');
    if (closeButton) {
      event.preventDefault();
      closePlayer();
      return;
    }

    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    var anchor = event.target.closest('a[href]');
    if (!anchor) return;
    // Preserve normal multi-page navigation until a listener starts a session.
    if (!player || player.hidden) return;
    var url = new URL(anchor.href, window.location.href);
    if (!isNavigablePage(anchor, url)) return;
    event.preventDefault();
    navigate(url, true);
  });

  window.addEventListener('popstate', function () {
    navigate(new URL(window.location.href), false);
  });

  restorePlayerState();
}());
