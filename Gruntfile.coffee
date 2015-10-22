sass_options =
  sourcemap: 'inline',
  trace: true,
  require: './lib/loaders.rb',
  compass: true,
  style: 'compressed',

uuid = require('node-uuid')
execSync = require('child_process').execSync

module.exports = (grunt) ->

  grunt.option('target', grunt.option('target') or 'local')

  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-jade'
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

  grunt.initConfig
    pkg: grunt.file.readJSON('package.json')
    local_settings: grunt.file.readJSON('local_settings.json')
    site_structure: require('./site_content/structure.coffee')

    clean:
      dist: 'dist',
      build: 'build',

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
          require('autoprefixer')
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
          'build/js/lib.min.js': [
            'bower_components/jquery/dist/jquery.js',
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
            return 'img src="' + grunt.config.data.local_settings[grunt.option('target')].root_url + '/images/' + u + '"'
        ]
      root_url:
        src: ['build/**/*.html', '!build/templates/**/*', 'build/templates/**/index.html']
        overwrite: true
        replacements: [
          from: /\=\"\/(?!\/)/g
          to: ->
            return '="' + grunt.config.data.local_settings[grunt.option('target')].root_url + '/'
        ]

    exec:
      html:
        cmd: 'plenv/bin/python make.py'

    copy:
      favicon:
        src: 'favicon.ico',
        dest: 'build/favicon.ico'
      images:
        expand: true
        cwd: 'images'
        src: [
          'logo.png'
        ]
        dest: 'build/images'
      fonts:
        expand: true,
        cwd: 'bower_components/font-awesome/fonts',
        src: ['*'],
        dest: 'build/fonts'
      dist:
        expand: true
        cwd: 'build'
        src: [
          'images/logo.png',
          'js/lib.min.js',
          'js/campl.min.js',
          'js/modernizr.min.js',
          'css/campl.min.css',
          'css/campl_legacy.min.css',
          'fonts/*',
          'favicon.ico'
        ]
        dest: 'dist'

    jade:
      options:
        data:
          ROOT: '<%= local_settings.root_url %>'
          REMOTE_JS: [
            'https://code.jquery.com/jquery-1.11.3.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/moment.js',
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/locale/en-gb.js',
            'https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.0.3/js.cookie.js',
            'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.37/js/bootstrap-datetimepicker.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/js/bootstrap.min.js'
          ]
          LOCAL_JS: [
            'js/campl.js',
            'js/theme_switcher.js',
          ]
          LINKS: grunt.file.readJSON('site_content/links.json')
          COLOURS: grunt.file.readJSON('themes.json')
          PAGES: require('./site_content/structure.coffee').pages
      compile:
        files:
          expand: true
          cwd: 'templates'
          src: '**'
          ext: '/index.html'
          dest: 'build'

    rsync:
      options:
        recursive: true
      local:
        options:
          src: "build/*"
          dest: "<%= local_settings.local.release_dir %>"
      remote:
        options:
          src: "build/*"
          dest: "<%= local_settings.remote.release_dir %>"
          host: "<%= local_settings.remote.host %>"


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


  grunt.registerTask 'default', ['clean:build', 'sass:core', 'coffee:core']

  grunt.registerTask 'build-css', ['sass_globbing', 'sass', 'postcss']

  grunt.registerTask 'build-js', ['coffee:core', 'coffee:meta', 'uglify']

  grunt.registerTask 'build-images', ['copy:images', 'copy:favicon']

  grunt.registerTask 'build-html', ['build-jade', 'replace:root_url']

  grunt.registerTask 'build-fonts', ['copy:fonts']

  grunt.registerTask 'build', ['clean:build', 'build-css', 'build-js', 'build-images', 'build-html', 'build-fonts', 'modernizr']

  grunt.registerTask 'dist', ['clean:dist', 'build', 'copy:dist']

  grunt.registerTask 'build-jade', "Build HTML from Jade", ->
    BASE_CONTEXT =
      LINKS: grunt.file.readJSON('site_content/links.json')
      COLOURS: grunt.file.readJSON('themes.json')
      IMAGE_STYLES: grunt.file.readJSON('images.json')
      PAGES: grunt.config.data.site_structure
      lipsum: require('lorem-ipsum')
      random_image: (width, height = null) ->
        if not height
          height = width
          scale = Math.random() + 1
          height = Math.floor height * scale
          scale = Math.random() + 1
          width = Math.floor width * scale
          return "http://loremflickr.com/#{width}/#{height}/?user=cambridge%%20university"

    for page in grunt.config.data.site_structure
      page.render BASE_CONTEXT, grunt

  grunt.registerTask 'deploy', ['rsync:' + grunt.option('target')]

  grunt.registerTask 'cache-images', ['replace:image_cache']

  grunt.registerTask 'test', ['coffee:test', 'webdriver']
