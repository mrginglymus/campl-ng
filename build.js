/* eslint-env: node */

const pug = require('pug');
const path = require('path');
const fs = require('fs')

const content = require('campl-ng/pages/content')

content.forEach(page => {
    const template = pug.compileFile(path.join('src', 'pages', `${page.source}.pug`));
    const content = template({page});
    fs.writeFileSync(path.join('build', page.destination), content);
})
