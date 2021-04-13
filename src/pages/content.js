const {Page, FrontPage} = require('./page')

module.exports = {
    pages: [
        new Page('About', 'about'),
    ],
    frontPage: new FrontPage('Home', 'frontpage')
}