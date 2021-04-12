class Page {
    constructor(title, source = null, children = [], options = {}) {
        this.title = title;
        this.source = source;
        this.children = children;
        this.options = options
    }

    get destination() {
        return ''
    }

    get url() {
        return ''
    }
}

class FrontPage extends Page {
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