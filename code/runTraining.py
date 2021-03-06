import sys

import tifffile
import copy
import cv2
import imutils
import numpy as np
from imtools import Img, reverse_tform_order
from TF_models import AtlasNet, TrainTForm, ElasticNet
import fsys
import matplotlib.pyplot as plt

## TO DO:

## params for neural network
params = {'load_file':None,#'D:/__Atlas__/model_saves/model-Elastic2_257x265_1000',
          'save_file': 'Elastic2',
          'save_interval': 1000,
          'batch_size': 32,
          'lr': .0001,  # Learning rate
          'rms_decay': 0.999,  # RMS Prop decay
          'rms_eps': 1e-9,  # RMS Prop epsilon
          'width':257,
          'height':265,
          'numParam':3,
          'train':True}

# go to training dir
fsys.cd('D:/__Atlas__')

## initialize net
#net = AtlasNet(params)
net = ElasticNet(params)
#net = ElasticNet(params)

train_files = fsys.file('trainData/*')

# test objective function
# fixed = cv2.imread('30890 B1S2 272N_01_small.jpg')
# fixed = cv2.cvtColor(fixed, cv2.COLOR_BGR2GRAY)
# fixed = cv2.resize(fixed, (0,0), fx=0.125, fy=0.125)
# fixed = fixed.astype(np.float32)/255.
# fixed= cv2.copyMakeBorder(fixed,25,25,25,25,cv2.BORDER_CONSTANT,value=0.0)
# moving = fixed
# H1,H2 = net.run(fixed,moving)
# print(H1)
# print(H2)
# print('Done!')
# sys.exit()


# train network
avgCost = 100*[np.inf]
avgCost2 = 100*[np.inf]
train_tform = TrainTForm({'width':257,'height':265})

for itrain in range(490000):
  # get batch files
  f_batch = np.random.choice(train_files,params['batch_size'])

  # random uniform sample of transformations
  # ideal = np.random.uniform(low=-40,high=40,size=(params['batch_size'],params['numParam']))
  # ideal2 = copy.deepcopy(ideal)
  batch = np.zeros(shape=(params['batch_size'],params['width'],params['height'],2),dtype=np.float32)

  ####
  #batch2 = np.zeros(shape=(params['batch_size'], params['width'], params['height'], 2))

  # ideal[0,:] = [50,-10,10]
  # create noisy batch
  for b,f in enumerate(f_batch):
    with tifffile.TiffFile(f) as tif:
      img = tif.asarray()
    #img[img<5]=255.
    #img[img==255.] = 0
    img = cv2.resize(img, (params['height'],params['width']))

    #img = img.astype(np.float32) / 255.
    #cyber
    img = imutils.translate(img, np.random.normal(0,3,1), np.random.normal(0,3,1))


    # cv2.imshow('raw', img)
    # cv2.waitKey(0)

    # do flip/reflection
    if np.random.uniform(0, 1, 1) > .125:
      img = np.flipud(img)
    if np.random.uniform(0, 1, 1) > .125:
      img = np.fliplr(img)


    # cv2.imshow('raw', img)
    # cv2.waitKey(0)

    # add noise
    # if np.random.uniform(0, 1, 1) > .05:
    #   m = (0., 0., 0.)
    #   s = (0.1, 0.1, 0.0)
    #   #img = img + cv2.randn(img, m, s)
    #   img = img + .05*np.random.randn(img.shape[0],img.shape[1],img.shape[2])
    # if np.random.uniform(0, 1, 1) > .05:
    #   m = (0., 0., 0.)
    #   s = (0., 0.1, 0.)
    #   #img = img + cv2.randn(img, m, s)
    #   img = img + .05*np.random.randn(img.shape[0], img.shape[1], img.shape[2])
    # if np.random.uniform(0, 1, 1) > .05:
    #   m = (0., 0., 0.)
    #   s = (0.1, 0., 0.)
    #   #img = img + cv2.randn(img, m, s)
    #   img = img + .05*np.random.randn(img.shape[0], img.shape[1], img.shape[2])

    #cv2.imshow('raw', img)
    #cv2.waitKey(0)

    # flip white/ black
    # if 0:#np.random.uniform(0, 1, 1) > .25:
    #   img[img>=.98] = 0.
    #   img[img <= 0.02] = 1.

    # cv2.imshow('raw', img)
    # cv2.waitKey(0)

    # cv2.imshow('raw', img)
    # cv2.waitKey(0)

    # swap fixed/moving
    # if True:#np.random.uniform(0,1,1)>.5:
    #   fixed = img[:,:,0]
    #   moving = img[:,:,1]
    # else:
    #   fixed = img[:, :, 1]
    #   moving = img[:, :, 0]

    # invert
    # if 0:#np.random.uniform(0, 1, 1) > .25:
    #   fixed = 1. - fixed
    # if 0:#np.random.uniform(0, 1, 1) > .25:
    #   moving = 1. - moving

    # fixed = fixed.astype(np.float32)
    # moving = moving.astype(np.float32)


    # apply transformation
    #DRot = -ideal[b,2]*(math.pi/180)
    #transMAT = np.array([[np.cos(DRot), np.sin(DRot), ideal[b,0]], [-np.sin(DRot), np.cos(DRot), ideal[b,1]]])
    #transMAT = np.linalg.inv(np.array([[np.cos(DRot), np.sin(DRot), -ideal[b,0]], [-np.sin(DRot), np.cos(DRot), -ideal[b,1]], [0, 0, 1]]))
    #transMAT = transMAT[0:2,:]

    #rows, cols = moving.shape
    #moving = cv2.warpAffine(moving, transMAT, (cols, rows))

    # moving = imutils.rotate(moving, ideal[b,2])
    # moving = imutils.translate(moving, ideal[b,0], ideal[b,1])

    #cv2.imshow('raw', fixed)
    #cv2.waitKey(0)
    #cv2.imshow('raw', moving)
    #cv2.waitKey(0)
    # save into batch
    # batch2[b,:,:,:] = cv2.merge((Img.from_array(fixed).p_intensity,Img.from_array(moving).p_intensity))
    #batch[b,:,:,:] = cv2.merge((Img.from_array(img[:,:,0]).p_intensity,Img.from_array(img[:,:,1]).p_intensity))
    batch[b, :, :, :] = np.stack((img[:, :, 0], img[:, :, 1]),axis=2)
    #img[:,:,0:1]#cv2.merge((Img.from_array(fixed).p_intensity,Img.from_array(moving).p_intensity))
    # dxdy = reverse_tform_order(ideal[b,2],ideal[b,0],ideal[b,1])
    # ideal2[b,0] = dxdy[0][0]
    # ideal2[b,1] = dxdy[0][1]
  #moved = train_tform.run(-ideal2,batch)[0]
  #for i in range(params['batch_size']):
  #    batch[i,:,:,1] = np.squeeze(moved[i,:,:])
  batch = batch + .005 * np.random.randn(batch.shape[0], batch.shape[1], batch.shape[2],batch.shape[3])
  #TEST
  # tformed,xytheta,cost_cc,E,t_vals,p_vals, dxy, e2 = net.run_batch(batch)
  # print(e2)
  # for i in range(batch.shape[0]):
  #
  #   plt.subplot(2,2,1)
  #   #f, (ax1, ax2, ax3, ax4) = plt.subplots(2, 2, sharey=True,figsize=(20, 7))
  #   merged = np.dstack(
  #       (np.array(batch[i, :, :, 0]), np.array(batch[i, :, :, 1]), np.array(batch[i, :, :, 1])))
  #   plt.imshow(merged)
  #   plt.subplot(2,2,2)
  #   merged = np.dstack(
  #     (np.array(batch[i, :, :, 0]), np.array(tformed[i, :, :, 0]), np.array(tformed[i, :, :, 0])))
  #   plt.imshow(merged)
  #   plt.subplot(2,2,3)
  #   plt.imshow(dxy[i,:,:,0])
  #   plt.colorbar()
  #   plt.subplot(2,2,4)
  #   plt.imshow(dxy[i, :, :, 1])
  #   plt.colorbar()
  #   plt.show()
  # exit()

  # plt.imshow(np.array(tformed[0][:][:][:]).squeeze())
  # plt.show()
  cnt, cost, cost_cc, E_det_j, E_div, E_curl = net.train(batch) # , out, cost_t
  #cnt, cost, cost_cc, E_det_j, E_div, E_curl
  #train
  #cnt,cost = net.train(batch,ideal)
  avgCost.append(cost)
  avgCost.pop(0)
  avgCost2.append(cost_cc)
  avgCost2.pop(0)
  # print('count: {}, cost_p: {}, cost_cc: {}, avg_cost: {}, avg_cc: {}, sanity: {}'.format(cnt, cost, cost_t, np.mean(avgCost),np.mean(avgCost2),
  #                                                              np.mean(np.abs(out), axis=0)))
  #print((cnt,cost))
  print('count: {}, cost: {}, cost_cc: {}, avg_cost: {}, avg_cost_cc: {}, e_det_j: {}, e_div {}, e_curl {}'.format(
      cnt,
      cost,
      cost_cc,
      np.mean(avgCost),
      np.mean(avgCost2),
      np.mean(E_det_j),
      np.mean(E_div),
      np.mean(E_curl)))

  if (params['save_file']):
    if cnt % params['save_interval'] == 0:
      net.save_ckpt('model_saves/model-' + params['save_file'] + "_" + str(params['width'])+'x'+str(params['height']) + '_' + str(cnt))
      print('Model saved')

# now do test
ideal = np.random.uniform(low=-20, high=20, size=(1, params['numParam']))
#img2 = np.zeros(shape=(1,fixed.shape[0],fixed.shape[1],2))
moving = imutils.rotate(fixed, ideal[0,0])
moving = imutils.translate(moving, ideal[0,1], ideal[0,2])
#img2[0,:,:,:] = cv2.merge((fixed,moving))

#p = net.sess.run(net.Out,feed_dict = {net.In:img2})
result_ = net.sess.run(net.result,feed_dict = {net.In:batch})
#moving = imutils.translate(moving, p[0,1], p[0,2])
#moving = imutils.rotate(moving, p[0,0])
#print(p)
print(-ideal)

cv2.imshow('fixed',batch[0,:,:,0])
cv2.waitKey(0)
cv2.imshow('moving',batch[0,:,:,1])
cv2.waitKey(0) # Waits forever for user to press any key
cv2.imshow('moved',np.swapaxes(np.swapaxes(np.array((batch[0,:,:,0].squeeze(),batch[0,:,:,0].squeeze(),result_[0,:,:,1].squeeze())),0,2),0,1))
cv2.waitKey(0)
cv2.destroyAllWindows()


#  cv2.imshow('fixed',fixed)
# cv2.waitKey(0)
# cv2.imshow('moving',moving)
# cv2.waitKey(0)                 # Waits forever for user to press any key
# cv2.destroyAllWindows()