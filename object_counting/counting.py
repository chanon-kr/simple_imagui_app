# https://docs.ultralytics.com/modes/track/#python-examples
import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Counting config
line_position = 50
text_size = 30
text_x_position = 50
text_y_position = 0

# Open the camera
cap = cv2.VideoCapture(1)

# Get Camera Parameter
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Counting prep
x_line= line_position*width/100
pt1 = (int(x_line), 0)
pt2 = (int(x_line), int(height))
counting_buffer = {}
counting_result = {'left-to-right' : 0, 'right-to-left' : 0}

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, verbose=False)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Get Data for counting
        result = results[0].cpu().boxes
        detect_id = result.id.tolist() if result.id != None else []
        detect_xyxy = result.xyxy.tolist() if result.xyxy != None else []
        frame_counting_buffer = dict(zip(detect_id, detect_xyxy))
        # Process
        for i in frame_counting_buffer :
            # Prep count buffer
            counting_buffer[i] = counting_buffer.get(i,[])
            if len(counting_buffer[i]) >= 2 : counting_buffer[i] = counting_buffer[i][-1:]
            # Append avg x axis to buffer
            avg_x = (frame_counting_buffer[i][0] + frame_counting_buffer[i][2])/2
            counting_buffer[i].append(avg_x)
            # Count logic
            if len(counting_buffer[i]) >= 2 : 
                if (counting_buffer[i][0] > x_line) & (counting_buffer[i][1] < x_line) :
                    counting_result['right-to-left'] += 1
                elif (counting_buffer[i][0] < x_line) & (counting_buffer[i][1] > x_line) :
                    counting_result['left-to-right'] += 1

        # Create Line
        cv2.line(annotated_frame, pt1= pt1, pt2= pt2 , color= (0,0,255), thickness= 2) 
        # Put Counting to picture
        text_position = text_y_position
        for i in counting_result : 
            text_position += text_size
            info_text = f"{i} : {counting_result[i]}"
            annotated_frame = cv2.putText(  annotated_frame
                                          , info_text
                                          , (int(width*text_x_position/100)
                                          , text_position)
                                          , cv2.FONT_HERSHEY_SIMPLEX
                                          , 1
                                          , (0,0,255)
                                          , 1
                                          , cv2.LINE_AA)
            

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
