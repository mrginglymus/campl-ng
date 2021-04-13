const {Page, FrontPage} = require('./page')

module.exports = {
    pages: [
        new Page('About', 'about'),
        new Page('Core Elements', null, {
            children: [
                new Page('Typography', 'core_elements/typography', {
                    scss: ['core_elements/_typography.scss', 'core_elements/_blockquote.scss']
                })
            ]
        })
    ],
    frontPage: new FrontPage('Home', 'frontpage')
}