from setuptools import setup

package_name = 'test_nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [              
        	'talker = test_nodes.publisher_firemech_test:main',
            'firemech = test_nodes.firemech:main',
            'vel_publisher = test_nodes.vel_publisher:main',
            'keyboard_reader = test_nodes.keyboard_reader:main',
            'visual_cortex = test_nodes.visual_cortex:main',
            'lidarInput = test_nodes.lidarInput:main',
            'movement_controller = test_nodes.movement_controller:main',
            'test_visual_cortex = test_nodes.test_visual_cortex:main',
            'ledsub = test_nodes.ledsub:main',
            'angle = test_nodes.angle_firemech:main',
            'publi2 = test_nodes.publisher_anglemech_test:main'
            'spideysense= test_nodes.spideysense:main'
        ],
    },
)
