const {Page, FrontPage} = require('./page')

module.exports = {
    pages: [
        new Page('About', 'about'),
        new Page('Core Elements', null, {
            children: [
                new Page('Typography', 'core_elements/typography', {
                    scss: ['core_elements/_typography.scss', 'core_elements/_blockquote.scss']
                }),
                new Page('Links and Buttons', 'core_elements/links_and_buttons', {
                    scss: ['core_elements/_buttons.scss']
                }),
                new Page('Forms', 'core_elements/forms'),
                new Page('Lists', 'core_elements/lists'),
                new Page('Images', 'core_elements/images'),
                new Page('Embedded Media', 'core_elements/embedded_media'),
                new Page('Themes', 'core_elements/themes'),
            ]
        })
    ],
    frontPage: new FrontPage('Home', 'frontpage')
}