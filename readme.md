# TurtleLab
Dear teammates, please clone this repo on your laptop/pc with:
```
git clone https://github.com/felixdeswaef/TurtleLab
```
To get updates from other people that haved pushed changes use `git pull` frequently so your local repo stays up to date.
Make your changes to this local repo (on your laptop, not on the turtlebot) and commit them afterwards using:
- `git status` to see what you have changed
- `git add fileA fileB ...` to add the files you want to commit (or simply use `git add --all` to add all changed files)
- `git commit -m "a message"` to commit the changes to your local repo
Then you can push them to the git remote repo with `git push` 
(if you are a couple commits behind, you will have to pull first and solve merge conflicts before you can push again)

## Coding in the local repo on your laptop
### creating a new pkg
When creating a new package for nodes, do this on the turtlebot (because colcon builds the packages here to binaries which are not on git..):
- first connect to the turtlebot `ssh ubuntu@192.168.5.5`
- enter passwd
- go to the src folder `cd turtlebot_ws/src` 
- create the ros2 package `ros2 pkg create --build-type ament_python <package_name>`
- add to git: `git status`, `git add --all`, `git commit -m "new package"`, `git push`
- make some nodes for this package on your laptop...
### Adding a node to a package
For example let"s add a node to the package test_nodes:
- add your node as a python file (e.g. mynode.py) (location: TurtleLab/test_nodes/test_nodes/mynode.py)
- add an entry point in the setup.py file (location: TurtleLab/test_nodes/setup.py): <br/>
    entry_points={ <br/>
        'console_scripts': [   <br/>             
        	'talker = test_nodes.publisher_firemech_test:main', <br/>
            'listener = test_nodes.subscriber_firemech:main', <br/>
             ADD AN ENTRY POINT HERE <'name = pkg_name.filename:function_name'> <br/>
        ], <br/>
    } <br/>
- on bot `ssh ubuntu@192.168.5.5` : in the turtlebot_ws folder run `colcon build`
- then run your node with `ros2 run pkg_name node_name`

## Testing your code on the turtlebot
After you have written some code on your laptop and you have pushed this code to git, you can test it on the turtlebot.
- Connect to the turtlebot with `ssh ubuntu@192.168.5.5`
- enter the psswd that is very secret ...
- go to the local git repo on the bot with `cd turtlebot_ws/src`
- pull the changes from the remote git repo with `git pull`
- build the project with `colcon build` (while being in the turtlebot_ws folder)
- run your nodes with `ros2 run pkg_name node_name`




