/* eslint-env: node */

const moment = require('moment');

const imageStyles = require('./images.json').images;
const themes = require('./themes.json').themes;

const {pages, frontPage} = require('campl-ng/pages/content');
const examples = require('campl-ng/pages/examples');
const links = require('campl-ng/pages/links');

const siteName = 'CamPL-NG';



examples.articles.populate().then(() => {

    const context = {
        examples,
        links,
        siteName,
        menu: pages,
        themes,
        moment,
        imageStyles
    };

    pages.forEach(p => p.updateUrl());

    pages.forEach(p => p.updateBreadcrumbs(pages));

    pages.forEach(p => p.render(context));

    frontPage.render(context);
});

