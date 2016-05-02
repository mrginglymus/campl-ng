class Pages extends Array
  constructor: ->
    @push arguments...
    for page in @
      page.update_url()
    for page in @
      page.update_breadcrumbs(@)

module.exports = Pages
