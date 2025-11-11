/** @odoo-module */

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.o_structured_menu--content').forEach((parent) => {
    const defaultDelay = 0.1;
    parent.querySelectorAll('.o_structured_menu--item').forEach((item, index) => {
      item.style.animationDelay = `${defaultDelay + (index * 0.04)}s`;
    });
  });

});