import { describe, it, expect, beforeEach } from 'vitest';
import { openNav, closeNav } from '../static/sidebar.js';

describe('sidebar navigation', () => {

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="mySidenav"></div>
        `;
    });

    it('opens the sidebar', () => {

        openNav();

        const sidenav =
            document.getElementById('mySidenav');

        expect(sidenav.classList.contains('open'))
            .toBe(true);
    });

    it('closes the sidebar', () => {

        openNav();
        closeNav();

        const sidenav =
            document.getElementById('mySidenav');

        expect(sidenav.classList.contains('open'))
            .toBe(false);
    });
});