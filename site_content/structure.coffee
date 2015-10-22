Page = require './page.coffee'
Pages = require './pages.coffee'


pages = new Pages(
  new Page('About', 'pages/about.jade'),
  new Page('Page Layouts', null, [
    new Page('Subsection with navigation', 'layout/page.jade'),
    new Page('Subsection without navigation', 'layout/page.jade', [], {side_menu:false}),
    new Page('Subsection without right column', 'layout/page.jade'),
    new Page('App', 'layout/page.jade', [], {side_menu:false}),
    new Page('Cambridge Front Page', 'layout/page.jade')
  ]),
  new Page('Core Elements', null, [
    new Page('Typography', 'pages/core_elements/typography.jade'),
    new Page('Links and Buttons', 'pages/core_elements/links_and_buttons.jade'),
    new Page('Forms', 'pages/core_elements/forms.jade'),
    new Page('Lists', 'layout/page.jade'),
    new Page('Images', 'pages/core_elements/images.jade'),
    new Page('Themes', 'layout/page.jade'),
  ])
  new Page('In Page Components', null, [
    new Page('Navigation', null, [
      new Page('Tabs', 'layout/page.jade'),
      new Page('Pills', 'layout/page.jade'),
      new Page('Pills (Stacked)', 'layout/page.jade'),
      new Page('Stages', 'layout/page.jade'),
      new Page('Pagination', 'layout/page.jade'),
      new Page('A to Z', 'layout/page.jade'),
      new Page('Search', 'layout/page.jade'),
    ]),
    new Page('Content', null, [
      new Page('Tables', 'layout/page.jade'),
      new Page('Alerts', 'layout/page.jade'),
      new Page('Date/Time Picker', 'layout/page.jade'),
    ]),
    new Page('Teasers', 'layout/page.jade', [], {side_menu:false}),
  ]),
)

module.exports = pages
