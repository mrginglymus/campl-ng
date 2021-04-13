class Page {
    constructor(title, source = null, children = [], options = {}) {
        this.title = title;
        this.source = source;
        this.children = children;
        this.options = options
        this.isFrontPage = false
        this.horizontalBreadcrumb = [['Campl-NG', '/']]
        this.verticalBreadcrumb = []
        this.verticalBreadcrumbParent = null
        this.verticalBreadcrumbChildren = null
        this.verticalBreadcrumbSiblings = []
    }

    get destination() {
        return ''
    }

    get url() {
        return ''
    }
}

class FrontPage extends Page {

    constructor(title, source = null, children = [], options = {}) {
        super(title, source, children, options);
        this.isFrontPage = true
    }

    get destination() {
        return 'index.html'
    }

    get url() {
        return ''
    }
}

module.exports = {
    FrontPage,
    Page
}