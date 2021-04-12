/* eslint-env: node */

const pug = require('pug');
const path = require('path');
const fs = require('fs')

const content = require('campl-ng/pages/content')
const links = require('campl-ng/pages/links');
const examples = require('campl-ng/pages/examples');
const siteName = 'CamPL-NG'

content.forEach(page => {
    const template = pug.compileFile(path.join('src', 'pages', `${page.source}.pug`));
    const content = template({page, links, siteName, examples});
    fs.writeFileSync(path.join('build', page.destination), content);
})
