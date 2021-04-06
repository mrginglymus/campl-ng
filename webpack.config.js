/* eslint-env node */

const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const SRC_ROOT = path.join(__dirname, 'src');

const OUTPUT_PATH = path.join(__dirname, 'build');
const JS_OUTPUT = path.join(OUTPUT_PATH, 'js');
const RELATIVE_JS_OUTPUT = path.relative(JS_OUTPUT, OUTPUT_PATH);

module.exports = (env, argv = {}) => {
    const MODE = argv.mode || 'production';
    const WATCH = argv.watch || false;

    const entrypoints = {
        campl: 'campl.js',
    };

    return {
        mode: MODE,
        target: 'web',
        entry: Object.entries(entrypoints).reduce((acc, [name, file]) => {
            acc[name] = [
                path.join(SRC_ROOT, 'scripts', file),
            ];
            return acc;
        }, {}),
        output: {
            path: JS_OUTPUT,
            filename: '[name].js',
        },
        devtool: MODE === 'production' ? 'source-map' : 'inline-source-map',
        amd: false,
        stats: 'minimal',
        plugins: [
            new MiniCssExtractPlugin({
                filename: path.join(RELATIVE_JS_OUTPUT, 'css', '[name].css'),
                chunkFilename: path.join(RELATIVE_JS_OUTPUT, 'css', '[name].css'),
            }),
            new CaseSensitivePathsPlugin(),
            new BundleAnalyzerPlugin({
                analyzerMode: WATCH ? 'server' : 'disabled',
                openAnalyzer: false
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'babel-loader',
                            options: {
                                presets: ['@babel/preset-env'],
                            }
                        }
                    ]
                },
                {
                    test: /\.(?:c|sc|sa)ss$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                        },
                        {
                            loader: 'css-loader'
                        },
                        {
                            loader: 'sass-loader'
                        }
                    ]
                }
            ]
        },
        resolve: {
            extensions: ['.js', '.json']
        },
        bail: !WATCH
    }
}
