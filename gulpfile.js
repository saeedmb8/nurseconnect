'use strict';

var gulp            = require('gulp');
var argv            = require('yargs').argv;
var autoprefixer    = require('gulp-autoprefixer');
var bless           = require('gulp-bless');
var browserSync     = require('browser-sync').create();
var cssNano         = require('gulp-cssnano');
var del             = require('del');
var gulpif          = require('gulp-if');
var pixRem          = require('gulp-pixrem');
var plumber         = require('gulp-plumber');
var runSequence     = require('run-sequence');
var sass            = require('gulp-sass');
var watch           = require('gulp-watch');

/* =================================== */
/* *** constants *** */

var srcPath = 'src';
var distPath = 'dist';

var production = argv.production >= 1;

/* =================================== */
/* *** SASS *** */

gulp.task('styles',['clean-css'] ,function () {
    return gulp.src(srcPath + '/sass/**/*.s+(a|c)ss')
    .pipe(plumber())
    .pipe(sass().on('error', sass.logError))
    .pipe(bless())
    .pipe(autoprefixer())
    .pipe(gulpif(production, cssNano()))
    .pipe(plumber.stop())
    .pipe(gulp.dest(distPath + '/css'))
    .pipe(browserSync.stream());
});

gulp.task('clean-css', function() {
    return del(distPath + '/css');
});

/* =================================== */
/* *** sync browser *** */


// Static server
gulp.task('browser-sync', function() {
    browserSync.init({
        server: {
            baseDir: "./templates/"

        }
    });

    gulp.watch(srcPath + '/**/*.s+(a|c)ss', ['styles']);
    gulp.watch("/*.html").on('change', browserSync.reload);
});

/* =================================== */
/* *** sync browser *** */


gulp.task('default', ['clean-css'], function() {
  runSequence('styles', 'browser-sync');
});
