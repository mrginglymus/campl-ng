sass_options = 
  sourcemap: 'inline',
  trace: true,
  require: './lib/themes.rb',
  compass: true,

REMOTE_JS = [
  'https://code.jquery.com/jquery-1.11.3.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/moment.js',
  'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/locale/en-gb.js',
  'https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.0.3/js.cookie.js',
]

module.exports = (grunt) ->
  
  grunt.loadNpmTasks 'grunt-contrib-sass'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-contrib-concat'
  grunt.loadNpmTasks 'grunt-contrib-uglify'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-jade'
  grunt.loadNpmTasks 'grunt-contrib-watch'

  
  grunt.initConfig
    pkg: grunt.file.readJSON('package.json')
    local_settings: grunt.file.readJSON('local_settings.json')

    env:
      local:
        ROOT_DIR: '/Users/bill/Sites/campl-ng'
        ROOT_URL: '/~bill/campl-ng'

    clean: 
      dist: 'dist',
      build: 'build',
      
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
    
    concat:
      core:
        src: [
          'js/menu.js',
          'js/select_tab.js',
        ]
        dest:
          'build/js/campl.js'
      dev:
        src: [
          'js/theme_switcher.js',
        ]
        dest:
          'build/js/theme_switcher.js'
    
    uglify:
      options:
        sourceMap: true
        sourceMapIncludeSources: true
      core:
        src: '<%= concat.core.dest %>'
        dest: 'build/js/campl.min.js'
      dev:
        src: '<%= concat.dev.dest %>'
        dest: 'build/js/theme_switcher.min.js'
        
    copy:
      images:
        expand: true
        cwd: 'images'
        src: [
          'logo.png'
        ]
        dest: 'build/images'
      dist:
        expand: true
        cwd: 'build'
        src: [
          'images/**',
          'js/**',
          'css/**',
        ]
        dest: 'dist'
      deploy:
        expand: true
        cwd: 'build'
        src: ['**']
        dest: '<%= local_settings.release_dir %>'

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
      compile:
        files:
          'build/base.html': ['templates-jade/layouts/page.jade']      
          
    watch:
      html:
        files: 'templates-jade/**'
        tasks: ['jade', 'copy:deploy']
      css:
        files: 'scss/**'
        tasks: ['sass:core', 'copy:dist']
    
  grunt.registerTask 'default', ['clean:build', 'sass:core', 'concat:core']
  
  grunt.registerTask 'build-css', ['sass', 'cssmin']
  
  grunt.registerTask 'build-js', ['concat', 'uglify']
  
  grunt.registerTask 'build-images', ['copy:images']
  
  grunt.registerTask 'build', ['clean:build', 'build-css', 'build-js', 'build-images', 'copy:deploy']
  
  grunt.registerTask 'dist', ['clean:dist', 'build', 'copy:dist']

  grunt.registerTask 'deploy', ['copy:deploy']  
