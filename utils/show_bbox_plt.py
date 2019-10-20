import numpy as np 
import matplotlib.pyplot as plt 

def draw_bounding_boxes_on_images(images, results, class_info, thresold=0.6):
	for i, img in enumerate(images):
		# Parse the outputs. each result contains many boxes. 
		det_label = results[i][:, 0]
		det_conf = results[i][:, 1]
		det_xmin = results[i][:, 2]
		det_ymin = results[i][:, 3]
		det_xmax = results[i][:, 4]
		det_ymax = results[i][:, 5] 

		# Get detections with confidence higher than thresold <- probability
		top_indices = [i for i, conf in enumerate(det_conf) if conf >= thresold]
		top_conf = det_conf[top_indices]
		top_label_indices = det_label[top_indices].tolist()
		top_xmin = det_xmin[top_indices]
		top_ymin = det_ymin[top_indices]
		top_xmax = det_xmax[top_indices]
		top_ymax = det_ymax[top_indices]

		colors = plt.cm.hsv(np.linspace(0, 1, len(class_info) )).tolist() 

		dpi = plt.gcf().dpi
		print(dpi)
		xinch = np.shape(img)[1] / dpi
		yinch = np.shape(img)[0] / dpi
		print (xinch,yinch)
		plt.figure(figsize=(xinch,yinch))
		plt.imshow(img / 255.)

		currentAxis = plt.gca()

		for box_idx in range(top_conf.shape[0]):
			xmin = top_xmin[box_idx]
			ymin = top_ymin[box_idx]
			xmax = top_xmax[box_idx]
			ymax = top_ymax[box_idx]
			score = top_conf[box_idx]
			label = int(top_label_indices[box_idx])
			label_name = class_info[label - 1] 
			display_txt = '{:0.2f}, {}'.format(score, label_name)
			coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
			color = colors[label]
			currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
			currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5}) 
			
		plt.savefig('result_plt.png')