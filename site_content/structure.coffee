Page = require './page.coffee'
Pages = require './pages.coffee'


pages = new Pages(
  new Page('About', 'pages/about.pug'),
)

module.exports = pages
