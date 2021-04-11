/* eslint-env node */

const path = require('path');

const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const JsonImporter = require('node-sass-json-importer');

const SRC_ROOT = path.join(__dirname, 'src');

const OUTPUT_PATH = path.join(__dirname, 'build');
const JS_OUTPUT = path.join(OUTPUT_PATH, 'js');
const RELATIVE_JS_OUTPUT = path.relative(JS_OUTPUT, OUTPUT_PATH);

module.exports = (env, argv = {}) => {
    const MODE = argv.mode || 'production';
    const WATCH = argv.watch || false;

    const entrypoints = {
        campl: path.join(__dirname, 'src', 'scripts', 'campl.js'),
        demo: path.join(__dirname, 'demo', 'scripts', 'demo.js'),
    };

    return {
        mode: MODE,
        target: 'web',
        entry: Object.entries(entrypoints).reduce((acc, [name, file]) => {
            acc[name] = [file];
            return acc;
        }, {}),
        output: {
            path: JS_OUTPUT,
            filename: '[name].js',
        },
        devtool: MODE === 'production' ? 'source-map' : 'inline-source-map',
        amd: false,
        stats: 'minimal',
        externals: {
            jquery: 'jQuery',
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: path.join(RELATIVE_JS_OUTPUT, 'css', '[name].css'),
                chunkFilename: path.join(RELATIVE_JS_OUTPUT, 'css', '[name].css'),
            }),
            new CopyPlugin({
                patterns: [
                    {from: path.join(SRC_ROOT, 'favicon.ico'), to: OUTPUT_PATH},
                    {from: path.join(SRC_ROOT, 'images', 'logo.png'), to: path.join(OUTPUT_PATH, 'images', 'logo.png')}
                ]
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
                    test:/\.coffee$/,
                    loader: 'coffee-loader',
                },
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
                            loader: 'sass-loader',
                            options: {
                                sassOptions: {
                                    importer: JsonImporter()
                                }
                            }
                        }
                    ]
                },
                {
                    test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                name: '[name].[ext]',
                                outputPath: '../fonts',
                            }
                        }
                    ]
                },
                {
                    test: /\.png$/,
                    type: 'asset',
                }
            ]
        },
        resolve: {
            extensions: ['.js', '.json']
        },
        bail: !WATCH,
        devServer: {
            contentBase: OUTPUT_PATH
        }
    }
}
