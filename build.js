/* eslint-env: node */

const pug = require('pug');
const path = require('path');
const fs = require('fs')
const {LoremIpsum} = require('lorem-ipsum')
const moment = require('moment');

const {pages, frontPage} = require('campl-ng/pages/content')
const links = require('campl-ng/pages/links');
const examples = require('campl-ng/pages/examples');
const themes = require('./themes.json').themes
const imageStyles = require('./images.json').images
const siteName = 'CamPL-NG';

const lorem = new LoremIpsum()

function lipsum(paragraphs) {
    return lorem.generateParagraphs(paragraphs);
}

function randomSentence() {
    return lorem.generateSentences(1)
}

examples.articles.populate().then(() => {

    const context = {links, siteName, examples, menu: pages, themes, moment, lipsum, randomSentence, imageStyles}

    pages.forEach(p => p.updateUrl())

    pages.forEach(p => p.updateBreadcrumbs(pages))

    pages.forEach(p => p.render(context));

    frontPage.render(context);
})

