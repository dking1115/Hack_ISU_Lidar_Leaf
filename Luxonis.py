#!/usr/bin/env python3

import cv2
import numpy as np
import depthai as dai

# Weights to use when blending depth/rgb image (should equal 1.0)
rgbWeight = 0.4
depthWeight = 0.6


def updateBlendWeights(percent_rgb):
    """
    Update the rgb and depth weights used to blend depth/rgb image

    @param[in] percent_rgb The rgb weight expressed as a percentage (0..100)
    """
    global depthWeight
    global rgbWeight
    rgbWeight = float(percent_rgb)/100.0
    depthWeight = 1.0 - rgbWeight


# Optional. If set (True), the ColorCamera is downscaled from 1080p to 720p.
# Otherwise (False), the aligned depth is automatically upscaled to 1080p
downscaleColor = True
fps = 30
# The disparity is computed at this resolution, then upscaled to RGB resolution
monoResolution = dai.MonoCameraProperties.SensorResolution.THE_720_P

# Create pipeline
pipeline = dai.Pipeline()
device = dai.Device()
queueNames = []

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
left = pipeline.create(dai.node.MonoCamera)
right = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)

rgbOut = pipeline.create(dai.node.XLinkOut)
disparityOut = pipeline.create(dai.node.XLinkOut)

rgbOut.setStreamName("rgb")
queueNames.append("rgb")
disparityOut.setStreamName("disp")
queueNames.append("disp")

#Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setFps(fps)
if downscaleColor: camRgb.setIspScale(2, 3)
# For now, RGB needs fixed focus to properly align with depth.
# This value was used during calibration
try:
    calibData = device.readCalibration2()
    lensPosition = calibData.getLensPosition(dai.CameraBoardSocket.CAM_A)
    if lensPosition:
        camRgb.initialControl.setManualFocus(lensPosition)
except:
    raise
left.setResolution(monoResolution)
left.setCamera("left")
left.setFps(fps)
right.setResolution(monoResolution)
right.setCamera("right")
right.setFps(fps)

stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# LR-check is required for depth alignment
stereo.setLeftRightCheck(True)
stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)

# Linking
camRgb.isp.link(rgbOut.input)
left.out.link(stereo.left)
right.out.link(stereo.right)
stereo.disparity.link(disparityOut.input)
device.startPipeline(pipeline)
# Connect to device and start pipeline
def get_img():
    

    frameRgb = None
    frameDisp = None

    # Configure windows; trackbar adjusts blending ratio of rgb/depth
    rgbWindowName = "rgb"
    depthWindowName = "depth"
    blendedWindowName = "rgb-depth"
    """
    cv2.namedWindow(rgbWindowName)
    cv2.namedWindow(depthWindowName)
    cv2.namedWindow(blendedWindowName)
    cv2.createTrackbar('RGB Weight %', blendedWindowName, int(rgbWeight*100), 100, updateBlendWeights)
    """
    if True:
        latestPacket = {}
        latestPacket["rgb"] = None
        latestPacket["disp"] = None

        queueEvents = device.getQueueEvents(("rgb", "disp"))
        for queueName in queueEvents:
            packets = device.getOutputQueue(queueName).tryGetAll()
            if len(packets) > 0:
                latestPacket[queueName] = packets[-1]

        if latestPacket["rgb"] is not None:
            frameRgb = latestPacket["rgb"].getCvFrame()
            #cv2.imshow(rgbWindowName, frameRgb)

        if latestPacket["disp"] is not None:
            frameDisp = latestPacket["disp"].getFrame()
            dists=frameDisp
            maxDisparity = stereo.initialConfig.getMaxDisparity()
            #print(frameDisp)
            # Optional, extend range 0..95 -> 0..255, for a better visualisation
            if 1: frameDisp = (frameDisp * 255. / maxDisparity).astype(np.uint8)
            # Optional, apply false colorization
            if 1: frameDisp = cv2.applyColorMap(frameDisp, cv2.COLORMAP_HOT)
            frameDisp = np.ascontiguousarray(frameDisp)
            #cv2.imshow(depthWindowName, frameDisp)

        # Blend when both received
        if frameRgb is not None and frameDisp is not None:
            # Need to have both frames in BGR format before blending
            if len(frameDisp.shape) < 3:
                frameDisp = cv2.cvtColor(frameDisp, cv2.COLOR_GRAY2BGR)
            blended = cv2.addWeighted(frameRgb, rgbWeight, frameDisp, depthWeight, 0)
            #cv2.imshow(blendedWindowName, blended)
            

            height,width,channels=frameRgb.shape

            fx = 500  # Focal length in x
            fy = 500  # Focal length in y
            cx = width / 2  # Principal point in x
            cy = height / 2  # Principal point in y

            # Create a grid of pixel coordinates
            x, y = np.meshgrid(np.arange(width), np.arange(height))
            x_normalized = (x - cx) / fx
            y_normalized = (y - cy) / fy

            # Calculate XYZ coordinates
            z = dists
            x_world = x_normalized * z
            y_world = y_normalized * z
            #print(point)
            points=np.zeros((height, width, 6), dtype=np.float32)

            
            for i in range(width):
                for j in range(height):
                    #print(f"i: {i} j: {j}")
                    point=[frameRgb[j,i,0],frameRgb[j,i,1],frameRgb[j,i,2],x_world[j,i],y_world[j,i],z[j,i]]
                    points[j,i]=point

            img_out=frameRgb
            frameRgb = None
            frameDisp = None
            points=np.array(points)
            return img_out,points
        else:
            return get_img()

if __name__=="__main__":
    while True:
        get_img()
