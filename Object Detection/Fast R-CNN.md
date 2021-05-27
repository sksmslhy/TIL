# **Fast R-CNN**

paper : [Link](https://arxiv.org/pdf/1504.08083.pdf)

### R-CNN

- 학습 시간이 매우 오래 걸린다.  
- detection 속도 또한 이미지 한 장당 47초 소요.  
- 3가지 모델 (AlexNet, linear SVM, Bounding box regressor)을 독립적으로 학습시켜, 연산을 공유하거나 가중치 값을 update하는 것이 불가능.


**=> 이 문제를 RoI(Region of Interest) pooling으로 해결한 것이 Fast R-CNN !!!**


### Preview  
<image src = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FIv58U%2FbtqPwlVdub3%2FrYZl3fBVLNlPDqKrUsWQrk%2Fimg.png">  

R-CNN 모델은 2000장의 region proposals를 CNN 모델에 입력시켜 각각에 대하여 독립적으로 학습시켜 많은 시간이 소요된다. Fast R-CNN은 이러한 문제를 개선해 **단 1장의 이미지를 입력**받으며, region proposals의 크기를 warp시킬 필요 없이 RoI pooling을 통해 고정된 크기의 feature vector를 fully connected layer에 전달한다. 또한 multi-task loss를 사용해 모델을 개별적으로 학습시킬 필요 없이 한 번에 학습시킨다. 이를 통해 학습 및 detection 시간이 크게 감소하였다.


## Main Ideas

### 1. RoI pooling  

RoI pooling은 feature map에서 region proposals에 해당하는 관심 영역(RoI)을 지정한 크기의 grid로 나눈 후 max pooling을 수행하는 방법이다. 각 channel별로 독립적으로 수행하며, 이같은 방법을 통해 고정된 크기의 feature map을 출력하는 것이 가능하다. 

<image src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbafmBN%2FbtqPsEgEwxB%2FpISRTDmEkK99t4IVQ3Ywh1%2Fimg.jpg">  

1. 먼저 800 x 800 크기의 원본 이미지를 CNN 모델(VGG)에 통과시켜 8 x 8 크기의 feature map을 얻는다. 이때 sub-sampling ratio = 1/100이라고 할 수 있다. (sub-sampling : pooling을 거치는 과정을 의미)  
 2. 동시에 원본 이미지에 대해 Selective search 알고리즘을 적용해 500 x 700 크기의 region proposals를 얻는다.  
 3. feature map에서 각 region proposals에 해당하는 영역을 추출한다.(이 과정은 RoI projection을 통해 가능) Selective search를 통해 얻은 region proposals는 sub-sampling 과정을 거치지 않은 반면, 원본 이미지의 feature map은 sub-sampling 과정을 여러 번 거쳐 크기가 작아진다. 작아진 feature map에서 region proposals이 encode(표현)하고 있는 부분을 찾기 위해 작아진 feature map에 맞게 region proposals를 투영해주는 과정이 필요하다. 이는 region proposal의 크기와 중심 좌표를 sub sampling ratio에 맞게 변경시켜줌으로써 가능하다.  
 4. 추출한 5 x 7 크기의 RoI feature map을 지정한 sub-window의 크기(2 x 2)에 맞게 grid로 나눠준다.  
 5. grid의 각 셀마다 max pooling을 수행해 고정된 2 x 2 크기의 feature map을 얻는다.  

 미리 지정한 크기의 sub-window에서 max pooling을 수행 -> region proposal의 크기가 서로 달라도 고정된 크기의 feature map을 얻을 수 있다.

  
  
  
 ### 2. Multi-task loss  

Fast R-CNN 모델에서는 feature vector를 multi-task loss를 사용하여 Classifier와 Bounding regressor를 동시에 학습시킨다. 각각의 RoI(=region proposal)에 대해 multi task loss를 사용하여 학습시킵니다. 이처럼 두 모델을 한번에 학습시키기 때문에, R-CNN 모델과 같이 **각 모델을 독립적으로 학습시켜야 하는 번거로움이 없다**는 장점이 있다.   

Multi-task loss는 다음과 같다.  
$L(p, u, t^{u}, v) = L_{cls}(p, u) + lambda[u>=1]L_{loc}(t^{u}, v)$  

$p=(p_{0},.....,p_{k})$ : (k+1)개의 class score




