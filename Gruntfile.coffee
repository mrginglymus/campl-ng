sass_options = 
  sourcemap: 'inline',
  trace: true,
  require: './lib/themes.rb',
  compass: true,

module.exports = (grunt) ->
  
  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-sass-globbing'
  grunt.loadNpmTasks 'grunt-exec'
  
  grunt.initConfig
    pkg: grunt.file.readJSON('package.json')
    local_settings: grunt.file.readJSON('local_settings.json')

    clean: 
      dist: 'dist',
      build: 'build',
      
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
      deploy:
        expand: true,
        cwd: 'build'
        src: ['**']
        dest: '<%= local_settings.release_dir %>'
          
    watch:
      css:
        files: 'scss/**/*.scss'
        tasks: ['sass_globbing', 'sass:core', 'sass:meta', 'copy:deploy']
      html:
        files: 'templates/**/*.html'
        tasks: ['exec:html', 'copy:deploy']
    
  grunt.registerTask 'default', ['clean:build', 'sass:core', 'coffee:core']
  
  grunt.registerTask 'build-css', ['sass_globbing', 'sass', 'cssmin']
  
  grunt.registerTask 'build-js', ['coffee', 'uglify']
  
  grunt.registerTask 'build-images', ['copy:images']

  grunt.registerTask 'build-html', ['exec:html']
  
  grunt.registerTask 'build', ['clean:build', 'build-css', 'build-js', 'build-images', 'build-html', 'copy:deploy']
  
  grunt.registerTask 'dist', ['clean:dist', 'build', 'copy:dist']

  grunt.registerTask 'deploy', ['copy:deploy']  