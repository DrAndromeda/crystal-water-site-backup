/* Click-to-load YouTube: no third-party requests/cookies until the user clicks. Works without JS as a plain link. */
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[data-yt]');
  if (!a) return;
  e.preventDefault();
  var f = document.createElement('iframe');
  f.src = 'https://www.youtube-nocookie.com/embed/' + a.getAttribute('data-yt') + '?autoplay=1&rel=0';
  f.title = a.getAttribute('data-title') || 'YouTube';
  f.allow = 'autoplay; encrypted-media; picture-in-picture';
  f.allowFullscreen = true;
  a.parentNode.replaceChild(f, a);
});
