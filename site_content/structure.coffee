Page = require './page.coffee'
Pages = require './pages.coffee'


pages = new Pages(
  new Page('About', 'pages/about.jade'),
  new Page('Page Layouts', null, [
    new Page('Subsection with navigation', 'layouts/page.jade'),
    new Page('Subsection without navigation', 'layouts/page.jade', [], {side_menu:false}),
    new Page('Subsection without right column', 'layouts/page.jade'),
    new Page('App', 'layouts/page.jade', [], {side_menu:false}),
    new Page('Cambridge Front Page', 'layouts/page.jade')
  ]),
  new Page('Core Elements', null, [
    new Page('Typography', 'pages/core_elements/typography.jade'),
    new Page('Links and Buttons', 'pages/core_elements/links_and_buttons.jade'),
    new Page('Forms', 'pages/core_elements/forms.jade'),
    new Page('Lists', 'layouts/page.jade'),
    new Page('Themes', 'layouts/page.jade'),
  ])
  new Page('In Page Components', null, [
    new Page('Navigation', null, [
      new Page('Tabs', 'layouts/page.jade'),
      new Page('Pills', 'layouts/page.jade'),
      new Page('Pills (Stacked)', 'layouts/page.jade'),
      new Page('Stages', 'layouts/page.jade'),
      new Page('Pagination', 'layouts/page.jade'),
      new Page('A to Z', 'layouts/page.jade'),
      new Page('Search', 'layouts/page.jade'),
    ]),
    new Page('Content', null, [
      new Page('Tables', 'layouts/page.jade'),
      new Page('Alerts', 'layouts/page.jade'),
      new Page('Date/Time Picker', 'layouts/page.jade'),
    ]),
    new Page('Teasers', 'layouts/page.jade', [], {side_menu:false}),
  ]),
)

module.exports = pages
