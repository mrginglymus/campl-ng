Page = require './page.coffee'
Pages = require './pages.coffee'


pages = new Pages(
  new Page('About', 'layouts/page.html'),
  new Page('Page Layouts', null, [
    new Page('Subsection with navigation', 'layouts/page.html'),
    new Page('Subsection without navigation', 'layouts/page.html', [], {side_menu:false}),
    new Page('Subsection without right column', 'layouts/page.html'),
    new Page('App', 'layouts/page.html', [], {side_menu:false}),
    new Page('Cambridge Front Page', 'layouts/page.html')
  ]),
  new Page('Core Elements', null, [
    new Page('Typography', 'layouts/page.html'),
    new Page('Links and Buttons', 'layouts/page.html'),
    new Page('Forms', 'layouts/page.html'),
    new Page('Lists', 'layouts/page.html'),
    new Page('Themes', 'layouts/page.html'),
  ])
  new Page('In Page Components', null, [
    new Page('Navigation', null, [
      new Page('Tabs', 'layouts/page.html'),
      new Page('Pills', 'layouts/page.html'),
      new Page('Pills (Stacked)', 'layouts/page.html'),
      new Page('Stages', 'layouts/page.html'),
      new Page('Pagination', 'layouts/page.html'),
      new Page('A to Z', 'layouts/page.html'),
      new Page('Search', 'layouts/page.html'),
    ]),
    new Page('Content', null, [
      new Page('Tables', 'layouts/page.html'),
      new Page('Alerts', 'layouts/page.html'),
      new Page('Date/Time Picker', 'layouts/page.html'),
    ]),
    new Page('Teasers', 'layouts/page.html', [], {side_menu:false}),
  ]),
)

module.exports = pages

###
ages = Pages([
  Page('About', 'demo.html'),
  Page('Page Layouts', 'layouts/overview.html', children=[
    Page('Subsection with navigation', 'layouts/subnav.html'),
    Page('Subsection without navigation', 'layouts/subnonav.html', side_menu=False),
    Page('Subsection without right column', 'layouts/subnocol.html'),
    Page('App', 'layouts/app.html', side_menu=False),
    Page('Cambridge Front Page', 'layouts/campage.html', globals={'CAM_PAGE': True}),
  ]),
  Page('Core Elements', children=[
    Page('Typography', 'core_elements/typography.html', scss=['core_elements/_typography.scss', 'core_elements/_blockquote.scss']),
    Page('Links and Buttons', 'core_elements/links_and_buttons.html', scss=['core_elements/_buttons.scss']),
    Page('Forms', 'core_elements/forms.html'),
    Page('Lists', 'core_elements/lists.html'),
    Page('Themes', 'core_elements/themes.html'),
  ]),
  Page('In Page Components', children=[
    Page('Navigation', children=[
      Page('Tabs', 'components/inpage/navigation/tabs.html', scss=['components/navigation/_nav.scss']),
      Page('Pills', 'components/inpage/navigation/pills.html', scss=['components/navigation/_nav.scss']),
      Page('Pills (Stacked)', 'components/inpage/navigation/pills_stacked.html', scss=['components/navigation/_nav.scss']),
      Page('Stages', 'components/inpage/navigation/stages.html', scss=['components/navigation/_nav.scss']),
      Page('Pagination', 'components/inpage/navigation/pagination.html', scss=['components/navigation/_pagination.scss']),
      Page('A to Z', 'components/inpage/navigation/atoz.html', context={'A_TO_Z': A_TO_Z}, side_menu=False),
      Page('Search', 'components/inpage/navigation/search.html', scss=['components/navigation/_search.scss']),
    ]),
    Page('Content', children=[
      Page('Tables', 'components/inpage/content/tables.html', scss=['components/inpage/_tables.scss']),
      Page('Alerts', 'components/inpage/content/alerts.html', scss=['components/inpage/_alerts.scss']),
      Page('Date/Time Picker', 'components/inpage/content/datetimepicker.html'),
    ]),
    Page('Teasers', 'components/teasers/examples.html', side_menu=False),
  ]),
  Page('Templates', children=template_pages),
  Page('Stylesheets', children=scss_pages),
])

front_page = FrontPage(
  'Home',
  'layouts/frontpage_example.html',
  pages,
)
###
