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
            'listener = test_nodes.subscriber_firemech:main',
            'vel_publisher = test_nodes.vel_publisher:main',
            'keyboard_reader = test_nodes.keyboard_reader:main',
            'visual_cortex = test_nodes.visual_cortex:main' ,
            'lidarInput = test_nodes.lidarInput:main',
            'ledSub' = 'test_nodes.ws2812b_subscriber:main'
        ],
    },
)
