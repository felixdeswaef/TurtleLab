while true
do
  ros2 action send_goal pi_gpio_server pi_gpio_interface/action/GPIO {'gpio: "23,high"'}
  ros2 action send_goal pi_gpio_server pi_gpio_interface/action/GPIO {'gpio: "23,low"'}
done
