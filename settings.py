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
        'color': '67C8FF'
    },
    5: {
        'yrange': [0, 700],
        'color': 'F66'
    },
    4: {
        'fill': '6F63'
    }
}
