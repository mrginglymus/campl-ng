const pug = require('pug');
const fs = require('fs');
const path = require('path');


class Page {
    constructor(title, source = null, options = {}) {
        options = {
            children: [],
            scss: [],
            image: null,
            hasSideMenu: true,
            hasSideBar: true,
            ...options
        }

        this.title = title;
        this.source = source;
        this._url = `/${this.title.toLowerCase().replace(/ /g, '_')}`
        this.children = options.children;
        this.scss = options.scss;
        this.image = options.image;
        this.hasSideMenu = options.hasSideMenu
        this.isFrontPage = false
        this.horizontalBreadcrumb = [['Campl-NG', '/']]
        this.verticalBreadcrumb = []
        this.verticalBreadcrumbParent = null
        this.verticalBreadcrumbChildren = null
        this.verticalBreadcrumbSiblings = []
        this.type = 'page'
    }

    render(context) {
        if (this.source) {
            const template = pug.compileFile(path.join('src', 'pages', `${this.source}.pug`));
            const rendered = template({...context, page: this});
            fs.mkdirSync(path.join('build', path.dirname(this.destination)), {recursive: true})
            fs.writeFileSync(path.join('build', this.destination), rendered);
        }
        this.children.forEach(c => c.render(context));
    }

    updateUrl(root, parent) {
        this.parent = parent
        if (root) {
            this._url = root + this._url
        }
        this.children.forEach(c => c.updateUrl(this._url, this))
    }

    updateBreadcrumbs(pages, verticalBreadcrumb, horizontalBreadcrumb, parent) {
        horizontalBreadcrumb = horizontalBreadcrumb || [['Campl-NG', '/']]
        verticalBreadcrumb = verticalBreadcrumb || [['Campl-NG', '/']]

        this.horizontalBreadcrumb = [...horizontalBreadcrumb, [this.title, this.source ? this.url : null]]

        this.verticalBreadcrumb = [...verticalBreadcrumb, [this.title, this.url]]

        const verticalBreadcrumbBase = this.verticalBreadcrumb
        const horizontalBreadcrumbBase = this.horizontalBreadcrumb

        if (this.children.length > 0) {
            this.verticalBreadcrumbParent = this.horizontalBreadcrumb.slice(this.horizontalBreadcrumb.length - 1)[0]
            this.verticalBreadcrumb = this.verticalBreadcrumb.slice(0, this.horizontalBreadcrumb.length - 1)

            this.verticalBreadcrumbChildren = this.children.map(c => [c.title, c.url])

            if (parent) {
                this.verticalBreadcrumbSiblings = parent.children.map(c => [c.title, c.url])
            } else {
                this.verticalBreadcrumbSiblings = pages.map(p => [p.title, p.url])
            }
        } else if (!this.parent) {
            this.verticalBreadcrumb = [['Campl-NG', '/']]
            this.verticalBreadcrumbParent = [this.title, this.url]
            this.verticalBreadcrumbSiblings = pages.map(p => [p.title, p.url])
        } else {
            this.verticalBreadcrumbParent = this.horizontalBreadcrumb.slice(this.horizontalBreadcrumb.length - 2)[0]
            this.verticalBreadcrumb = this.verticalBreadcrumb.slice(0, this.horizontalBreadcrumb.length - 2)
            if (this.parent) {
                this.verticalBreadcrumbChildren = parent.children.map(c => [c.title, c.url])
                this.verticalBreadcrumbSiblings = parent.verticalBreadcrumbSiblings
            }
        }
        this.children.forEach(c => c.updateBreadcrumbs(pages, verticalBreadcrumbBase, horizontalBreadcrumbBase, this))
    }

    get destination() {
        return path.join(this.url.slice(1), 'index.html')
    }

    get url() {
        if (this.source) {
            return this._url
        } else if (this.children.length > 0) {
            return this.children[0].url
        } else {
            return ''
        }
    }

    get sourcesLinks() {
        if (this.type !== 'page') {
            return []
        }
        return [
            {
                title: ['pages', ...this.source.split('/')].join(' > ') + '.pug',
                link: `/templates/${this.source}/`
            }, ...this.scss.map(scss => ({
                title: ['styles', ...scss.split('/')].join(' > '),
                link: `/stylesheets/${scss}/`
            }))
        ]
    }
}

class FrontPage extends Page {

    constructor(title, source = null, children = [], options = {}) {
        super(title, source, children, options);
        this.isFrontPage = true
        this.hasSideMenu = false
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