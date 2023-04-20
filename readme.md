# TurtleLab
Please clone this repo with:
`git clone https://github.com/felixdeswaef/TurtleLab`
Make your changes to your local repo on your laptop and commit them afterwards to your loca repo:
`git status`
`git commit -m "a message"`
Then you can push them to git remote repo:
`git push`
(if you are a couple commits behind you will have to pull first and solve merge conflicts before you can push again)
## Adding a node to a package
For example let"s add a package to test_nodes:
- add your node as a python file (e.g. mynode.py) (TurtleLab/test_nodes/test_nodes/mynode.py)
- add an entry point in the setup.py file (TurtleLab/test_nodes/setup.py)
    entry_points={
        'console_scripts': [                
        	'talker = test_nodes.publisher_firemech_test:main',
            'listener = test_nodes.subscriber_firemech:main',
             ADD AN ENTRY POINT HERE <'name = pkg_name.filename:function_name'>
        ],
    }
- on bot `ssh ubuntu@192.168.5.5` : in turtlebot_ws/ run `colcon build`
- then run your node with `ros2 run pkg_name node_name`


