Shapes = {
	'I': [
		[0,0,0,0],
		[1,1,1,1],
		[0,0,0,0],
		[0,0,0,0],
	],
	'J': [
		[1,0,0],
		[1,1,1],
		[0,0,0]
	],
	'L': [
		[0,0,1],
		[1,1,1],
		[0,0,0]
	],
	'O': [
		[1,1],
		[1,1]
	],
	'S': [
		[0,1,1],
		[1,1,0],
		[0,0,0]
	],
	'T': [
		[0,1,0],
		[1,1,1],
		[0,0,0]
	],
	'Z': [
		[1,1,0],
		[0,1,1],
		[0,0,0]
	]
}

Colors = {
	'I': 6,
	'J': 4,
	'L': 3,
	'O': 3,
	'S': 2,
	'T': 5,
	'Z': 1
}

Wallkick = {
    'I': [
        [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        [[-2, 0], [2, 0], [-1, 0], [1, 0], [2, 0], [-2, 0], [1, 0], [-1, 0]],
        [[1, 0], [-1, 0], [2, 0], [-2, 0], [-1, 0], [1, 0], [-2, 0], [2, 0]],
        [[-2, 1], [2, -1], [-1, -2], [1, 2], [2, -1], [-2, 1], [1, 2], [-1, -2]],
        [[1, -2], [-1, 2], [2, 1], [-2, -1], [-1, 2], [1, -2], [-2, -1], [2, 1]]
    ],
    'default': [
        [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        [[-1, 0], [1, 0], [1, 0], [-1, 0], [1, 0], [-1, 0], [-1, 0], [1, 0]],
        [[-1, -1], [1, 1], [1, 1], [-1, -1], [1, -1], [-1, 1], [-1, 1], [1, -1]],
        [[0, 2], [0, -2], [0, -2], [0, 2], [0, 2], [0, -2], [0, -2], [0, 2]],
        [[-1, 2], [1, -2], [1, -2], [-1, 2], [1, 2], [-1, -2], [-1, -2], [1, 2]],
    ]
}