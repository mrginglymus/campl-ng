var gulp = require('gulp');
var sass = require('gulp-ruby-sass');
var compass = require('gulp-compass')
var globSass = require('gulp-sass-globbing');
var del = require('del');

gulp.task('default', [
	'clean',
	'glob',
	'css'
]);


gulp.task('clean', function() {
	return del(['build/**/*']);
})

gulp.task('css', function() {
	return sass('scss/campl.scss', {
		compass: true,
		require: './lib/loaders.rb'
	})
		.pipe(gulp.dest('build/css'));
});

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