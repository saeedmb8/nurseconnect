'use strict';

var gulp            = require('gulp');
var autoprefixer    = require('gulp-autoprefixer');
var bless           = require('glup-bless');
var browserSync     = require('browser-sync').create();
var cssNano         = require('gulp-cssnano');
var pixRem          = require('gulp-pixrem');
var sass            = require('gulp-sass');
var watch           = require('gulp-watch');

/* =================================== */
/* *** constants *** */

var srcPath = 'src/';
var distPath = 'dist/';

var srcSass = srcStatic + '/sass';
var distSass = distStatic + '/css';
var production = argv.production >= 1;

/* =================================== */
/* *** SASS *** */

gulp.task('sass', function () {
  return gulp.src(srcSass + '/**/*.s+(a|c)ss')
    .pipe(plumber())
    .pipe(sass().on('error', sass.logError))
    .pipe(bless())
    .pipe(autoprefixer())
    .pipe(gulpif(production, cssNano()))
    .pipe(plumber.stop())
    .pipe(gulp.dest(distSass + './css'))
    .pipe(browserSync.stream());
});

/* =================================== */
/* *** sync browser *** */


// Static server
gulp.task('browser-sync', function() {
    browserSync.init({
        server: {
            baseDir: "./"
        }
    });

    gulp.watch(pathSass + '/**/*.s+(a|c)ss', ['sass']);
    gulp.watch("/*.html").on('change', browserSync.reload);
});
