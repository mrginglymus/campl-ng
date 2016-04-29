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
var webserver = require('gulp-webserver');

gulp.task('default', ['build'])

/************************************************************/
/* Entrypoint tasks                                         */
/************************************************************/


gulp.task('build', function(cb) {
  sequence('clean', ['assets', 'html'], cb);
});

gulp.task('run', function() {
  return gulp.src('build')
    .pipe(webserver());
})

gulp.task('clean', function() {
  return del(['build/**/*']);
})


/************************************************************/
/* Misc asset tasks                                         */
/************************************************************/

gulp.task('assets', function(cb) {
  sequence(['css', 'js', 'fonts', 'images', 'favicon'], 'modernizr', cb);
})

gulp.task('cache-images', function() {
  return gulp.src(['build/**/*.html', '!build/templates/**/*.html'])
    .pipe(replace(/img src="(http.+?)"/g, function(match, img) {
      u = uuid.v4();
      r = execSync("wget -O build/images/" + u + " " + img);
      return "img src=\"/images/" + u + "\"";
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

/************************************************************/
/* HTML Tasks                                               */
/************************************************************/

gulp.task('html', function(cb) {
  sequence('html-gen', cb);
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

/************************************************************/
/* JS Tasks                                                 */
/************************************************************/

gulp.task('js', [
  'js-core',
  'js-meta',
  'js-jquery',
  'js-lib'
]);

// build core js
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

// build meta js
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

// copy and compress jquery
gulp.task('js-jquery', function() {
  return gulp.src('bower_components/jquery/dist/jquery.js')
    .pipe(gulp.dest('build/js'))
    .pipe(uglify())
    .pipe(rename({extname: '.min.js'}))
    .pipe(gulp.dest('build/js'))
})

// concat and compress lib
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

// build modernizr
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



/************************************************************/
/* CSS Tasks                                                */
/************************************************************/

gulp.task('css', function(cb) {
  sequence('glob', ['css-core', 'css-legacy', 'css-meta'], cb);
});

// browsers to use for autoprefixer
var browsers = [
  'Android 2.3',
  'Android >= 4',
  'Chrome >= 35',
  'Firefox >= 31',
  'Explorer >= 10',
  'iOS >= 7',
  'Opera >= 12',
  'Safari >= 7.1'
]

function glob(base) {
  return gulp.src(base + '/**/*.scss', {cwd: 'scss'})
    .pipe(globSass({
      path: 'scss/_' + base + '.scss'
    }))
}

// Glob files - create glob files for including all files in subdirectory.
gulp.task('glob', function() {
  glob('components');
  glob('core_elements');
  glob('layout');
  glob('navigation');
})

function build_css(src, browsers) {
  return gulp.src(src)
    .pipe(sourcemaps.init())
    .pipe(sass({
      importer: sass_json_importer
    }))
    .pipe(
      postcss([
        autoprefixer({
          browsers: browsers
        }),
        assets({
          loadPaths: ['images/']
        })

      ])
    )
    .pipe(
      mirror(
        pipe(
          sourcemaps.write('.')
        ),
        pipe(
          cssnano(),
          rename({extname: '.min.css'}),
          sourcemaps.write('.')
        )
      )
    )
    .pipe(gulp.dest('build/css'));
}

// Build css
gulp.task('css-core', function() {
  return build_css('scss/campl.scss', browsers);
});

// Build legacy (non-flexbox version) css
gulp.task('css-legacy', function() {
  return build_css('scss/campl_legacy.scss', ['Explorer 9']);
})

// build meta files
gulp.task('css-meta', function() {
  return build_css('scss/meta.scss', browsers);
})