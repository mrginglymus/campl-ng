sass_options =
  sourcemap: 'inline',
  importer: require('node-sass-json-importer'),
  style: 'compressed',

uuid = require('node-uuid')
execSync = require('child_process').execSync
inliner = require('postcss-image-inliner')

module.exports = (grunt) ->

  grunt.option('target', grunt.option('target') or 'local')

  grunt.loadNpmTasks 'grunt-sass'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-sass-globbing'
  grunt.loadNpmTasks 'grunt-scss-lint'
  grunt.loadNpmTasks 'grunt-exec'
  grunt.loadNpmTasks 'grunt-text-replace'
  grunt.loadNpmTasks 'grunt-rsync'
  grunt.loadNpmTasks 'grunt-coffeelint'
  grunt.loadNpmTasks 'grunt-html'
  grunt.loadNpmTasks 'grunt-modernizr'
  grunt.loadNpmTasks 'grunt-postcss'
  grunt.loadNpmTasks 'grunt-webdriver'
  grunt.loadNpmTasks 'grunt-env'
  grunt.loadNpmTasks 'grunt-http-server'

  grunt.initConfig
    pkg: grunt.file.readJSON('package.json')

    clean:
      dist: 'dist',
      build: 'build',

    env:
      local:
        ROOT_URL: process.env.LOCAL_ROOT_URL
        RELEASE_DIR: process.env.LOCAL_RELEASE_DIR
      remote:
        ROOT_URL: process.env.REMOTE_ROOT_URL
        RELEASE_DIR: process.env.REMOTE_RELEASE_DIR
        HOST: process.env.REMOTE_HOST
        
      
    scsslint:
      options:
        config: 'scss/.scss-lint.yml'
      src: ['scss/**/*.scss']

    coffeelint:
      options:
        configFile: 'coffee/coffeelint.json'
      src: ['coffee/**/*.coffee', 'Gruntfile.coffee']
      test: ['test/specs/**/*.coffee']

    htmllint:
      src: ['build/**/*.html', '!build/templates/**/*', 'build/templates/**/index.html']
      
    webdriver:
      test:
        configFile: './test/wdio.conf.js'

    modernizr:
      build:
        dest: 'build/js/modernizr.min.js'
        excludeTests: ['svg'],
        options: [],
        files:
          src: [
            'build/**/*.{js,css}'
          ]


    sass_globbing:
      core:
        files:
          'scss/_components.scss': 'scss/components/**/*.scss',
          'scss/_core_elements.scss': 'scss/core_elements/**/*.scss',
          'scss/_layout.scss': 'scss/layout/**/*.scss',
          'scss/_navigation.scss': 'scss/navigation/**/*.scss'

    sass:
      core:
        options:
          sass_options
        files:
          'build/css/campl.min.css': 'scss/campl.scss'
      legacy:
        options:
          sass_options
        files:
          'build/css/campl_legacy.min.css': 'scss/campl_legacy.scss'
      meta:
        options:
          sass_options
        files:
          'build/css/meta.min.css': 'scss/meta.scss'

    postcss:
      options:
        map:
          inline: false,
          annotation: 'build/css/'
      core:
        src: 'build/css/campl.min.css'
        processors: [
          inliner
            strict: true
        ]
      legacy:
        src: 'build/css/campl.min.css'
        processors: [
          require('autoprefixer')
            browsers: [
              'Explorer 9'
            ]
        ]

    coffee:
      core:
        files:
          'build/js/campl.js': [
            'coffee/menu.coffee',
            'coffee/select_tab.coffee',
            'coffee/carousel.coffee',
            'coffee/object_fit.coffee',
            'coffee/flexbox.coffee'
          ]
      meta:
        files:
          'build/js/theme_switcher.js': ['coffee/theme_switcher.coffee']
      test:
        options:
          bare: true
        expand: true
        flatten: false
        cwd: 'test/specs'
        src: ['**/*.coffee']
        dest: 'test/specs'
        ext: '.js'

    uglify:
      options:
        sourceMap: true
      core:
        src: 'build/js/campl.js'
        dest: 'build/js/campl.min.js'
      meta:
        src: 'build/js/theme_switcher.js'
        dest: 'build/js/theme_switcher.min.js'
      lib:
        files:
          'build/js/jquery.min.js': [
            'bower_components/jquery/dist/jquery.js',
          ],
          'build/js/lib.min.js': [
            'bower_components/tether/dist/js/tether.js',
            'bower_components/bootstrap/dist/js/bootstrap.js',
            'bower_components/moment/moment.js',
            'bower_components/moment/locale/en-gb.js',
            'bower_components/eonasdan-bootstrap-datetimepicker/build/js/bootstrap-datetimepicker.min.js',
            'bower_components/hammerjs/hammer.js',
            'bower_components/jquery-hammerjs/jquery.hammer.js',
            'bower_components/js-cookie/src/js.cookie.js'
          ]

    replace:
      image_cache:
        src: ['build/**/*.html', '!build/templates/**/*.html'],
        overwrite: true,
        replacements: [
          from: /img src="(http.+?)"/g
          to: (match, index, fulltext, matches) ->
            u = uuid.v4()
            r = execSync "wget -O build/images/" + u + " " + matches[0]
            return "img src=\"<%= ROOT_URL %>/images/#{u}\""
        ]
      root_url:
        src: ['build/**/*.html', '!build/templates/**/*', 'build/templates/**/index.html']
        overwrite: true
        replacements: [
          from: /\=\"\/(?!\/)/g
          to: ->
            return "=\"<%= ROOT_URL %>/"
        ]

    exec:
      html:
        cmd: 'python make.py'

    copy:
      favicon:
        src: 'favicon.ico',
        dest: 'build/favicon.ico'
      images:
        expand: true,
        cwd: 'images'
        src: [
          'logo.png',
        ]
        dest: 'build/images'
      fonts:
        expand: true,
        cwd: 'bower_components/font-awesome/fonts',
        src: ['*'],
        dest: 'build/fonts'
      dist:
        expand: true,
        cwd: 'build'
        src: [
          'images/logo.png',
          'js/jquery.min.js',
          'js/lib.min.js',
          'js/campl.min.js',
          'js/modernizr.min.js',
          'css/campl.min.css',
          'css/campl_legacy.min.css',
          'fonts/*',
          'favicon.ico'
        ]
        dest: 'dist'

    'http-server':
      test:
        root: 'build/'
        port: 8080
        host: "0.0.0.0"
        runInBackground: true
        
    rsync:
      options:
        recursive: true
      local:
        options:
          src: "build/*"
          dest: "<%= RELEASE_DIR %>"
      remote:
        options:
          src: "build/*"
          dest: "<%= RELEASE_DIR %>"
          host: "<%= HOST %>"

    watch:
      css:
        files: 'scss/**/*.scss'
        tasks: ['sass_globbing', 'sass:core', 'sass:meta', 'deploy']
      html:
        files: 'templates/**/*.html'
        tasks: ['build-html', 'deploy']
      js:
        files: 'coffee/**/*.coffee'
        tasks: ['build-js', 'deploy']
      scsslint:
        files: ['scss/**/*.scss', 'scss/.scss-lint.yml']
        tasks: ['scsslint']
      coffeelint:
        files: ['coffee/**/*.coffee']
        tasks: ['coffeelint']

  grunt.registerTask 'setenv', "Set environment", ->
    grunt.config('RELEASE_DIR', process.env.RELEASE_DIR)
    grunt.config('HOST', process.env.HOST)
    grunt.config('ROOT_URL', process.env.ROOT_URL)
  
  grunt.registerTask 'deploy', "Deploy", ->
    if grunt.config('HOST')
      grunt.task.run('rsync:remote')
    else
      grunt.task.run('rsync:local')
        
  grunt.registerTask 'default', ['clean:build', 'sass:core', 'coffee:core']

  grunt.registerTask 'build-css', ['sass_globbing', 'sass', 'postcss']

  grunt.registerTask 'build-js', ['coffee:core', 'coffee:meta', 'uglify']

  grunt.registerTask 'build-images', ['copy:images', 'copy:favicon']

  grunt.registerTask 'build-html', ['exec:html', 'replace:root_url']

  grunt.registerTask 'build-fonts', ['copy:fonts']

  grunt.registerTask 'build', ['clean:build', 'build-css', 'build-js', 'build-images', 'build-html', 'build-fonts', 'modernizr']

  grunt.registerTask 'dist', ['clean:dist', 'build', 'copy:dist']
  
  grunt.registerTask 'cache-images', ['replace:image_cache']

  grunt.registerTask 'test', ['http-server', 'coffee:test', 'webdriver']

  grunt.task.run('env:' + grunt.option('target'), 'setenv')
