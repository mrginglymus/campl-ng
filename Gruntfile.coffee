sass_options = 
  sourcemap: 'inline',
  trace: true,
  require: './lib/themes.rb',
  compass: true,

uuid = require('node-uuid')
execSync = require('child_process').execSync

module.exports = (grunt) ->
  
  grunt.option('target', grunt.option('target') || 'local')
  
  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-sass-globbing'
  grunt.loadNpmTasks 'grunt-scss-lint'
  grunt.loadNpmTasks 'grunt-exec'
  grunt.loadNpmTasks 'grunt-text-replace'
  grunt.loadNpmTasks 'grunt-rsync'
  
  grunt.initConfig
    pkg: grunt.file.readJSON('package.json')
    local_settings: grunt.file.readJSON('local_settings.json')

    clean: 
      dist: 'dist',
      build: 'build',
    
    scsslint:
      options:
        config: 'scss/.scss-lint.yml'
      src: ['scss/**/*.scss']

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
          'build/css/campl.css': 'scss/campl.scss'
      legacy:
        options:
          sass_options
        files:
          'build/css/campl_legacy.css': 'scss/campl_legacy.scss'
      meta:
        options:
          sass_options
        files:
          'build/css/meta.css': 'scss/meta.scss'
    
    cssmin:
      options:
        sourceMap: true
      core:
        files:[
          expand: true,
          cwd: 'build/css',
          src: ['*.css', '!*.min.css'],
          dest: 'build/css',
          ext: '.min.css',
        ]
    
    coffee:
      core:
        files:
          'build/js/campl.js': ['coffee/menu.coffee', 'coffee/select_tab.coffee']
      meta:
        files:
          'build/js/theme_switcher.js': ['coffee/theme_switcher.coffee']
    
    uglify:
      options:
        sourceMap: true
        sourceMapIncludeSources: true
      core:
        src: 'build/js/campl.js'
        dest: 'build/js/campl.min.js'
      meta:
        src: 'build/js/theme_switcher.js'
        dest: 'build/js/theme_switcher.min.js'
    
    replace:
      image_cache:
        src: ['build/**/*.html', '!build/templates/**/*.html'],
        overwrite: true,
        replacements: [
          from: /(http\:\/\/lorempixel\.com\/\d+\/\d+\/)/g
          to: (lp) ->
            u = uuid.v4()
            r = execSync "wget -O build/images/" + u + " " + lp
            return grunt.config.data.local_settings[grunt.option('target')].root_url + '/images/' + u
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
      images:
        expand: true,
        cwd: 'images'
        src: [
          'logo.png',
        ]
        dest: 'build/images'
      dist:
        expand: true,
        cwd: 'build'
        src: [
          'images/**',
          'js/**',
          'css/**',
          '!css/meta**'
        ]
        dest: 'dist'
    
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
        tasks: ['sass_globbing', 'sass:core', 'sass:meta', 'copy:local']
      html:
        files: 'templates/**/*.html'
        tasks: ['exec:html', 'rsync:local']
  
  
  grunt.registerTask 'default', ['clean:build', 'sass:core', 'coffee:core']
  
  grunt.registerTask 'build-css', ['sass_globbing', 'sass', 'cssmin']
  
  grunt.registerTask 'build-js', ['coffee', 'uglify']
  
  grunt.registerTask 'build-images', ['copy:images']

  grunt.registerTask 'build-html', ['exec:html', 'replace:root_url']
  
  grunt.registerTask 'build', ['clean:build', 'build-css', 'build-js', 'build-images', 'build-html']
  
  grunt.registerTask 'dist', ['clean:dist', 'build', 'copy:dist']

  grunt.registerTask 'deploy', ['rsync:' + grunt.option('target')]
  
  grunt.registerTask 'cache-images', ['replace:image_cache']
  

