// Example config using js rather than json.
module.exports = {
    // The viewports
    'viewports': [{
        'name': 'feature_phone',
        'width': 240,
        'height': 360
    }, {
        'name': 'phone',
        'width': 320,
        'height': 480
    }, {
        'name': 'tablet_v',
        'width': 568,
        'height': 1024
    }, {
        'name': 'tablet_h',
        'width': 1024,
        'height': 768
    }],

    // Scenarios
    'scenarios': [{
        'label': 'index',
        'url': '../../templates/index.html',
        'hideSelectors': [],
        'removeSelectors': [],
        'selectors': [
            'body'
        ],
        // 'readyEvent': 'backstop.ready',
        'delay': 100,
        'misMatchThreshold': 0.1
    }, {
        'label': 'index',
        'url': '../../templates/base.html',
        'hideSelectors': [],
        'removeSelectors': [],
        'selectors': [
            'body'
        ],
        // 'readyEvent': 'backstop.ready',
        'delay': 100,
        'misMatchThreshold': 0.1
    }],
    'paths': {
        'bitmaps_reference': '../../backstop_data/bitmaps_reference',
        'bitmaps_test': '../../backstop_data/bitmaps_test',
        'compare_data': '../../backstop_data/bitmaps_test/compare.json'
    },
    'engine': 'phantomjs',
    'report': ['browser', 'CLI'],
    'port': 3005
};
