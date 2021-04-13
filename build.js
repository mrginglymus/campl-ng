/* eslint-env: node */

const pug = require('pug');
const path = require('path');
const fs = require('fs')

const {pages, frontPage} = require('campl-ng/pages/content')
const links = require('campl-ng/pages/links');
const examples = require('campl-ng/pages/examples');
const themes = require('./themes.json').themes
const siteName = 'CamPL-NG';

function renderPage(page) {
    const template = pug.compileFile(path.join('src', 'pages', `${page.source}.pug`));
    const rendered = template({page, links, siteName, examples, menu: pages, themes});
    fs.writeFileSync(path.join('build', page.destination), rendered);
}

pages.forEach(renderPage);

renderPage(frontPage);

