NUMBER_OF_SENSORS = 8
PLOTS_PER_ROw = 3

plots = {
    # default plot parameters
    'default': {
        'title': 'Sensor {index}',
        'color': '6F6',
        'xrange': [0, 1000],
        'yrange': [0, 10],
        'fill': False,
    },

    # specialized parameters
    0: {
        'title': 'Meh',
        'color': '67C8FF',
        'yrange': [40, 160],
    },
    5: {
        'yrange': [0, 700],
        'color': 'F66'
    },
    4: {
        'fill': '6F63'
    }
}

# defines basic calibration/transformation functions
transform = {
    'default': None,
    # scale [0,1024) => [50,150)
    0: lambda x: x/1024*100+50,
    # identity
    3: lambda x: x,
}

# export to file
export = {
    'raws': {
        'format': 'text',
        'stage': 'acquisition',
        'filename': 'raw_data.data'
    },
    'transformed': {
        'format': 'text',
        'stage': 'process',
        'filename': 'scaled_data.data'
    }
}