import hljs from 'highlight.js/lib/core';
import  django from 'highlight.js/lib/languages/django';
import  xml from 'highlight.js/lib/languages/xml';
import  scss from 'highlight.js/lib/languages/scss';
import  javascript from 'highlight.js/lib/languages/javascript';

import 'highlight.js/scss/monokai-sublime.scss'

hljs.registerLanguage('django', django);
hljs.registerLanguage('scss', scss);
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('xml', xml)

import 'campl-ng-demo/styles/demo.scss';

import 'campl-ng-demo/scripts/theme-switcher';

$('pre code').each(function (i, block) {
    hljs.highlightBlock(block);
});
$('span.hljs-keyword:contains("import") + span.hljs-string:not(:contains("lib")):not(:contains("compass"))').each(function (i, e) {
    // special case for campl
    $(e).html($(e).html().replace(/['"](campl)['"]/, '\'<a href="/stylesheets/campl.scss/">campl</a>\''));
    $(e).html($(e).html().replace(/['"]((?:\w+\/)*)(\w+)['"]/, '\'<a href="/stylesheets/$1_$2.scss/">$1$2</a>\''));
});
$('span.hljs-template_tag:contains(".html")').each(function (i, e) {
    $(e).html($(e).html().replace(/'(.*.html)'/, '\'<a href="/templates/$1/">$1</a>\''));
});
