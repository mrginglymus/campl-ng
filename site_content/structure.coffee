Page = require './page.coffee'
Pages = require './pages.coffee'


site_structure = new Pages(
  new Page('About', 'about.jade'),
  new Page('Page Layouts', null, [
    new Page('Subsection With Navigation', 'layouts/subnav.jade'),
  ]),
)

module.exports = site_structure