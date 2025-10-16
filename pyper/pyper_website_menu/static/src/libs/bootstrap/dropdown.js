/**
 * Add background color on navbar element when overlay header is enabled and structured menu is in the page.
 */
const structuredMenus = document.querySelectorAll(
    '.o_header_overlay .navbar.o_colored_level .o_structured_menu'
);
structuredMenus.forEach((structuredMenu) => {
    const dropdownItem = structuredMenu.previousElementSibling

    if (dropdownItem) {
        const navbar = dropdownItem.closest('.navbar.o_colored_level');

        if (navbar) {
            dropdownItem.addEventListener('show.bs.dropdown', () => {
                navbar.classList.add('o_structured_menu--navbar');
            });
            dropdownItem.addEventListener('hide.bs.dropdown', () => {
                navbar.classList.remove('o_structured_menu--navbar');
            });
        }
    }
});
