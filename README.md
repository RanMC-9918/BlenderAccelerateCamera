# BlenderAccelerateCamera
This is a blender script that lets you apply quick and smooth accelerations for large scale camera movement. This first time learning Python and my first time using the Blender Python API, so don't judge.
<hr>
<h2>Instructions</h2>
<ol>
  <li>Go to the scripting tab in blender and copy + paste this script</li>
  <li>Click the run button</li>
  <li>Go to the layout tab and set up your scene</li>
  <li>Make a camera</li>
  <li>Make any empty and rename it to <b>CamControl</b></li>
  <li>Add 2 identical keyframes(all channels) every time you want to exert a force/torque on the camera</li>
  <li>The time in between the 2 keyframes will be the duration the force is applied</li>
  <li>The location/rotation of <b>CamControl</b> will be the magnitude and direction the force is applied</li>
  <li>Click <b>N</b> to open the right panel</li>
  <li>Find the panel named <b>CamControl</b></li>
  <li>Adjust the <b>Damping</b> to make the camera slow down over time</li>
  <li>Adjust the <b>Affect</b> if forces are too strong</li>
  <li>Click <b>Get Data</b> to extract the <b>CamControl</b> data</li>
  <li>Click <b>Render Frames</b> while <b>selecting the camera</b> to apply the forces animation on the camera</li>
</ol>
