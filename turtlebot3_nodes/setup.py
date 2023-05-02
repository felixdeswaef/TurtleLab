from setuptools import setup

package_name = 'turtlebot3_nodes'

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
            #main nodes
            'visual_cortex = turtlebot3_nodes.visual_cortex:main',   
            'movement_controller = turtlebot3_nodes.movement_controller:main',
            'ledSub = turtlebot3_nodes.ledSub:main',   
            'firemech = turtlebot3_nodes.firemech:main',   
            #variations of firemech
            'firemech_2 = turtlebot3_nodes.firemech_2:main', 
            'spideysense = turtlebot3_nodes.spideysense:main'
        ],
    },
)
