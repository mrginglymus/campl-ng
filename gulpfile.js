var gulp = require('gulp');
var sass = require('gulp-sass');
var globSass = require('gulp-sass-globbing');
var autoprefixer = require('autoprefixer');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');
var cssnano = require('gulp-cssnano');
var del = require('del');
var mirror = require('gulp-mirror');
var pipe = require('multipipe');
var coffee = require('gulp-coffee');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var modernizr = require('gulp-modernizr');
var sequence = require('run-sequence');
var python = require('python-shell');
var postcss = require('gulp-postcss');
var assets = require('postcss-assets');
var sass_json_importer = require('node-sass-json-importer');
var replace = require('gulp-replace');
var uuid = require('node-uuid');
var execSync = require('child_process').execSync;

gulp.task('default', function(cb) {
	sequence('build', 'deploy', cb);
})

gulp.task('build', function(cb) {
	sequence('clean', ['assets', 'html'], cb);
});

gulp.task('assets', function(cb) {
	sequence(['css', 'js', 'fonts', 'images', 'favicon'], 'modernizr', cb);
})

gulp.task('css', function(cb) {
	sequence('glob', ['css-core', 'css-legacy', 'css-meta'], cb);
});

gulp.task('js', [
	'js-core',
	'js-meta',
	'js-jquery',
	'js-lib'
]);

gulp.task('html', function(cb) {
	sequence('html-gen', 'root-url', cb);
})

gulp.task('html-gen', function(cb) {
	python.run('make.py', cb);
})

gulp.task('root-url', function() {
	return gulp.src(['build/**/*.html', '!build/templates/**/*', 'build/templates/**/index.html'])
		.pipe(replace(/\=\"\/(?!\/)/g, function() {
			return "=\"" + process.env.LOCAL_ROOT_URL + "/";
		}))
		.pipe(gulp.dest('build'));
})

gulp.task('cache-images', function() {
	return gulp.src(['build/**/*.html', '!build/templates/**/*.html'])
		.pipe(replace(/img src="(http.+?)"/g, function(match, img) {
			u = uuid.v4();
			r = execSync("wget -O build/images/" + u + " " + img);
			return "img src=\"" + process.env.LOCAL_ROOT_URL + "/images/" + u + "\"";
		}))
		.pipe(gulp.dest('build'));
})

gulp.task('images', function() {
	return gulp.src('images/logo.png')
		.pipe(gulp.dest('build/images'));
})

gulp.task('fonts', function() {
	return gulp.src('bower_components/font-awesome/fonts/*')
		.pipe(gulp.dest('build/fonts'));
})

gulp.task('favicon', function() {
	return gulp.src('favicon.ico')
		.pipe(gulp.dest('build'));
})

gulp.task('deploy', function() {
	return gulp.src('build/**/*')
		.pipe(gulp.dest(process.env.LOCAL_RELEASE_DIR));
})


gulp.task('clean', function() {
	return del(['build/**/*']);
})

gulp.task('js-core', function() {
	return gulp.src([
			'coffee/menu.coffee',
            'coffee/select_tab.coffee',
            'coffee/carousel.coffee',
            'coffee/object_fit.coffee',
            'coffee/flexbox.coffee'
		])
		.pipe(sourcemaps.init())
		.pipe(concat('campl.coffee'))
		.pipe(coffee())
		.pipe(
			mirror(
				pipe(
					concat('campl.js'),
					sourcemaps.write('.')
				),
				pipe(
					concat('campl.min.js'),
					uglify()
				)
			)
		)
		.pipe(gulp.dest('build/js'));
})

gulp.task('js-meta', function() {
	return gulp.src('coffee/theme_switcher.coffee')
		.pipe(sourcemaps.init())
		.pipe(coffee())
		.pipe(
			mirror(
				pipe(
					concat('meta.js'),
					sourcemaps.write('.')
				),
				pipe(
					concat('meta.min.js'),
					uglify()
				)
			)
		)
		.pipe(gulp.dest('build/js'));
})

gulp.task('js-jquery', function() {
	return gulp.src('bower_components/jquery/dist/jquery.js')
		.pipe(gulp.dest('build/js'))
		.pipe(uglify())
		.pipe(rename({extname: '.min.js'}))
		.pipe(gulp.dest('build/js'))
})

gulp.task('js-lib', function() {
	return gulp.src([
		'bower_components/tether/dist/js/tether.js',
        'bower_components/bootstrap/dist/js/bootstrap.js',
        'bower_components/moment/moment.js',
        'bower_components/moment/locale/en-gb.js',
        'bower_components/eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
        'bower_components/hammerjs/hammer.js',
        'bower_components/jquery-hammerjs/jquery.hammer.js',
        'bower_components/js-cookie/src/js.cookie.js'
	])
	.pipe(sourcemaps.init())
	.pipe(concat('lib.js'))
	.pipe(
		mirror(
			pipe(
				concat('lib.js'),
				sourcemaps.write('.')
			),
			pipe(
				concat('lib.min.js'),
				uglify()
			)
		)
	)
	.pipe(gulp.dest('build/js'))
})

gulp.task('modernizr', function() {
	return gulp.src('build/**/*.{js,css}')
		.pipe(modernizr('modernizr.js', {
			excludeTests: ['svg']
		}))
		.pipe(gulp.dest('build/js'))
		.pipe(uglify())
		.pipe(rename({extname: '.min.js'}))
		.pipe(gulp.dest('build/js'))
})

gulp.task('css-core', function() {
	return gulp.src('scss/campl.scss')
		.pipe(sourcemaps.init())
		.pipe(sass({
			importer: sass_json_importer
		}))
		.pipe(
			postcss([
				autoprefixer({
					browsers: [
						'Android 2.3',
		              	'Android >= 4',
		              	'Chrome >= 35',
		              	'Firefox >= 31',
		              	'Explorer >= 10',
		              	'iOS >= 7',
		              	'Opera >= 12',
		              	'Safari >= 7.1'
					]
				}),
				assets({
					loadPaths: ['images/']
				})

			])
		)
		.pipe(
			mirror(
				pipe(sourcemaps.write('.')),
				pipe(
					cssnano(),
					rename({extname: '.min.css'}),
					sourcemaps.write('.')
				)
			)
		)
		.pipe(gulp.dest('build/css'));
});

gulp.task('css-legacy', function() {
	return gulp.src('scss/campl_legacy.scss')
		.pipe(sourcemaps.init())
		.pipe(sass({
			importer: sass_json_importer
		}))
		.pipe(
			postcss([
				autoprefixer({
					browsers: [
						'Explorer 9'
					]
				}),
				assets({
					loadPaths: ['images/']
				})
			])
		)
		.pipe(
			mirror(
				pipe(sourcemaps.write('.')),
				pipe(
					cssnano(),
					rename({extname: '.min.css'}),
					sourcemaps.write('.')
				)
			)
		)
		.pipe(gulp.dest('build/css'));
})

gulp.task('css-meta', function() {
	return gulp.src('scss/meta.scss')
		.pipe(sourcemaps.init())
		.pipe(sass({
			importer: sass_json_importer
		}))
		.pipe(
			postcss([
				autoprefixer({
					browsers: [
						'Android 2.3',
		              	'Android >= 4',
		              	'Chrome >= 35',
		              	'Firefox >= 31',
		              	'Explorer >= 10',
		              	'iOS >= 7',
		              	'Opera >= 12',
		              	'Safari >= 7.1'
					]
				})
			])
		)
		.pipe(
			mirror(
				pipe(sourcemaps.write('.')),
				pipe(
					cssnano(),
					rename({extname: '.min.css'}),
					sourcemaps.write('.')
				)
			)
		)
		.pipe(gulp.dest('build/css'));
})

gulp.task('glob', function() {
	gulp.src('components/**/*.scss', {cwd: 'scss'})
		.pipe(globSass({
			path: 'scss/_components.scss'
		}))
		.pipe(gulp.dest(''));
	gulp.src('core_elements/**/*.scss', {cwd: 'scss'})
		.pipe(globSass({
			path: 'scss/_core_elements.scss'
		}))
		.pipe(gulp.dest(''));
	gulp.src('layout/**/*.scss', {cwd: 'scss'})
		.pipe(globSass({
			path: 'scss/_layout.scss'
		}))
		.pipe(gulp.dest(''));
	gulp.src('navigation/**/*.scss', {cwd: 'scss'})
		.pipe(globSass({
			path: 'scss/_navigation.scss'
		}))
		.pipe(gulp.dest(''));

})