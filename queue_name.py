import depthai as dai

# Create a simple pipeline with a ColorCamera
pipeline = dai.Pipeline()

colorCam = pipeline.createColorCamera()
colorCam.setBoardSocket(dai.CameraBoardSocket.RGB)
colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

# Create an XLinkOut to retrieve stream names
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
colorCam.video.link(xout.input)

# List available streams
with dai.Device(pipeline) as device:
    streams = device.getAvailableStreams()
    print("Available Streams:", streams)

# The correct stream name for RGB data may vary depending on the camera model and configuration.
# Look for the stream name that corresponds to RGB data and use it accordingly.

