import cv2
import time
import argparse
import imutils
import datetime
import config as cf
import sendEmailsWithImage


def detect_motion():
    fps = cf.fps
    interval_time = cf.interval_time
    last_time = time.time()
    global preFrame

    camera = cv2.VideoCapture(0)

    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--min-area", type=int, default=cf.min_area, help="minimum area size")
    args = vars(ap.parse_args())

    # check camera
    if camera.isOpened():
        print('Camera Open')
    else:
        print('Please open your camera!')

    # print frame size
    # size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
    #         int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # print('size:' + repr(size))

    preFrame = None
    camera = cv2.VideoCapture(0)

    n = 0
    while True:
        (grabbed, frame) = camera.read()
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        n += 1
        if preFrame is None:
            preFrame = gray
            continue
        if n >= fps:
            preFrame = gray
            n = 0

        frameDelta = cv2.absdiff(preFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        text = "safe"
        change = False
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "movement detected"
            change = True

        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        if change:
            now_time = time.time()
            if (now_time - last_time) > interval_time:
                last_time = now_time
                localtime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
                print("Motion Detected!  " + localtime)
                cv2.imwrite('motion.png', frame)
                sendEmailsWithImage.sendEmail('motion.png')

        cv2.imshow("Security Feed", frame)
        # cv2.imshow("Frame Delta", frameDelta)
        # cv2.imshow("Thresh", thresh)


        # press q to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # When everything done, release the capture
    camera.release()
    cv2.destroyAllWindows()
