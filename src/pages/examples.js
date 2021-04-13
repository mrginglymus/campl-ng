const Parser = require('rss-parser');
const {LoremIpsum,} = require('lorem-ipsum')

const lorem = new LoremIpsum()
lorem.format = 'html'

class Articles {

    constructor() {
        this.articles = []
    }

    async populate() {
        const parser = new Parser()
        const feed = await parser.parseURL('http://www.cam.ac.uk/news/feed')
        this.articles = feed.items
    }

    randomArticle() {
        const article = this.articles[Math.floor(Math.random() * this.articles.length)]
        return {
            title: article.title,
            link: article.link,
            body: article.contentSnippet.split('.')[0] + '.',
            date: new Date(article.pubDate)
        }
    }
}

const articles = new Articles();

function randomImage(width, height) {
    if (!height) {
        height = width
    }
    height = Math.floor(height * (Math.random() + 1))
    width = Math.floor(width * (Math.random() + 1))
    return `//placehold.it/${width}x${height}`;
}

const localFooterLinks = [
    [
        {
            header: "About the Faculty",
            links: [
                "Lorem ipsum dolor",
                "Sit amet",
                "Consectetur adipisicing elit",
                "Sed do eiusmod",
                "Tempor Incididunt"
            ]
        },
        {
            header: "Research",
            links: [
                "Ut labore et dolore",
                "Ut enim ad minim veniam",
                "Magna aliqua"
            ]
        }
    ],
    [
        {
            header: "About the University",
            links: [
                "Quis nostrud exercitation",
                "Ullamco laboris nisi",
                "Ut aliquip ex ea commodo",
                "Duis aute irure dolor"
            ]
        },
        {
            header: "Libraries & facilities",
            links: [
                "In reprehenderit in voluptate",
                "Velit esse cillum dolore",
                "Eu fugiat nulla pariatur",
                "Duis aute irure dolor"
            ]
        }
    ],
    [
        {
            header: "Graduate",
            links: [
                "Excepteur sint occaecat",
                "Cupidatat non proident"
            ]
        }
    ],
    [
        {
            header: "Subjects",
            links: [
                "Sunt in culpa qui officia",
                "Deserunt mollit anim",
                "Id est laborum",
                "Duis aute irure dolor"
            ]
        }
    ]
]

function makeCarousel() {
    return [
        [articles.randomArticle(), randomImage(885, 432)],
        [articles.randomArticle(), randomImage(885, 432)],
        [articles.randomArticle(), randomImage(885, 432)]
    ]
}

const videos = {
    "16by9": "//www.youtube.com/embed/Nz8gqWsSpm8",
    "4by3": "//www.youtube.com/embed/8-QNAwUdHUQ",
}

const navItems = [
    {
        'title': 'Active',
        'id': 'tab1',
        'disabled': false,
        'active': true,
        'content': lorem.generateParagraphs(2),
    },
    {
        'title': 'Link',
        'id': 'tab2',
        'disabled': false,
        'active': false,
        'content': lorem.generateParagraphs(2),
    },
    {
        'title': 'Another Link',
        'id': 'tab3',
        'disabled': false,
        'active': false,
        'content': lorem.generateParagraphs(2),
    },
    {
        'title': 'Disabled',
        'disabled': true
    }
]

module.exports = {
    localFooterLinks,
    makeCarousel,
    articles,
    randomImage,
    videos,
    navItems
}