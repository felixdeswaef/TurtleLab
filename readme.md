# TurtleLab
Dear teammates, please clone this repo on your laptop/pc with:
```
git clone https://github.com/felixdeswaef/TurtleLab
```
To get updates from other people that haved pushed changes use `git pull` frequently so your local repo stays up to date.
Make your changes to this local repo (on your laptop, not on the turtlebot) and commit them afterwards using:
- `git status` to see what you have changed
- `git add fileA fileB ...` to add the files you want to commit (or simply use `git add --all` to add all changed files)
- `git commit -m "a message"` to commit the changes to your local repo <br/>
Then you can push them to the git remote repo with `git push`. 
(In case you are a couple commits behind, you will have to pull first. Subsequently solve possible merge conflicts and then push again)

## Coding in the local repo on your laptop
### Creating a new pkg
When creating a new package for nodes, do this on the turtlebot (because colcon builds the packages here to binaries which are not on git):
- first connect to the turtlebot `ssh ubuntu@192.168.5.5`
- enter passwd
- go to the src folder `cd turtlebot_ws/src` 
- create the ros2 package `ros2 pkg create --build-type ament_python <package_name>`
- add to git: `git status`, `git add --all`, `git commit -m "new package"`, `git push`
- make some nodes for this package on your laptop...
More information about ros2 packages can be found in the [ros2 foxy docs](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)
### Adding a node to a package
For example let"s add a node to the package **test_nodes**, do this on your laptop:
- Create a node in python (e.g. mynode.py) (location: TurtleLab/test_nodes/test_nodes/mynode.py)
- add an entry point in the setup.py file (location: TurtleLab/test_nodes/setup.py):<br/>
entry_points={ <br/>
&emsp;'console_scripts': [<br/>             
&emsp;&emsp;'talker = test_nodes.publisher_firemech_test:main',<br/>
&emsp;&emsp;'listener = test_nodes.subscriber_firemech:main',<br/>
&emsp;&emsp;*ADD AN ENTRY POINT HERE, e.g. <'name = pkg_name.file_name:function_name'>*<br/>
&emsp;],<br/>
}<br/>
- if your node uses imports that are note standard ros, include them in the **package.xml**, e.g. <exec_depend>your_lib</exec_depend> as depencies. (more info in the [docs](https://docs.ros.org/en/foxy/Tutorials/Intermediate/Rosdep.html))
- add to git: `git status`, `git add --all`, `git commit -m "new package"`, `git push`
- test your node on the turtlebot, this is explained in the section "Testing your code on the turtlebot" below

## Testing your code on the turtlebot
After you have written some code on your laptop and you have pushed this code to git, you can test it on the turtlebot.
- Connect to the turtlebot with `ssh ubuntu@192.168.5.5`
- enter the psswd that is very secret ...
- go to the local git repo on the bot with `cd turtlebot_ws/src`
- pull the changes from the remote git repo with `git pull`
- go back to the turtlebot_ws folder `cd ..` and build the project with `colcon build`
- run your nodes with `ros2 run pkg_name node_name`<br/>
Note: If you are using depencies on the bot from other git repos, venvs, large files,... -> add them to the **.gitignore** file.
Note: make sure the ros2 turtlebot bringup is already running to init all things turtlebot:
- Connect to the turtlebot with `ssh ubuntu@192.168.5.5`
- enter the psswd that is very secret ...
- launch the bringup file with `ros2 launch turtlebot3_bringup robot.launch.py`
- let this terminal run indefinitely (only one person has to do is)


