/* eslint-env node */

module.exports = {
    'env': {
        'node': true,
        'es2021': true
    },
    'globals': {
        '$': false,
    },
    'extends': [
        'eslint:recommended',
    ],
    'parserOptions': {
        'ecmaVersion': 12,
        'sourceType': 'module'
    },
    'plugins': [
        'import'
    ],
    'settings': {
        'import/resolver': {
            'node': {
                'extensions': [
                    '.js',
                    '.json',
                    '.scss',
                ]
            }
        },
        'import/internal-regex': '^campl-ng'
    },
    'rules': {
        'import/order': [
            'error',
            {
                'newlines-between': 'always',
                'alphabetize': {
                    'order': 'asc',
                    'caseInsensitive': true,
                }
            }
        ],
        'indent': [
            'error',
            4
        ],
        'quotes': [
            'error',
            'single',
            {
                'avoidEscape': true,
                'allowTemplateLiterals': true
            }
        ],
        'semi': [
            'error',
            'always',
            {
                'omitLastInOneLineBlock': false
            }
        ],
        'semi-spacing': [
            'error',
            {
                'before': false,
                'after': true
            }
        ],
        'semi-style': [
            'error',
            'last'
        ],
        'space-before-function-paren': [
            'error', {
                'anonymous': 'never',
                'named': 'never',
                'asyncArrow': 'always'
            }
        ],
        'func-call-spacing': [
            'error',
            'never'
        ],
        'no-whitespace-before-property': [
            'error'
        ],
        'space-infix-ops': [
            'error'
        ],
        'space-unary-ops': [
            'error',
            {
                'words': true,
                'nonwords': false
            }
        ],
        'eol-last': [
            'error',
            'always'
        ],
        'function-paren-newline': [
            'error',
            'consistent'
        ],
        'array-bracket-newline': [
            'error',
            'consistent'
        ],
        'newline-per-chained-call': [
            'error',
            {
                'ignoreChainWithDepth': 3
            }
        ],
        'dot-location': [
            'error',
            'property'
        ],
        'dot-notation': [
            'error'
        ],
        'comma-dangle': [
            'error',
            {
                'arrays': 'only-multiline',
                'objects': 'only-multiline',
                'imports': 'only-multiline',
                'exports': 'only-multiline',
                'functions': 'ignore'
            }
        ],
        'comma-spacing': [
            'error',
            {
                'before': false,
                'after': true
            }
        ],
        'comma-style': [
            'error',
            'last'
        ],
        'curly': [
            'error',
            'all'
        ],
        'brace-style': [
            'error',
            '1tbs',
            {
                'allowSingleLine': false
            }
        ],
        'no-trailing-spaces': [
            'error'
        ],
        'no-loop-func': [
            'error'
        ],
        'no-multi-str': [
            'error'
        ],
        'implicit-arrow-linebreak': [
            'error',
            'beside'
        ],
        'arrow-parens': [
            'error',
            'as-needed',
            {
                'requireForBlockBody': false
            }
        ],
        'arrow-spacing': [
            'error',
            {
                'before': true,
                'after': true
            }
        ],
        'prefer-arrow-callback': [
            'error',
            {
                'allowNamedFunctions': false,
                'allowUnboundThis': true
            }
        ],
        'no-duplicate-imports': [
            'error'
        ],
        'no-var': [
            'error'
        ],
        'prefer-const': [
            'error'
        ],
        'prefer-spread': [
            'error'
        ],
        'template-curly-spacing': [
            'error',
            'never'
        ],
        'object-shorthand': [
            'error',
            'methods'
        ],
        'eqeqeq': [
            'error'
        ],
    }
};