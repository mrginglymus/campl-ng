/* eslint-env: node */

const moment = require('moment');

const {pages, frontPage} = require('campl-ng/pages/content')
const links = require('campl-ng/pages/links');
const examples = require('campl-ng/pages/examples');
const themes = require('./themes.json').themes
const imageStyles = require('./images.json').images
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
    }

    pages.forEach(p => p.updateUrl())

    pages.forEach(p => p.updateBreadcrumbs(pages))

    pages.forEach(p => p.render(context));

    frontPage.render(context);
})

