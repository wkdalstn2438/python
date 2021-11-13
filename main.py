def detection_result():
    device = select_device('cpu')

    dect_model = attempt_load('../save_model/yolo_best.pt', map_location=device)
    dect_model.eval()

    with torch.no_grad():
        detection_result = []

        img_path = ""
        img = cv2.imread(img_path)

        detection_pred, _ = detect_img(img, dect_model)
        detection_result.append(detection_pred)

