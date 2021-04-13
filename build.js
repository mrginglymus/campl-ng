/* eslint-env: node */

const pug = require('pug');
const path = require('path');
const fs = require('fs')
const moment = require('moment');

const {pages, frontPage} = require('campl-ng/pages/content')
const links = require('campl-ng/pages/links');
const examples = require('campl-ng/pages/examples');
const themes = require('./themes.json').themes
const siteName = 'CamPL-NG';


examples.articles.populate().then(() => {

    const context = {links, siteName, examples, menu: pages, themes, moment}

    pages.forEach(p => p.updateUrl())

    pages.forEach(p => p.updateBreadcrumbs(pages))

    pages.forEach(p => p.render(context));

    frontPage.render(context);
})

