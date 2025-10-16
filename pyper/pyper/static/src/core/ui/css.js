/** @odoo-module **/

/*global CSSMatrix*/
/*global WebKitCSSMatrix*/
/*global MSCSSMatrix*/

/**
 * Get the horizontal position of target element.
 *
 * @param {HTMLElement} el         The element
 * @param {Boolean}     [computed] Check if computed values must be used
 *
 * @return {{e: number, f: number}}
 */
export function getTransform(el, computed) {
    let transformCss = computed ? window.getComputedStyle(el).getPropertyValue('transform') : el.style.transform,
        transform = {e: 0, f: 0},
        reMatrix,
        match;

    if (transformCss) {
        if ('function' === typeof CSSMatrix) {
            transform = new CSSMatrix(transformCss);

        } else if ('function' === typeof WebKitCSSMatrix) {
            transform = new WebKitCSSMatrix(transformCss);

        } else if ('function' === typeof MSCSSMatrix) {
            transform = new MSCSSMatrix(transformCss);

        } else {
            reMatrix = /matrix\(\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)/;
            match = transformCss.match(reMatrix);

            if (match) {
                transform.e = parseInt(match[1], 10);
                transform.f = parseInt(match[2], 10);
            }
        }
    }

    return transform;
}

/**
 * @param {Object} style
 *
 * @returns {string}
 */
export function stylesToString(style) {
    return Object.entries(style).map(([k, v]) => `${k}:${v}`).join(';');
}
