// Keep the desktop navigation visible while starting the mobile menu closed.
const atlasMenu = document.querySelector('.atlas-menu');
if (atlasMenu) {
  const desktopMenu = window.matchMedia('(min-width: 851px)');
  const setMenu = () => { atlasMenu.open = desktopMenu.matches; };
  setMenu();
  desktopMenu.addEventListener('change', setMenu);
}
