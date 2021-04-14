const {Page, FrontPage} = require('./page')
const {randomImage} = require('./examples')

module.exports = {
    pages: [
        new Page('About', 'about', {
            image: randomImage(590, 310)
        }),
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
        }),
        new Page('In Page Components', null, {
            children: [
                new Page('Navigation', null, {
                    children: [
                        new Page('Tabs', 'components/navigation/tabs', {scss: ['components/navigation/_nav.scss']}),
                        new Page('Pills', 'components/navigation/pills', {scss: ['components/navigation/_nav.scss']}),
                        new Page('Pills (Stacked)', 'components/navigation/pills_stacked', {scss: ['components/navigation/_nav.scss']}),
                        new Page('Stages', 'components/navigation/stages', {scss: ['components/navigation/_nav.scss']}),
                        new Page('Pagination', 'components/navigation/pagination', {scss: ['components/navigation/_pagination.scss']}),
                        new Page('A to Z', 'components/navigation/atoz', {scss: ['components/navigation/_atoz.scss'], hasSideMenu: false}),
                        new Page('Search', 'components/navigation/search', {scss: ['components/navigation/_search.scss']}),
                    ]
                }),
                new Page('Content', null, {
                    children: [
                        new Page('Tables', 'components/content/tables', {scss: ['core_elements/_tables.scss']}),
                        new Page('Collapse', 'components/content/collapse', {scss: ['core_elements/_collapse.scss']}),
                        new Page('Alerts', 'components/content/alerts', {scss: ['core_elements/_alerts.scss']}),
                        new Page('Well', 'components/content/well', {scss: ['core_elements/_well.scss']}),
                        new Page('Date Time Picker', 'components/content/date_time_picker'),
                    ]
                })
            ]
        })
    ],
    frontPage: new FrontPage('Home', 'frontpage')
}